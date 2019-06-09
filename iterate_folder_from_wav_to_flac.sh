#!/bin/bash

# bash iterate_gcs_folder_from_wav_to_flac.sh gs://folder 

for file in `ls $1` ; do
	echo "python wav_to_flac.py $file"
	python wav_to_flac.py ${1}${file}
	done
