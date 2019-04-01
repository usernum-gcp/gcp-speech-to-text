# Google Cloud Platform - Speech to Text with Python Library - Cloud Functions

This bunch of files are the functions to deploy in order to get the following flow:

[file uploaded to GCS] -> [Google Cloud Function] -> [Speech API] -> [JSON transcrition file into GCS]

This architecture is good only as long as the transcription takes less than 9 minutes (540 seconds)

## creating the function

<bucket-name> is the actual name, no gs:// is required
```
bash deploy_gcf.bash <bucket-name>
```

