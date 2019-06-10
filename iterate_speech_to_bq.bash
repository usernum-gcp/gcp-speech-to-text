#!/bin/bash

file=/tmp/tmpfile$$
cat /dev/null > ${file}


DATASET=$1
LOCAL_FOLDER=$2
TABLE=speech_to_text_word_by_word
PROJECT_ID=$(gcloud config get-value core/project)

for line in `ls -1 ${LOCAL_FOLDER} | grep csv | grep -v meta | grep -v transcript` ; do

	cat ${LOCAL_FOLDER}/$line | grep -v "call_id,word,start_time,end_time,confidence" >> ${file}

done

bq load --source_format=CSV   ${PROJECT_ID}:${DATASET}.${TABLE} ${file} call_id:integer,word,start_time:float,end_time:float,confidence:float

rm ${file}

exit