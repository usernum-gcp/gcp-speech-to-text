# Google Cloud Platform - Speech to Text with Python Library - Cloud Functions

This bunch of files are the functions to deploy in order to get the following flow:

[file uploaded to GCS] -> [Google Cloud Function] -> [Speech API] -> [JSON transcrition file into GCS]

This architecture is good only as long as the transcription takes less than 9 minutes (540 seconds)

## Creating the function

* Enable the relevant APIs
```
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable speech.googleapis.com
```

* Deploy the function 'gcf_speech_to_text' to be triggered upon object upload to [bucket-name]

The parameter [bucket-name] is the actual name of the bucket.  'gs://'' is NOT required.

The following will take a couple of minutes.
```
bash deploy_gcf.bash [bucket-name]
```

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