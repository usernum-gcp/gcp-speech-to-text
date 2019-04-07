#!/bin/bash

source params.bash

if [ "$1" != "" ] ; then
	BUCKET=$1	
fi

gcloud beta functions deploy ${TRANSCRIBE_FUNCTION_NAME} \
--runtime python37 \
--trigger-resource $BUCKET \
--trigger-event google.storage.object.finalize

