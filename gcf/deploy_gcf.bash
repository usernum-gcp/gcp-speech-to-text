#!/bin/bash

if [ "$1" == "" ] ; then
	exit 1
else
	BUCKET=$1
fi

gcloud beta functions deploy gcf_speech_to_text\
 --runtime python37 \
--trigger-resource $BUCKET \
--trigger-event google.storage.object.finalize