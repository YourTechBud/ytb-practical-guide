package main

import (
	"context"
	"fmt"
	"io/ioutil"
	"log"
	"strings"

	"github.com/ghodss/yaml"
	"github.com/open-policy-agent/opa/ast"
	"github.com/open-policy-agent/opa/rego"
)

func main() {
	ctx := context.Background()

	preparedRegoQuery, err := createRegoPreparedQueryFromTemplateFile(ctx, "opa-template.yaml")
	if err != nil {
		log.Panic(err)
	}

	opaConstraintsParams, err := getConstraintParamsFromConstraintFile("opa-policy.yaml")
	if err != nil {
		log.Panic(err)
	}

	resource, err := getResource("deployment.yaml")
	if err != nil {
		log.Panic(err)
	}

	err = evaluateRego(ctx, preparedRegoQuery, opaConstraintsParams, resource)
	if err != nil {
		log.Panic(err)
	}
}

func createRegoPreparedQueryFromTemplateFile(ctx context.Context, filename string) (*RegoStruct, error) {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, fmt.Errorf("failed reading data from file: %s", err)
	}

	resourceObject := map[string]interface{}{}
	if err := yaml.Unmarshal(data, &resourceObject); err != nil {
		return nil, fmt.Errorf("failed reading data from file: %s", err)
	}

	regoQuery := resourceObject["spec"].(map[string]interface{})["targets"].([]interface{})[0].(map[string]interface{})["rego"].(string)
	moduleName := resourceObject["metadata"].(map[string]interface{})["name"].(string)

	compiler, err := ast.CompileModules(map[string]string{moduleName + ".rego": regoQuery})
	if err != nil {
		return nil, err
	}

	r := rego.New(
		rego.Query("data[_].violation"),
		rego.Compiler(compiler),
	)

	query, err := r.PrepareForEval(ctx)
	if err != nil {
		return nil, err
	}

	res := RegoStruct{
		Query: query,
		Name:  moduleName,
	}
	return &res, nil
}

func getConstraintParamsFromConstraintFile(filename string) (interface{}, error) {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, fmt.Errorf("failed reading data from file: %s", err)
	}

	resourceObject := K8sConstraintSpecObject{}
	if err := yaml.Unmarshal(data, &resourceObject); err != nil {
		return nil, fmt.Errorf("failed reading data from file: %s", err)
	}

	return resourceObject.Spec.Parameters, nil
}

func getResource(filename string) (map[string]interface{}, error) {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, fmt.Errorf("failed reading data from file: %s", err)
	}

	resourceObject := map[string]interface{}{}
	if err := yaml.Unmarshal(data, &resourceObject); err != nil {
		return nil, fmt.Errorf("failed reading data from file: %s", err)
	}

	return resourceObject, nil
}

func evaluateRego(ctx context.Context, preparedRego *RegoStruct, params interface{}, resource map[string]interface{}) error {
	resourceAPIGroup, resourceVersion := prepareK8sKind(resource["apiVersion"].(string))

	input := map[string]interface{}{
		"review": map[string]interface{}{
			"object": resource,
			"kind": map[string]interface{}{
				"kind":    resource["kind"],
				"group":   resourceAPIGroup,
				"version": resourceVersion,
			},
		},
		"parameters": params,
	}

	rs, err := preparedRego.Query.Eval(ctx, rego.EvalInput(input))
	if err != nil {
		return err
	}

	for _, violations := range rs[0].Expressions[0].Value.([]interface{}) {
		fmt.Println("Violation:", violations.(map[string]interface{})["msg"].(string))
	}

	return nil
}

func prepareK8sKind(resourceAPI string) (string, string) {
	resourceAPIGroup := ""
	resourceVersion := resourceAPI
	if strings.Contains(resourceAPI, "/") {
		resourceAPIGroup = strings.Split(resourceAPI, "/")[0]
		resourceVersion = strings.Split(resourceAPI, "/")[1]
	}
	return resourceAPIGroup, resourceVersion
}
