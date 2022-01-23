## Prerequisites
- Clone this git repo `git clone git@github.com:YourTechBud/practical-guide.git`
- Change the directory to `cd how-to-get-started-with-kubernetes`


## Setting up your cluster

### Installing kubectl
```
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin
```

### Installing K3d cluster
```
wget -q -O - https://raw.githubusercontent.com/rancher/k3d/main/install.sh | bash
```

### Creating K3d cluster
```
k3d cluster list
```

```
k3d registry create --port 0.0.0.0:5000
```

```
k3d cluster create --config k3d-config.yaml
```

## Deploying our app

### Creating a pod
```
kubectl apply -f pod.yaml
```

```
kubectl get pods greeting-app
```

```
kubectl describe pods greeting-app
```

### Accessing shell of the container running inside the pod
```
kubectl run my-shell --rm -i --tty --image curlimages/curl:7.80.0 -- sh
```

```
curl http://your-pod-ip-address:8080/greeting/john
```

### Deleting a pod
```
kubectl delete pod greeting-app
```

## Exploring Deployments

### Creating a deployment
```
kubectl apply -f deployment.yaml
```

```
kubectl describe deployments greeting-app-deployment
```

## Service Discovery

### Creating a service
```
kubectl apply -f service.yaml
```

## Autoscaling

### Creating a HPA resource
```
kubectl apply -f hpa.yaml
```

### Watching status changes of pods
```
watch kubectl get pods
```
