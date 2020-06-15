#!/bin/bash

file=/tmp/tmpfile$$
cat /dev/null > ${file}


DATASET=$1
LOCAL_FOLDER=$2
TABLE=$3
PROJECT_ID=$(gcloud config get-value core/project)

for line in `ls -1 ${LOCAL_FOLDER} | grep csv | grep transcript_ |  grep "\.csv"` ; do
    sed 1d $line >> ${file}
done

bq load --source_format=CSV   ${PROJECT_ID}:${DATASET}.${TABLE} ${file} call_id:integer,transcript

rm ${file}

exit