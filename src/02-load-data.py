#!/usr/bin/env python

import os
from minio import Minio
from minio.error import S3Error

print("#TODO")
print("Extract, Transform, and Load your data")

def upload_to_s3(bucket, source_filename, destination_filename):

    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        endpoint = os.getenv("AWS_S3_ENDPOINT", "minio:9000").lstrip("http://"), 
        access_key = os.getenv("AWS_ACCESS_KEY_ID"), 
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
        secure = False
    )

    # Create a bucket if it does not exist.
    found = client.bucket_exists(bucket)

    if not found:
        print(f"Using Endpoint: {os.getenv('AWS_S3_ENDPOINT')}")
        print(f"Attempting to create bucket: {bucket}")
        client.make_bucket(bucket)
    else:
        print(f"Bucket {bucket} already exists")

    try:
        client.fput_object(bucket, source_filename, destination_filename)

    except S3Error as err:
        print(err)

if __name__ == "__main__":
    upload_to_s3('data', 'IBM.csv', 'stock/IBM.csv')
