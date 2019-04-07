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


def send_to_pubsub(topic_name,data,project_id):
    from google.cloud import pubsub


    publisher = pubsub.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)
    data = data.encode('utf-8')
    future = publisher.publish(topic_path, data=data)
    print ('Published {} of message ID {}.'.format(data, future.result()))


# [START storage_upload_file]
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""

    from google.cloud import storage 

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))
# [END storage_upload_file]

def extract_call_id_from_file_name(gcs_uri):
    import random

    path=gcs_uri.split('_')

    if (len(path) == 5 ):
        #[phone-number]_#[number]_#[call-id]_#[number]_#[number].wav
        call_id=path[2]
    else:
        call_id=random.randint(1,9223372036854775807)


    return call_id 

def extract_phone_number_from_file_name(gcs_uri):
    import random

    path=gcs_uri.split('_')

    if (len(path) == 5 ):
        #[phone-number]_#[number]_#[call-id]_#[number]_#[number].wav
        phone_number=path[0].split('/')[-1]
    else:
        phone_number=random.randint(1,9223372036854775807)


    return  phone_number 

# [START gcf_speech_to_text]

def check_if_wav(filename):
    if (filename.split('.')[-1] == "wav"):
        return True
    else:
        return False

def gcf_speech_to_text(data, context):
    """Background Cloud Function to be triggered by Cloud Storage.
       This generic function logs relevant data when a file is changed.

    Args:
        data (dict): The Cloud Functions event payload.
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to Stackdriver Logging
    """
    print('---------')
    print('Event ID: {}'.format(context.event_id))
    print('Event type: {}'.format(context.event_type))
    print('Bucket: {}'.format(data['bucket']))
    print('File: {}'.format(data['name']))
    print('Metageneration: {}'.format(data['metageneration']))
    print('Created: {}'.format(data['timeCreated']))
    print('Updated: {}'.format(data['updated']))

    if (not check_if_wav(data['name'])):
        print ("This is not a wav file, therefore skipping handling this")
        return 0
    else:
        print ("transcribing..")
        transcribe_wav_file(data,context)


def transcribe_wav_file(data,context):

    ## Should be an environment variable!
    project_id="mimunnlp"

    gcs_uri="gs://"+data['bucket']+'/'+data['name']

    print(gcs_uri)

    index=extract_call_id_from_file_name(gcs_uri)
    phone_number=extract_phone_number_from_file_name(gcs_uri)

    
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    import csv
    import json
    import datetime


    timeout_seconds = 550
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri) 
    config = types.RecognitionConfig(
        #encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        #sample_rate_hertz=16000,
        #sample_rate_hertz=8000,
        language_code='he-IL',
        enable_word_time_offsets=True
        #enableSpeakerDiarization=True,
        #enableWordTimeOffsets=True
        #diarizationSpeakerCount=2
        )

    operation = client.long_running_recognize(config, audio)

    csv_file_name="/tmp/"+"i"+index+"p"+phone_number+"w.csv"
    transcript_file_name="/tmp/"+"i"+index+"p"+phone_number+"t.csv"

    result = operation.result(timeout=timeout_seconds)

    #wbw_data =[]
    #t_data = []
    ts=datetime.datetime.utcnow().isoformat()

    with open(csv_file_name, 'w') as csvfile, open (transcript_file_name,'w') as csvfile2:
        fieldnames = ['call_id', 'phone_number','word', 'start_time','end_time','confidence']
        fieldnames2 = ['call_id', 'phone_number', 'transcript']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer2 = csv.DictWriter(csvfile2, fieldnames=fieldnames2)
        writer.writeheader()
        writer2.writeheader()
        transcripter=" "
        for result in result.results:
            alternative = result.alternatives[0]
            transcripter=str(transcripter)+" "+str(alternative.transcript.encode('utf-8'))
            for word_info in alternative.words:
                word = word_info.word
                start_time = word_info.start_time
                end_time = word_info.end_time
                writer.writerow({'call_id': index, 'phone_number': phone_number,'word': word.encode('utf-8'),
                        'start_time': start_time.seconds + start_time.nanos * 1e-9 ,
                    'end_time': end_time.seconds + end_time.nanos * 1e-9,
                    'confidence': alternative.confidence})

                jsontxt = "{"
                jsontxt = jsontxt+"\"timestamp\":\"" + str(ts)+"\""
                jsontxt = jsontxt+",\"call_id\":\""+str(index)+"\""
                jsontxt = jsontxt+",\"phone_number\":\""+str(phone_number)+"\""
                jsontxt = jsontxt+",\"word\":\""+str(word.encode('utf-8'))+"\""
                jsontxt = jsontxt+",\"start_time\":\""+str(start_time.seconds+start_time.nanos*1e-9)+"\""
                jsontxt = jsontxt+",\"end_time\":\""+str(end_time.seconds + end_time.nanos * 1e-9)+"\""
                jsontxt = jsontxt+",\"confidence\":\""+str(alternative.confidence)+"\""
                jsontxt = jsontxt+"}"

                send_to_pubsub("word-by-word-topic",jsontxt,project_id)

                '''
                wbw_data.append({'timestamp':ts,'call_id': index, 'phone_number': phone_number,'word': word.encode('utf-8'),
                        'start_time': start_time.seconds + start_time.nanos * 1e-9 ,
                    'end_time': end_time.seconds + end_time.nanos * 1e-9,
                    'confidence': alternative.confidence})
                '''
        writer2.writerow({'call_id': index, 'phone_number': phone_number, 'transcript': transcripter})
        #t_data.append({'timestamp':ts, 'call_id': index, 'phone_number': phone_number, 'transcript': transcripter})
        
        jsontxt = "{"
        jsontxt = jsontxt+"'timestamp':'" + str(ts)+"'"
        jsontxt = jsontxt+",'call_id':'"+str(index)+"'"
        jsontxt = jsontxt+",'phone_number':'"+str(phone_number)+"'"
        jsontxt = jsontxt+",'transcript':'"+str(transcripter)+"'"
        jsontxt = jsontxt+"}"

        send_to_pubsub("full-transcript-topic",jsontxt,project_id)

    ## topics should be envrioinment variables!
    #send_to_pubsub("word-by-word-topic",wbw_data,project_id)
    #send_to_pubsub("full-transcript-topic",t_data,project_id)

    #print (t_data)
    #print (wbw_data)

    word_by_word_file="transcripts/raw/"+"i"+index+"p"+phone_number+"w.csv"
    transcript_file="transcripts/raw/"+"i"+index+"p"+phone_number+"t.csv"

    upload_blob(data['bucket'], csv_file_name, word_by_word_file)
    upload_blob(data['bucket'], transcript_file_name, transcript_file)
    



# [END gcf_speech_to_text]
