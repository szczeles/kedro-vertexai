# Configuration

Plugin maintains the configuration in the `conf/base/vertexai.yaml` file. Sample configuration can be generated using `kedro vertexai init`:

```yaml
# Configuration used to run the pipeline
project_id: my-gcp-mlops-project
region: europe-west1
run_config:
  # Name of the image to run as the pipeline steps
  image: eu.gcr.io/my-gcp-mlops-project/example_model:${commit_id}

  # Pull policy to be used for the steps. Use Always if you push the images
  # on the same tag, or Never if you use only local images
  image_pull_policy: IfNotPresent

  # Location of Vertex AI GCS root
  root: bucket_name/gcs_suffix

  # Name of the kubeflow experiment to be created
  experiment_name: MyExperiment

  # Name of the scheduled run, templated with the schedule parameters
  scheduled_run_name: MyExperimentRun

  # Optional pipeline description
  #description: "Very Important Pipeline"

  # How long to keep underlying Argo workflow (together with pods and data
  # volume after pipeline finishes) [in seconds]. Default: 1 week
  ttl: 604800

  # What Kedro pipeline should be run as the last step regardless of the
  # pipeline status. Used to send notifications or raise the alerts
  # on_exit_pipeline: notify_via_slack

  # Optional section allowing adjustment of the resources
  # reservations and limits for the nodes
  resources:

    # For nodes that require more RAM you can increase the "memory"
    data_import_step:
      memory: 2Gi

    # Training nodes can utilize more than one CPU if the algoritm
    # supports it
    model_training:
      cpu: 8
      memory: 1Gi

    # GPU-capable nodes can request 1 GPU slot
    tensorflow_step:
      nvidia.com/gpu: 1

    # Default settings for the nodes
    __default__:
      cpu: 200m
      memory: 64Mi
```

## Dynamic configuration support

`kedro-vertexai` contains hook that enables [TemplatedConfigLoader](https://kedro.readthedocs.io/en/stable/kedro.config.TemplatedConfigLoader.html).
It allows passing environment variables to configuration files. It reads all environment variables following `KEDRO_CONFIG_<NAME>` pattern, which you 
can later inject in configuration file using `${name}` syntax. 

This feature is especially useful for keeping the executions of the pipelines isolated and traceable by dynamically setting output paths for intermediate data in the **Data Catalog**, e.g.

```yaml
# ...
train_x:
  type: pandas.CSVDataSet
  filepath: gs://<bucket>/kedro-vertexai/${run_id}/05_model_input/train_x.csv

train_y:
  type: pandas.CSVDataSet
  filepath: gs://<bucket>/kedro-vertexai/${run_id}/05_model_input/train_y.csv
# ...
```

In this case, the `${run_id}` placeholder will be substituted by the unique run identifier from Vertex AI Pipelines.

There are two special variables `KEDRO_CONFIG_COMMIT_ID`, `KEDRO_CONFIG_BRANCH_NAME` with support specifying default when variable is not set, 
e.g. `${commit_id|dirty}`   

### Disabling dynamic configuration hook
In current Kedro versions (`<=0.18`) [only single configuration hook can be attached](https://github.com/kedro-org/kedro/blob/0.17.7/kedro/framework/hooks/specs.py#L304), which means if your project had a custom one, this plug-in will most likely overwrite it. You can disable this plugin's configuration hook by setting environment variable `KEDRO_VERTEXAI_DISABLE_CONFIG_HOOK` to `true`, e.g.:
```bash
export KEDRO_VERTEXAI_DISABLE_CONFIG_HOOK=true
```
Once set, the plugin will provide a clear warning with a reminder:
```
KEDRO_VERTEXAI_DISABLE_CONFIG_HOOK environment variable is set and EnvTemplatedConfigLoader will not be used which means formatted config values like ${run_id} will not be substituted at runtime
```

To make plugin-compatible custom config loader you can extend the class `kedro_vertexai.context_helper.EnvTemplatedConfigLoader` and register your own hook.