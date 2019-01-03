#!/bin/bash

PROJECT_ID=fnx-speech2text
DATASET=fnx_speech_to_text_poc
TABLE=fnx_speech_to_text_poc_loading_stats
FOLDER="~/20190101/upload_stats/"

if [ "$#" -ne "0" ] ; then
	FOLDER=${1}	
fi

bq rm -f -t ${PROJECT_ID}:${DATASET}.${TABLE}

file=/tmp/tmpfile$$

cat ${FOLDER}*.csv | grep -v "gcs_uri,call_id,processing_elapsed_seconds,call_length,csv_file_name" > ${file}

bq load --source_format=CSV  ${PROJECT_ID}:${DATASET}.${TABLE} ${file} gcs_uri,call_id:integer,processing_elapsed_seconds:float,call_length:float,csv_file_name

rm ${file}

