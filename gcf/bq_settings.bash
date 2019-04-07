#!/bin/bash

source params.bash

bq ls -a --format=csv ${PROJECT_ID}:${DATASET} 2>&1 > /dev/null
if [ $? -ne 0 ] ; then
	echo "${PROJECT_ID}:${DATASET} does not exist. creating it"
	bq mk ${PROJECT_ID}:${DATASET}
else
	echo "${PROJECT_ID}:${DATASET} exists"
fi

bq show ${PROJECT_ID}:${DATASET}.${FULL_TRANSCRIPT_TABLE} 2>&1 > /dev/null
if [ $? -ne 0 ] ; then
	echo "Table ${PROJECT_ID}:${DATASET}.${FULL_TRANSCRIPT_TABLE} does not exist. need to be created"
	bq mk \
	--time_partitioning_field timestamp \
	--schema \
timestamp:timestamp,\
call_id:string,\
phone_number:string,\
transcript:string \
	 -t ${DATASET}.${FULL_TRANSCRIPT_TABLE}

else
	echo "Table ${PROJECT_ID}:${DATASET}.${FULL_TRANSCRIPT_TABLE} already exists"

fi

bq show ${PROJECT_ID}:${DATASET}.${WORD_BY_WORD_TABLE} 2>&1 > /dev/null
if [ $? -ne 0 ] ; then
	echo "Table ${PROJECT_ID}:${DATASET}.${WORD_BY_WORD_TABLE} does not exist. need to be created"

	bq mk \
	--time_partitioning_field timestamp \
	--schema \
	timestamp:timestamp,\
call_id:string,\
phone_number:string,\
word:string,\
start_time:float,\
end_time:float,\
confidence:float \
	-t ${DATASET}.${WORD_BY_WORD_TABLE}
else
		echo "Table ${PROJECT_ID}:${DATASET}.${WORD_BY_WORD_TABLE} already exists"
fi

gcloud pubsub topics list | grep ${WORD_BY_WORD_TOPIC} 2>&1 > /dev/null
if [ $? -ne 0 ] ; then

	echo "Now adding the pubsub topic ${WORD_BY_WORD_TOPIC}"
	gcloud pubsub topics create ${WORD_BY_WORD_TOPIC}
else
	echo "Pubsub topic ${WORD_BY_WORD_TOPIC} already exists"

fi

gcloud pubsub topics list | grep ${FULL_TRANSCRIPT_TOPIC} 2>&1 > /dev/null
if [ $? -ne 0 ] ; then

	echo "Now adding the pubsub topic ${FULL_TRANSCRIPT_TOPIC}"
	gcloud pubsub topics create ${FULL_TRANSCRIPT_TOPIC}
else
	echo "Pubsub topic ${FULL_TRANSCRIPT_TOPIC} already exists"

fi

gcloud dataflow jobs list | grep ${WORD_BY_WORD_JOB} 2>&1 > /dev/null
if [ $? -ne 0 ] ; then
	gcloud dataflow jobs run ${WORD_BY_WORD_JOB} \
    --gcs-location gs://dataflow-templates/latest/PubSub_to_BigQuery \
    --max-workers 1 \
    --region ${DF_REGION} \
    --parameters \
	inputTopic=projects/${PROJECT_ID}/topics/${WORD_BY_WORD_TOPIC},\
outputTableSpec=${PROJECT_ID}:${DATASET}.${WORD_BY_WORD_TABLE}
else
	echo "dataflow job ${WORD_BY_WORD_JOB} already exists"
fi

gcloud dataflow jobs list | grep ${FULL_TRANSCRIPT_JOB} 2>&1 > /dev/null
if [ $? -ne 0 ] ; then
	gcloud dataflow jobs run ${FULL_TRANSCRIPT_JOB} \
    --gcs-location gs://dataflow-templates/latest/PubSub_to_BigQuery \
    --max-workers 1 \
    --region ${DF_REGION} \
    --parameters \
	inputTopic=projects/${PROJECT_ID}/topics/${FULL_TRANSCRIPT_TOPIC},\
outputTableSpec=${PROJECT_ID}:${DATASET}.${FULL_TRANSCRIPT_TABLE}
else
	echo "dataflow job ${FULL_TRANSCRIPT_JOB} already exists"

fi


