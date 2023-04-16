# Kubevela Introduction

## Prerequisites

- You'll need to have [KubeVela](https://github.com/kubevela/kubevela/releases) installed.

## Steps To Reproduce The Video

Just run the following commands to generate the output files.

```bash
vela dry-run -f app-basic.yaml --offline -d ./definitions
vela dry-run -f app-hpa.yaml --offline -d ./definitions
vela dry-run -f app-keda.yaml --offline -d ./definitions
```