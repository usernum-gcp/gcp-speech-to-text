#!/usr/bin/env python

# pip install pydub --user

from os.path import splitext
from pydub import AudioSegment

def wav2flac(wav_path):
    flac_path = "%s.flac" % splitext(wav_path)[0]
    song = AudioSegment.from_wav(wav_path)
    song.export(flac_path, format = "flac")

if __name__ == "__main__":
    import sys
    print (sys.argv[1])
    wav2flac(sys.argv[1])