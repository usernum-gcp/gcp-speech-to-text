#!/usr/bin/env python

import json
 
def transcribe_file_with_diarization(gcs_uri):
    """Transcribe the given audio file synchronously with diarization."""
    # [START speech_transcribe_diarization_beta]
    from google.cloud import speech_v1p1beta1 as speech
    client = speech.SpeechClient()
 
    audio = speech.types.RecognitionAudio(uri=gcs_uri)
    config = speech.types.RecognitionConfig(
        language_code='en-IN',
        enable_speaker_diarization=True,
        diarization_speaker_count=2)
 
    operation = client.long_running_recognize(config, audio)
    
    print('Waiting for operation to complete...')
     
    response = operation.result(timeout=900)
 
    # Print to screen
    print(response)
 
    #Write to file
    f = open("response.json", "w")
    f.write(str(response))
 
# GCS file is public
transcribe_file_with_diarization('gs://amiteinav-sandbox/call-1-d791-5c4a663c-vcall-338949.wav')