#!/bin/bash

PROJECT_ID=$1
DATASET=$2
LOCAL_FOLDER=$3
TABLE=speech_to_text_loading_stats

# bash iterate_load_stats_to_bq.bash ${PROJECT_ID} ${DATASET} ${LOCAL_FOLDER} 

bq rm -f -t ${PROJECT_ID}:${DATASET}.${TABLE}

file=/tmp/tmpfile$$

cat ${LOCAL_FOLDER}/meta_*.csv | grep -v "gcs_uri,call_id,processing_elapsed_seconds,call_length,csv_file_name" > ${file}

bq load --source_format=CSV  ${PROJECT_ID}:${DATASET}.${TABLE} ${file} gcs_uri,call_id:integer,processing_elapsed_seconds:float,call_length:float,csv_file_name

rm ${file}

