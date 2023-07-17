# Predicting stock prices using Long Short-Term Memory (LSTM)

## Prerequisites

- An Openshift 4.11+ cluster
- Object storage (minio)
- The Openshift Pipelines Operator
- The `oc` and `tkn` command line tools (See the question mark menu in the Openshift UI)

### Files and directories

```
├── src                             Python source for data ingestion and model training
├── pipelines                       Tekton pipeline and tasks 
├── notebooks                       Jupyter experimentation
└── requirements.txt                Python dependencies
```

### Pipeline example

Login to Openshift with `oc`

Install RHODS and OpenShift-Pipelines Operator

```
# install operators
oc apply -k components/operators
```

Install Demo components

```
# install demo components
oc apply -k components/demo
```

### Create a worker container image

```
tkn pipeline start build-worker-image \
  -w name=shared-workspace,claimName=pipeline \
  --use-param-defaults
```

### Start a pipeline run

Replace the `S3_ACCESS_KEY_ID`, `S3_SECRET_ACCESS_KEY`, and `S3_ENDPOINT` values.

```
tkn pipeline start ingest-and-train \
  -w name=shared-workspace,claimName=pipeline \
  --use-param-defaults
```

### Optional: Auto-create a pvc when starting the pipeline

This method requires further investigation as the PVCs don't get deleted when the pipeline gets deleted.

```
tkn pipeline start ingest-and-train \
  -w name=shared-workspace,volumeClaimTemplateFile=components/demo/pipelines/pvc.yaml \
  --use-param-defaults
```

### TODOs

- Split build pipeline and training pipeline

### References

[Data streamer sample](https://github.com/redhat-na-ssa/ml_data_streamer/blob/main/source-eip/src/test/resources/samples/MUFG-1.csv)

[Custom Notebook Builder](https://github.com/redhat-na-ssa/rhods-custom-notebook-example.git)

[Pipeline examples](https://github.com/rh-datascience-and-edge-practice/kubeflow-examples/blob/main/pipelines/11_iris_training_pipeline.py)
