# KFP Tekton

## Issues

The pipeline service does not allow the setup of non secure s3 endpoints by default

```
spec:
  objectStorage:
    externalStorage:
      secure: false
```

```
oc patch DataSciencePipelinesApplication \
  pipelines-definition \
  --type merge \
  --patch '{"spec":{"objectStorage":{"externalStorage":{"secure": false }}}}'
```

## Setup samples

```
# Set up the python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the kfp-tekton SDK
pip install kfp-tekton
```

Non working example

```
curl -sL https://raw.githubusercontent.com/kubeflow/kfp-tekton/master/samples/trusted-ai/trusted-ai.py \
  sed 's@minio-service.kubeflow:9000@minio:9000@g' > trusted-ai.py
python trusted-ai.py
oc apply -f trusted-ai.yaml
```

## Links

- [KFP Tekton Samples](https://github.com/kubeflow/kfp-tekton/tree/master/samples)
