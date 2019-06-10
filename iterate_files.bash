#!/bin/bash

# bash iterate_files.bash GS_PATH FTYPE LANG
# bash iterate_files.bash gs://example/speech flac he-IL DST_FOLDER

GS_PATH=$1
FTYPE=$2
LANG=$3
DST_FOLDER=$4

TRANSCRIBE_PY=${HOME}/gcp-speech-to-text/transcribe_word_time_offsets.py

mkdir -p ${DST_FOLDER}
cd ${DST_FOLDER}

for i in `gsutil ls -r $GS_PATH | grep -i ${FTYPE}`
do
   : 
   echo "Now Handling $i"
   echo "python ${TRANSCRIBE_PY} -u $i -l '${LANG}' -i -e $2  "

done
