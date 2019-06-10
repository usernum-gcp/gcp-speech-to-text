#!/bin/bash

# bash iterate_files.bash GS_PATH FTYPE LANG
# bash iterate_files.bash gs://example/speech flac he-IL

GS_PATH=$1
FTYPE=$2
LANG=$3

TRANSCRIBE_PY=${HOME}/gcp-speech-to-text/transcribe_word_time_offsets.py

for i in `gsutil ls -r $GS_PATH | grep -i ${FTYPE}`
do
   : 
   echo "Now Handling $i"
   echo "python ${TRANSCRIBE_PY} -u $i -l '${LANG}' -i -e $2  "

done
