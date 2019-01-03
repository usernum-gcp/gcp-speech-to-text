#!/bin/bash

file=/tmp/tmpfile$$

cat *.csv | grep -v "call_id,word,start_time,end_time,confidence,sentence" > ${file}

bq load --source_format=CSV   fnx-speech2text:fnx_speech_to_text_poc.fnx_speech_to_text_poc_facts ${file} call_id,word,start_time:float,end_time:float,confidence:float,sentence:string

rm ${file}

#bq load --source_format=CSV --skip_leading_rows=1  fnx-speech2text:fnx_speech_to_text_poc.fnx_speech_to_text_poc_facts ${file} call_id,word,start_time:float,end_time:float,confidence:float,sentence:string

exit

for i in `ls -1 * | grep ".csv"` 
do
   : 
   echo $i
	bq load --source_format=CSV --skip_leading_rows=1  fnx-speech2text:fnx_speech_to_text_poc.fnx_speech_to_text_poc_facts ${i} call_id,word,start_time:float,end_time:float,confidence:float  
 
done
