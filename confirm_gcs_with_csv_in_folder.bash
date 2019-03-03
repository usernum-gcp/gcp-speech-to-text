#!/bin/bash

if [ "${1}" != "" ] ;  then
	path=${1} 
else
	path='gs://bucket-it-*'
fi

list_of_csv=`ls | grep csv`
list_of_gsutil=`gsutil ls -r  ${path}  | grep .wav |  awk -F"_" '{print $3}'`
for i in ${list_of_gsutil}
do
   : 
   
#echo "Checking ${i}"
	grep ${i} ${list_of_csv} > /dev/null 
   if [ $? -ne 0 ] ; then
   	echo "${i} not found"
	#gsutil ls -lrh ${i}
   fi
done
