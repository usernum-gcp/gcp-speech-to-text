#!/usr/bin/env python

from google.cloud import storage
import os


def download_blob2(bucket_name, source_blob_name, destination_file_name):
	client = storage.Client()

	bucket = client.get_bucket(bucket_name)

	blob = bucket.get_blob('folder1/text.file')

	print (blob.download_as_string())

download_blob2('bucket-it-speech2text-in-poc-3',' ',' ')



