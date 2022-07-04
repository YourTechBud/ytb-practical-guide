package main

import "github.com/open-policy-agent/opa/rego"

// K8sConstraintSpecObject is use to store the opa gatekeeper constraints
type K8sConstraintSpecObject struct {
	API  string            `json:"apiVersion" yaml:"apiVersion" mapstructure:"api"`
	Kind string            `json:"kind" yaml:"kind" mapstructure:"kind"`
	Meta K8sConstraintMeta `json:"metadata" yaml:"metadata,omitempty" mapstructure:"meta"`
	Spec K8sConstraintSpec `json:"spec" yaml:"spec,omitempty" mapstructure:"spec"`
}

// K8sConstraintMeta is use to store the opa gatekeeper constraints meta data
type K8sConstraintMeta struct {
	Name   string                 `json:"name" yaml:"name,omitempty" mapstructure:"name"`
	Labels map[string]interface{} `json:"labels" yaml:"labels,omitempty" mapstructure:"labels"`
}

// K8sConstraintSpec is use to store the opa gatekeeper constraints spec
type K8sConstraintSpec struct {
	EnforcementAction string      `json:"enforcementAction" yaml:"enforcementAction,omitempty" mapstructure:"enforcementAction"`
	Match             K8sMatch    `json:"match" yaml:"match,omitempty" mapstructure:"match"`
	Parameters        interface{} `json:"parameters" yaml:"parameters,omitempty" mapstructure:"parameters"`
}

// K8sMatchLabels is use to store the opa gatekeeper constraints spec match labels field
type K8sMatchLabels struct {
	MatchLabels map[string]string `json:"matchLabels" yaml:"matchLabels,omitempty" mapstructure:"matchLabels"`
}

// K8sMatch is use to store the opa gatekeeper constraints spect match field
type K8sMatch struct {
	Kind               []K8sKind      `json:"kinds" yaml:"kinds,omitempty" mapstructure:"kinds"`
	LabelSelector      K8sMatchLabels `json:"labelSelector" yaml:"labelSelector,omitempty" mapstructure:"labelSelector"`
	Namespaces         []string       `json:"namespaces" yaml:"namespaces,omitempty" mapstructure:"namespaces"`
	ExcludedNamespaces []string       `json:"excludedNamespaces" yaml:"excludedNamespaces,omitempty" mapstructure:"excludedNamespaces"`
}

// K8sKind is use to store the opa gatekeeper constraints spec match labels kind field
type K8sKind struct {
	APIGroups []string `json:"apiGroups" yaml:"apiGroups,omitempty" mapstructure:"apiGroups"`
	Kinds     []string `json:"kinds" yaml:"kinds,omitempty" mapstructure:"kinds"`
}

// RegoStruct is used to store pa gatekeeper prepared query and openApiSchema
type RegoStruct struct {
	Query         rego.PreparedEvalQuery
	Name          string
	OpenAPISchema map[string]interface{}
}
