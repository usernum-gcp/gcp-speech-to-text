#!/bin/bash

for i in `gsutil ls -r gs://fnx-it-* | grep .wav` 
do
   : 
   echo $i
   python /home/amiteinav_google_com/gcp-speech-to-text/extract_NICE_input_to_csv.py $i &
   sleep 15
done
