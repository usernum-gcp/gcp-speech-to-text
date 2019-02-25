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
1. **Transcribe_word_time_offsets.py**

   This is for transcribing local or gcs voice files.
   The script creates two files
     a. a CSV with word per line 
     b. a CSV with statistics how long it took to create the file and other metadata 


### Creating metadata 
1. **extract_NICE_input_to_csv.py**
   This is for converting the NICE metadata into a meaningful CSV

2. **combine_calls_into_csv.py**
   This is for combining all calls into a single CSV - for a single upload to BigQuery

3. **iterate_files.bash**
   This is for rounding up files and preparing for an upload one-ny-one into BigQuery

4. **iterate_load_stats_to_bq.bash**
   This is for uploading individual statistics files into BigQuery

5. **iterate_metadata_to_bq.bash**
   This is to upload the metadata files into BigQuery

6. **iterate_speech_to_bq.bash**
   This is to upload the CSVs with the transcriptions into BigQuery

### Other files
The rest of the files you will see in this folder are work in progress or just references to other possiblities in working with the SDK.

## Identifying postal code
There are cases when you might want to identify a postal code in the transcription.
For that you should iterate through the sentences transcribed and look for patterns. 
if you are not going to use DLP API, that can identfiy more than postal codes, you should clean spaces between numbers and then run some regular expressions. [here](https://stackoverflow.com/questions/578406/what-is-the-ultimate-postal-code-and-zip-regex) is a cool starting point
