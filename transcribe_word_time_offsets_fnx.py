#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample that demonstrates word time offsets.

Example usage:
    python transcribe_word_time_offsets.py resources/audio.raw
    python transcribe_word_time_offsets.py \
        gs://cloud-samples-tests/speech/vr.flac
"""

import argparse, io, random, datetime, csv

def message(msg, level="Info"):
  logfile = '/tmp/speec-to-text.log'
  now = datetime.datetime.now()
  time =  now.isoformat()
  str = level + "|" + time + "|" + msg + "\n"
  with open(logfile, "a") as myfile:
    myfile.write(str)
    myfile.close()
  if (level == "Error"):
    print (str)

#return the largest number from the file name
#counting on '_' as separator
#if nothing is coming back - generating a random for an index

def extract_index_from_file_name(gcs_uri):

    return_value = random.randint(1,9223372036854775807)

    for part in gcs_uri.split('_'):
        if (part.isdigit()):
            number = int(part)
            if (number > 999999):
                return_value=number

    return return_value

def transcribe_file_with_word_time_offsets(speech_file,index):
    """Transcribe the given audio file synchronously and output the word time
    offsets."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types

    client = speech.SpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_word_time_offsets=True)

    response = client.recognize(config, audio)

    for result in response.results:
        alternative = result.alternatives[0]
        print(u'Transcript: {}'.format(alternative.transcript))

        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            print('Word: {}, start_time: {}, end_time: {}'.format(
                word,
                start_time.seconds + start_time.nanos * 1e-9,
                end_time.seconds + end_time.nanos * 1e-9))


# [START speech_transcribe_async_word_time_offsets_gcs]
def transcribe_gcs_with_word_time_offsets(gcs_uri, index=random.randint(1,9223372036854775807)):
    """Transcribe the given audio file asynchronously and output the word time
    offsets."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    import time

    #from google.cloud import speech_v1p1beta1 as speech

    client = speech.SpeechClient()

    timeout_seconds = 3600
    csv_file_name = str(index) + ".csv"
    metadata_csv_file_name = "meta_" + csv_file_name

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.MULAW,
        #sample_rate_hertz=16000,
        sample_rate_hertz=8000,
        language_code='he-IL',
        enable_word_time_offsets=True)
        #enable_speaker_diarization=True,
        #diarization_speaker_count=2)

    operation = client.long_running_recognize(config, audio)

    start = time.time()
    
    # need to update some status DB

    message('Waiting up to {} seconds for operation of file {} with call_id {} to complete...'.format(
        timeout_seconds, gcs_uri, index))
    
    result = operation.result(timeout=timeout_seconds)

    with open(csv_file_name, 'w') as csvfile:
            fieldnames = ['call_id', 'word', 'start_time','end_time','confidence']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in result.results:
                alternative = result.alternatives[0]
                for word_info in alternative.words:
                    word = word_info.word
                    start_time = word_info.start_time
                    end_time = word_info.end_time
                    message('call_id: {}, word: {}, start_time: {}, end_time: {}, confidence: {}'.format(
                    index,
                    word.encode('utf-8'),
                    start_time.seconds + start_time.nanos * 1e-9,
                    end_time.seconds + end_time.nanos * 1e-9,
                    alternative.confidence))

                    writer.writerow({'call_id': index, 'word': word.encode('utf-8'),
                        'start_time': start_time.seconds + start_time.nanos * 1e-9 ,
                    'end_time': end_time.seconds + end_time.nanos * 1e-9,
                    'confidence': alternative.confidence})

    end = time.time()
    elapsed_seconds = end - start

    #close(csv_file_name)

    message('Finished processing of file {}, with call_id {}, in {}, seconds. File is {}, seconds long. into {}'.format(
        gcs_uri,
        index,
        elapsed_seconds,
        end_time.seconds + end_time.nanos * 1e-9,
        csv_file_name))
    with open(metadata_csv_file_name, 'w') as csvfile:
            fieldnames = ['gcs_uri', 'call_id', 'processing_elapsed_seconds','call_length','csv_file_name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'gcs_uri': gcs_uri, 'call_id': index, 'processing_elapsed_seconds':elapsed_seconds,
                'call_length':end_time.seconds + end_time.nanos * 1e-9,'csv_file_name':csv_file_name})


    # need to update some status DB


# [END speech_transcribe_async_word_time_offsets_gcs]

def transcribe_file_with_diarization(gcs_uri, index=random.randint(1,9223372036854775807)):
    """Transcribe the given audio file synchronously with diarization."""
    # [START speech_transcribe_diarization_beta]
    from google.cloud import speech_v1p1beta1 as speech
    #from google.cloud.speech import enums
    #from google.cloud.speech import types
    import time

    timeout_seconds = 3600

    client = speech.SpeechClient()

    #speech_file = 'resources/commercial_mono.wav'

    #with open(speech_file, 'rb') as audio_file:
    #    content = audio_file.read()


    #audio = speech.types.RecognitionAudio(content=content)
    audio = speech.types.RecognitionAudio(uri=gcs_uri)

    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.MULAW,
        sample_rate_hertz=8000,
        language_code='he-IL',
        audio_channel_count=2,
        enable_separate_recognition_per_channel=True,
        #enable_speaker_diarization=True,
        #diarization_speaker_count=2
        )

    print('Waiting for operation to complete...')
    
    #operation = client.long_running_recognize(config, audio)
    operation = client.long_running_recognize(config, audio)


    # The transcript within each result is separate and sequential per result.
    # However, the words list within an alternative includes all the words
    # from all the results thus far. Thus, to get all the words with speaker
    # tags, you only have to take the words list from the last result:
    
    #result = operation.results[-1]
    result = operation.result(timeout=timeout_seconds)

    print result

    #words_info = result.alternatives[0].words
    #words_info = result.results.alternative[0]

    

    # Printing out the output:
    #for word_info in words_info:
    #    print("word: '{}', speaker_tag: {}".format(word_info.word.encode('utf-8'),
    #                                               word_info.speaker_tag))
    # [END speech_transcribe_diarization_beta]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    args = parser.parse_args()
    if args.path.startswith('gs://'):
        index=extract_index_from_file_name(args.path)
        transcribe_gcs_with_word_time_offsets(args.path,index)
        #transcribe_file_with_diarization(args.path)
    else:
        transcribe_file_with_word_time_offsets(args.path)


