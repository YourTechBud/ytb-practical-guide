cronscaler: {
	type: "trait"
	annotations: {}
	description: "Automatically scale the component based on CRON schedule."
	attributes: {
		appliesToWorkloads: ["deployments.apps", "statefulsets.apps"]
	}
}

template: {
	outputs: cronscaler: {
		metadata: name: context.name
		spec: {
			scaleTargetRef: {
				name:       context.name
			}
			triggers: [{
				type: "cron"
				metadata: {
					timezone: parameter.timezone
					start: parameter.start
					end: parameter.end
					desiredReplicas: parameter.desiredReplicas
				}
			}]
		}
		apiVersion: "keda.sh/v1alpha1"
		kind:       "keda.sh/v1alpha1"
	}

	parameter: {
		timezone: *"Asia/Kolkata" | string
		start: string
		end: string
		desiredReplicas: *"10" | string
	}
}