#!/bin/bash

source params.bash

echo "Using file: $samplefile"

if [ "$1" != "" ] ; then
	BUCKET=$1
fi

echo "bash deploy_gcf.bash ${BUCKET}"
bash deploy_gcf.bash $BUCKET

echo "gsutil cp $samplefile gs://${BUCKET}/wav/legal-services/"
gsutil cp $samplefile gs://${BUCKET}/wav/legal-services/

echo "sleep 60"
sleep 60

#https://cloud.google.com/sdk/gcloud/reference/beta/functions/logs/read
echo "gcloud beta functions logs read ${TRANSCRIBE_FUNCTION_NAME} --limit 50"
gcloud beta functions logs read ${TRANSCRIBE_FUNCTION_NAME} --limit 50