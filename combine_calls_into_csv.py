#!/usr/bin/env python


# python3 process.py <input_file> <output_file>

import sys, random, csv, os, base64, uuid, hashlib


def parse_file(arg_in_file, arg_out_file):

	header = "call_id,transcription"

	in_file = open(arg_in_file,'r')
	out_file = open(arg_out_file,'w') 

	out_file.write(header + '\n')
	prev_id=''

	is_first = True
	out_line = ''

	for line in in_file.readlines():
		id,text = line.split(',')
		
		if (id == 'call_id'):
			pass
		elif (id == prev_id):
			out_line += text
		else:
			if (is_first):
				prev_id = id
				out_line += text.replace('\n', ' ')
				is_first = False
			else:
				new_line = out_line.replace('\n', ' ')
				out_line = new_line.replace('\r',' ')
				out_file.write(id + ',' + out_line + '\n')
				out_line = text.replace('\n', ' ')
				prev_id = id

if __name__ == '__main__':
    arg_in_file = sys.argv[1]
    arg_out_file = sys.argv[2]
    #arg_temp_file = '/tmp/tmp'+str(random.randint(1,9223372036854775807))+'.csv'
    
    parse_file(arg_in_file, arg_out_file)
  
    
    #os.remove(arg_temp_file)
    #remove_columns(arg_out_file + ".tmp", arg_out_file)
