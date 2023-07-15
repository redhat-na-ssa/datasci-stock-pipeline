#!/usr/bin/env python

import os
from minio import Minio
from minio.error import S3Error

print("#TODO")
print("Extract, Transform, and Load your data")

def upload_to_s3(bucket, local_path, bucket_path):
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        endpoint=os.getenv("AWS_S3_ENDPOINT").lstrip("http://"),
        access_key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        secure=False,
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
        print(f"Pushing {local_path} to {bucket}/{bucket_path}")
        client.fput_object(bucket, bucket_path, local_path)

    except S3Error as err:
        print(err)


if __name__ == "__main__":
    # upload_to_s3("data", "../data/IBM.csv", "stock/IBM.csv")
    upload_to_s3("data", "../data/IBM-sample.csv", "stock/IBM-sample.csv")
