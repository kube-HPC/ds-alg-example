import os
import boto3
from boto3.session import Session
from botocore.exceptions import ClientError, ParamValidationError

DEFAULT_ACCESS_KEY = 'AKIAIOSFODNN7EXAMPLE'
DEFAULT_SECRET_KEY = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
DEFAULT_S3_ENDPOINT_URL = 'http://127.0.0.1:9000'
DEFAULT_LOCAL_STORAGE_PATH = './localStoragePath'

class S3Session(object):
    
    def __init__(self, backetname):

        # YEHIAM:
        key = os.getenv('AWS_ACCESS_KEY_ID', DEFAULT_ACCESS_KEY)
        secret = os.getenv('AWS_SECRET_ACCESS_KEY', DEFAULT_SECRET_KEY)
        s3EndpointUrl = os.getenv('S3_ENDPOINT_URL', DEFAULT_S3_ENDPOINT_URL)
        self._localStoragePath = os.getenv('LOCAL_STORAGE_PATH', DEFAULT_LOCAL_STORAGE_PATH)
        if not os.path.exists(self._localStoragePath):
            os.makedirs(self._localStoragePath)
        if s3EndpointUrl:
            try:
                s3_client_session = boto3.session.Session(
                    aws_access_key_id=key,
                    aws_secret_access_key=secret,
                )
                s3_client = s3_client_session.resource(
                    service_name='s3',
                    endpoint_url=s3EndpointUrl
                    )
                print('s3 init to ',s3EndpointUrl)
                self._bucket = s3_client.Bucket(backetname)
            except ClientError as e:
                res = e.response
                outMessage = {'command': 'errorMessage', 'data': res}
                print(outMessage)
                return None
        else:
            print('s3 not init')


    def download(self, filename):
        try:
            localfilename = os.path.join(self._localStoragePath, filename)
            self._bucket.download_file(filename, localfilename)
        except ClientError as e:
                res = e.response
                outMessage = {'command': 'errorMessage', 'data': res}
                print(outMessage)
                return None
        # except ParamValidationError as e:
        #     print("Parameter validation error: %s" % e)
        # except ClientError as e:
        #     print("Unexpected error: %s" % e)

        return localfilename

    def upload(self, filename: str):
        try:
            path = filename.split('/')
            key = path[-1]
            self._bucket.upload_file(filename, key)
            return key
        except ClientError as e:
            res = e.response
            outMessage = {'command': 'errorMessage', 'data': res}
            print(outMessage)
            return None
