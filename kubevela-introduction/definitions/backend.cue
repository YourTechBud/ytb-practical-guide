backend: {
	annotations: {}
	attributes: workload: definition: {
		apiVersion: "apps/v1"
		kind:       "Deployment"
	}
	description: ""
	labels: {}
	type: "component"
}

template: {
	output: {
		spec: {
			selector: matchLabels: "app": context.name
			template: {
				metadata: labels: "app": context.name
				spec: containers: [{
					name:  context.name
					image: parameter.image
				}]
			}
		}
		apiVersion: "apps/v1"
		kind:       "Deployment"
	}
	outputs: {
		service: {
			metadata: name: context.name
			spec: {
				selector: "app": context.name
				ports: [{
					name: "http"
					port: parameter.port
				}]
				type: "ClusterIP"
			}
			apiVersion: "v1"
			kind:       "Service"
		}
	}
	parameter: {
		image: string
		port:  int
	}
}