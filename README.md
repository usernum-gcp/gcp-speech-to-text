# gcp-speech-to-txt

This rep is to help ramping up while working with the Google Cloud Speech to Text python sdk 

## Reference documentation

1. [Cloud Speech-to-Text Documentation](https://cloud.google.com/speech-to-text/docs/)
2. [Python reference](https://cloud.google.com/speech-to-text/docs/reference/libraries#client-libraries-install-python)

## What is in here

This repository is supposed to help with starting off at the right foot with the following:
1. Transcribing voice
2. Uploading results to bigquery

### Transcribing Voice
**Transcribe_word_time_offsets.py**

   This is for transcribing local or gcs voice files.
   The script creates two files
     a. a CSV with word per line 
     b. a CSV with statistics how long it took to create the file and other metadata 


### Creating metadata 
1. process.py
This   