#!/bin/bash

# THIS IS LOOKING FOR THE .out FILES 
# $1 will be the folder to look into

PROJECT_ID=name-speech2text
DATASET=name_speech_to_text_poc
TABLE=name_speech_to_text_poc_metadata
FOLDER=~/20190101/metadata/
SCRIPTS=~/scripts/

if [ "$#" -ne "0" ] ; then
	FOLDER=${1}	
fi

temp_file=/tmp/md$$
cat /dev/null > ${temp_file}

for i in `ls ${FOLDER}/ | grep '.txt'|grep -vi out`
do
   :
	cat ${i} >> ${temp_file}
done

python ${SCRIPTS}/process_metadata.py ${temp_file} ${temp_file}.out

bq rm -f -t ${PROJECT_ID}:${DATASET}.${TABLE}
header_to_filter="call_id|start_time|start_date|start_hour|end_time|duration|agent_id|extention|device|phone_number|dialed_in_number|direction|logger"

file=/tmp/tmpfile$$

cat ${temp_file}.out | grep -v ${header_to_filter} |sed '/^$/d'  > ${file}

cp ${file} /tmp/amit

bq load --source_format=CSV  --field_delimiter="|" ${PROJECT_ID}:${DATASET}.${TABLE} ${file} call_id:string,start_time:timestamp,start_date:date,start_hour:integer,end_time:timestamp,duration:float,agent_id:string,extention:string,device:string,phone_number:string,dialed_in_number:string,direction:string,logger:string

rm ${file}

