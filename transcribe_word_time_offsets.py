#!/usr/bin/env python

"""
Example usage:
    
    python transcribe_word_time_offsets.py -f resources/audio.raw -l 'en-US' -e 'FLAC'
    
    python transcribe_word_time_offsets.py -u gs://cloud-samples-tests/speech/vr.flac -l 'he-IL' -e 'FLAC'

    options for -e option : MULAW / FLAC / LINEAR16

    there is -i index that means the number of field in the filename to use as name
    01101015000_20190602_002640_230561.wav with -i 2 means : 002640 is the index

"""

from google.cloud import speech
#from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech import enums
#from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech import types
#from google.cloud.speech_v1p1beta1 import types

import time, argparse, io, random, datetime, csv,sys,getopt


def message(msg, level="Info"):
  logfile = '/tmp/transcribe_word_time_offset.log'
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

def extract_index_from_file_name(gcs_uri,index=0):

    return_value = random.randint(1,9223372036854775807)

    for part in gcs_uri.split('_'):
        if (index == 0):
            if (part.isdigit()):
                number = int(part)
                if (number > 999999):
                    return_value=number
        else
            index = index - 1 

    return return_value

def transcribe_file_with_word_time_offsets(speech_file,index,language='en-US'):
    """Transcribe the given audio file synchronously and output the word time
    offsets."""
    

    client = speech.SpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language,
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
def transcribe_gcs_with_word_time_offsets(
    gcs_uri, 
    index=random.randint(1,9223372036854775807),
    language='en-US',
    enable_speaker_diarization=False,
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16):
    """Transcribe the given audio file asynchronously and output the word time
    offsets."""
    

    #from google.cloud import speech_v1p1beta1 as speech

    message ('now working on {} with language {}'.format(gcs_uri,language))

    client = speech.SpeechClient()

    timeout_seconds = 3600
    csv_file_name = str(index) + ".csv"
    metadata_csv_file_name = "meta_" + csv_file_name
    transcript_file_name = "transcript_" + csv_file_name
    speaker_file_name = "speaker_"  + csv_file_name

    audio = types.RecognitionAudio(uri=gcs_uri) 
    config = types.RecognitionConfig(
        #encoding=enums.RecognitionConfig.AudioEncoding.MULAW,
        encoding=encoding,
        #sample_rate_hertz=16000,
        #sample_rate_hertz=8000,
        language_code=language,
        enable_word_time_offsets=True)
        #enable_speaker_diarization=enable_speaker_diarization,
        #diarization_speaker_count=2)
        #model='phone_call')
        #use_enhanced=True)
        #diarization_speaker_count=2)

    message ('running {}'.format(config))

    operation = client.long_running_recognize(config, audio)

    start = time.time()
    
    # need to update some status DB

    message('Waiting up to {} seconds for operation of file {} with call_id {} to complete...'.format(
        timeout_seconds, gcs_uri, index))
    
    result = operation.result(timeout=timeout_seconds)

    with open(csv_file_name, 'w') as csvfile, open (transcript_file_name,'w') as csvfile2:
            fieldnames = ['call_id', 'word', 'start_time','end_time','confidence']
            fieldnames2 = ['transcript']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer2 = csv.DictWriter(csvfile2, fieldnames=fieldnames2)
            writer.writeheader()
            writer2.writeheader()
            for result in result.results:
                alternative = result.alternatives[0]
                writer2.writerow({'transcript': alternative.transcript.encode('utf-8')})
                for word_info in alternative.words:
                    word = word_info.word
                    start_time = word_info.start_time
                    end_time = word_info.end_time
                    #speaker = word_info.speaker_tag
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
        enable_separate_recognition_per_channel=True
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

    print (result)

    #words_info = result.alternatives[0].words
    #words_info = result.results.alternative[0]

    

    # Printing out the output:
    #for word_info in words_info:
    #    print("word: '{}', speaker_tag: {}".format(word_info.word.encode('utf-8'),
    #                                               word_info.speaker_tag))
    # [END speech_transcribe_diarization_beta]


def main(argv):
    message ('Started a run ---')
    is_local = False
    is_gcs = False 
    index_extract_required=False
    enable_speaker_diarization=False
    speaker_csv_index=0
    langauge = 'en-US'
    url=''
    filepath=''
    fname_index=0
    encoding=enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED

    try:
        opts, args = getopt.getopt(argv,"f:l:u:de:s:i:")
    except getopt.GetoptError:
        sys.exit(42)
    for opt, arg in opts:
        if opt == "-f":
            filepath = arg
            is_local = True
        elif opt == "-l":
            language = arg
        elif opt == "-i":
            fnname_index-arg
        elif opt == "-u":
            is_gcs = True
            url = arg
        elif opt == "-d":
            enable_speaker_diarization=True
        elif opt == "-e":
            if (arg == "MULAW"):
                encoding=enums.RecognitionConfig.AudioEncoding.MULAW
            elif (arg == "FLAC"):
                encoding=enums.RecognitionConfig.AudioEncoding.FLAC
            elif (arg == "LINEAR16")
                encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16
            else:
                encoding=enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED
        elif opt == '-s':
            speaker_csv_index = arg

    print "Hello"


    index=extract_index_from_file_name(url,fname_index)
    
    message('now with index {} is_local {} is_gcs {}'.format(index,is_local,is_gcs))

    if (is_local):
        transcribe_file_with_word_time_offsets(filepath,index,language,enable_speaker_diarization,encoding)
    elif (is_gcs):
        transcribe_gcs_with_word_time_offsets(url,index,language,enable_speaker_diarization,encoding)


if __name__ == "__main__":
    script_name=sys.argv[0]
    arguments = len(sys.argv) - 1

    if (arguments == 0):
        sys.exit(42)

    main(sys.argv[1:])

