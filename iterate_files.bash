#!/bin/bash

for i in `gsutil ls -p fnx-speech2text gs://fnx-it-speech2text-poc-1/ | grep -i ".wav"`
do
   : 
   ls $i
done
