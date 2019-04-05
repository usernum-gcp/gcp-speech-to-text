#!/bin/bash

samplefile=0502112239_1_6397392588207366206_1_32.wav

echo "Using file: $samplefile"

if [ "$1" == "" ] ; then
	exit 1
else
	BUCKET=$1
fi

echo "bash deploy_gcf.bash ${BUCKET}"

bash deploy_gcf.bash $BUCKET

echo "gsutil cp $samplefile gs://${BUCKET}/wav/legal-services/"

gsutil cp $samplefile gs://${BUCKET}/wav/legal-services/

echo "sleep 12"
sleep 12

#https://cloud.google.com/sdk/gcloud/reference/beta/functions/logs/read
echo "gcloud beta functions logs read gcf_speech_to_text --limit 1000"
gcloud beta functions logs read gcf_speech_to_text --limit 1000