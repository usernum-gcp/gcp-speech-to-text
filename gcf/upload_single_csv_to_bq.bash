#!/bin/bash

source params.bash

#curr_file=gs://mimunnlp-poc-callcenter-1/transcripts/raw/i6397392588207366206p0502112239t.csv
curr_file=/Users/amiteinav/Documents/GitHub/gcp-speech-to-text/gcf/6397392588207366206.csv

#bq load --source_format=CSV ${PROJECT_ID}:${DATASET}.${FULL_TRANSCRIPT_TABLE} $curr_file call_id:string,phone_number:string,transcript:string

bq load --source_format=CSV --skip_leading_rows=1  ${PROJECT_ID}:${DATASET}.${WORD_BY_WORD_TABLE} $curr_file  \
call_id:string,word,start_time:float,end_time:float,confidence:float 

