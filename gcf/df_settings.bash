#!/bin/bash

gcloud dataflow jobs run JOB_NAME \
    --gcs-location gs://dataflow-templates/latest/PubSub_to_BigQuery \
    --parameters \
inputTopic=projects/YOUR_PROJECT_ID/topics/YOUR_TOPIC_NAME,\
outputTableSpec=YOUR_PROJECT_ID:YOUR_DATASET.YOUR_TABLE_NAME