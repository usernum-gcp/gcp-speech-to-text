#!/bin/bash

# This is the parameters settings file

export PROJECT_ID=$(gcloud config get-value core/project)
export DATASET_NAME=speech_to_text
export FULL_TRANSCRIPT_TABLE=full_transcript
export WORD_BY_WORD_TABLE=word_by_word
export TRANSCRIBE_FUNCTION_NAME=gcf_speech_to_text
export BUCKET=mimunnlp-poc-callcenter-1