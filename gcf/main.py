# Copyright 2018, Google, LLC.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# [START gcf_speech_to_text]
def gcf_speech_to_text(data, context):
    """Background Cloud Function to be triggered by Cloud Storage.
       This generic function logs relevant data when a file is changed.

    Args:
        data (dict): The Cloud Functions event payload.
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to Stackdriver Logging
    """

    print('Event ID: {}'.format(context.event_id))
    print('Event type: {}'.format(context.event_type))
    print('Bucket: {}'.format(data['bucket']))
    print('File: {}'.format(data['name']))
    print('Metageneration: {}'.format(data['metageneration']))
    print('Created: {}'.format(data['timeCreated']))
    print('Updated: {}'.format(data['updated']))

    #from google.cloud import speech_v1p1beta1 as speech
    #import time
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types


    timeout_seconds = 500
    client = speech.SpeechClient()

    gcs_uri="gs://"+data['bucket']+"data['name']"

    audio = types.RecognitionAudio(uri=gcs_uri) 
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.MULAW,
        #sample_rate_hertz=16000,
        #sample_rate_hertz=8000,
        language_code=he-IL,
        enable_word_time_offsets=True,
        enable_speaker_diarization=enable_speaker_diarization,
        diarization_speaker_count=2)
        #model='phone_call')
        #use_enhanced=True)
        #diarization_speaker_count=2)

    operation = client.long_running_recognize(config, audio)

    result = operation.result(timeout=timeout_seconds)



# [END gcf_speech_to_text]
