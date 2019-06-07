#!/usr/bin/env python

import time, argparse, datetime, csv,sys,getopt

'''
	-f <file-name> # which file to check
	-o <output-file-name> # send output to a tsv file: filename\tlength-in-seconds

'''

def get_wav_length2(filename):
	import scipy.io.wavfile as wav
	file_path = "/path/to/yourfile.wav"
	(source_rate, source_sig) = wav.read(file_path)
	duration_seconds = len(source_sig) / float(source_rate)


def get_wav_length(filename):
	import wave
	import contextlib
	fname = filename
	with contextlib.closing(wave.open(fname,'r')) as f:
		frames = f.getnframes()
		rate = f.getframerate()
		return ( frames / float(rate) )

def main(argv):

	got_output_file = False
	try:
		opts, args = getopt.getopt(argv,"f:o:")
	except getopt.GetoptError:
		sys.exit(42)

	for opt, arg in opts:
		if opt == "-f":
			filepath = arg
			is_local = True
		elif opt == "-o": 
			output_file = arg
			got_output_file = True

	string = filepath + '\t' + str(get_wav_length2(filepath))

	if (got_output_file):
		with open(output_file, "a") as myfile:
			myfile.write(string)
			myfile.close()

	print string



if __name__ == "__main__":
    script_name=sys.argv[0]
    arguments = len(sys.argv) - 1

    if (arguments == 0):
        sys.exit(42)

    main(sys.argv[1:])

