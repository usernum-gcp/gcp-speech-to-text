# Google Cloud Platform - Speech to Text with Python Library - Cloud Functions

This bunch of files are the functions to deploy in order to get the following flow:

[file uploaded to GCS] -> [Google Cloud Function] -> [Speech API] -> [JSON transcrition file into GCS]

This architecture is good only as long as the transcription takes less than 9 minutes (540 seconds)

This simple tutorial demonstrates writing, deploying, and triggering a Background Cloud Function 

The tutorial is based on [this](https://cloud.google.com/dataflow/docs/quickstarts/quickstart-templates
) and [this](https://codelabs.developers.google.com/codelabs/cpb101-bigquery-dataflow-streaming/index.html?index=..%2F..next17#0)

## Getting the repo
* From the cloud shell or any other terminal, get the repo with all code and scripts with the following command
```
git clone https://github.com/amiteinav/gcp-speechto-text.git
cd gcp-speech-to-text/gcf/
```

## Setting  Google Cloud BigQuery 
* From the cloud shell or any other terminal, Create the dataset and the table
```
bash bq_settings.bash
```

## Creating the Google Cloud Pub/Sub settings


## Creating the Google Cloud Dataflow settings (Using the Pub/Sub-to-BigQuery Template)
https://cloud.google.com/dataflow/docs/guides/templates/provided-templates#cloud-pubsub-to-bigquery

* Run the following command
```
bash df_settings.bash
```

## Creating the Google Cloud Function

* From the cloud shell or any other terminal, enable the relevant APIs
```
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable speech.googleapis.com
```

* From the cloud shell or any other terminal, deploy the function 'gcf_speech_to_text' to be triggered upon object upload to [bucket-name]. 'gs://'' is not required. just the name. 
```
bash deploy_gcf.bash [bucket-name]s
```
The script will take a couple of minutes.


## Logs of cloud functions
Check the functions logging this way:
```
gcloud beta functions logs read <FUNCTION_NAME> --execution-id EXECUTION_ID
```
example:
```
gcloud beta functions logs read gcf_speech_to_text 
```

## Testing code
while working on the gcf, you can use this to test deployment + file upload + watching the logs
```
bash test_gcf.bash $BUCKET_NAME
```