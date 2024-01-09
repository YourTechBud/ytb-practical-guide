# AutoGen DeepDive

> Consider giving this repo a ✨! Thanks!!!

Here's a link to the YouTube video explaining this setup in greater detail:

[![Querying Kubernetes using AutoGen](./thumbnail.png)](https://youtu.be/OdmyDGjNiCY)

## Prerequisites

You need to have the following tools installed:

- [Poetry](https://python-poetry.org/docs/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) Or [Racher Desktop](https://rancherdesktop.io/)
- [K3d](https://k3d.io/v5.6.0/)

## Environment Setup

### 1. Setup poetry & K8s Environment

```bash
# To setup poetry
poetry install

# To setup a k3d cluster
k3d cluster create --config k3d.config.yaml
```

### 2. Install Inferix (OpenAI compatible server)

- Make sure you have [Ollama](https://ollama.ai/) installed.
- Make sure you have pulled a model. I recommend [OpenHermes 2.5](https://ollama.ai/library/openhermes:7b-mistral-v2.5-q5_K_M).
- Use this [guide](https://github.com/YourTechBud/inferix) to setup the inference server locally. This supports function calling which most projects do not.

### 3. Run the AutoGen App

```bash
poetry run python src/main.py --prompt "give me all the pods"
```
