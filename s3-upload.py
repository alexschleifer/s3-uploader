# Created by Alex Schleifer
# Tool to upload file to S3 bucket with external arguments
# Usage: python3 .\s3-upload.py --file /Users/My-user/Downloads/test-file.pdf --bucket my-bucket --path folder1/folder2/test.pdf
#
# Prerequisite : You  mast change Access/Secret key and region name of bucket


import logging
import boto3
from botocore.exceptions import ClientError
import os
import argparse

# Credentials
AWS_ACCESS_KEY_ID = "my_access_key"
AWS_SECRET_ACCESS_KEY = "my_secret_key"
AWS_REGION_NAME = "s3_bucket_region_name"


TAG = "uploaded_by = python script"


parser = argparse.ArgumentParser(
    description="S3 Uploader",
    prog='S3-uploader',
    epilog="You are using this program on Your own RISK! Be careful")

parser.add_argument('--version', action='version', version='%(prog)s v0.01')
parser.add_argument("-f","--file", help="file name include path for upload to S3")
parser.add_argument("-b","--bucket", help="Bucket name ")
parser.add_argument("-p","--path", help="file name include path inside S3 bucket, use '/' to create folders")

args = parser.parse_args()
print(args.file)

def upload_file(file_name, bucket, object_name=None, extra_args=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    # s3_client = boto3.client('s3')

    s3_client = boto3.client(service_name='s3', region_name=AWS_REGION_NAME,
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    try:
        response = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs={'Tagging': TAG})
    except ClientError as e:
        logging.error(e)
        return False
    return True

upload_file(args.file,args.bucket,args.path)