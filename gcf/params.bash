#!/usr/bin/env bash

# This is the parameters settings file

export PROJECT_ID=$(gcloud config get-value core/project)
export DATASET=speech_to_text_poc
export FULL_TRANSCRIPT_TABLE=full_transcript
export WORD_BY_WORD_TABLE=word_by_word
export TRANSCRIBE_FUNCTION_NAME=gcf_speech_to_text
export BUCKET=mimunnlp-poc-callcenter-1
export samplefile=0502112239_1_6397392588207366206_1_32.wav
export WORD_BY_WORD_TOPIC=word-by-word-topic
export FULL_TRANSCRIPT_TOPIC=full-transcript-topic
export WORD_BY_WORD_JOB=word-by-word-df-job
export FULL_TRANSCRIPT_JOB=full-transcript-df-job
export DF_REGION=europe-west1
