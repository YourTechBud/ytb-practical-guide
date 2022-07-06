# Shifting policy management left with OPA Gatekeeper

> Special thanks to [@khannaabhi](https://github.com/khannaabhi) for contributing this guide

This app uses the following tools:
- [OPA-Gatekeeper](https://open-policy-agent.github.io/gatekeeper/website/docs/)

## Prerequisites
- A running K8s cluster
- Install OPA Gatekeeper by running the following commands
```bash
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper/release-3.8/deploy/gatekeeper.yaml
```
- Install [Golang](https://go.dev/doc/install) 

## How to test the tool in a K8s cluster
- Install the Gatekeeper's constraint-template and constraint by running the following command
```bash
kubectl apply -f opa-template.yaml
kubectl apply -f opa-policy.yaml 
```
- Create a deployment resource which violates the policy.
```bash
kubectl apply -f deployment.yaml
```
- The creation of deployment resource was rejected by OPA Gatekeeper as it violates the policy.
- The violation can be solved by changing the image tag from `latest` to a proper tag (eg. `1.23.0`)

## Validate the OPA policy at CI layer
OPA Gatekeeper is only meant to work on the CD layer by design. However we can extend it to run on the CI layer by writing some go code using the OPA library.

To test the above functionality build & execute the go script: 
```bash
go build . && ./opa-gatekeeper 
```
- The scripts outputs the policy violations.