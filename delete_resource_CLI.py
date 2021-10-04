"""
......This scrpit is for deleting AWS resources by AWS CLI command......
"""
import os, boto3


def lambda_handler(event=None, context=None):
    def session_token():
        sts = boto3.client('sts')
        sts_response = sts.get_session_token(DurationSeconds=900)
        credentials = sts_response['Credentials']
        session = boto3.Session(
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )
        return session

    def delete_bucket():
        session = session_token()

        s3_resource = session.client('s3')
        response = s3_resource.list_buckets()
        bucket = response.get('Buckets', [])
        if (len(bucket) != 0):
            for bucket in response['Buckets']:
                if not bucket['Name'].startswith('ahad'):
                    print(f"..........Working on bucket: {bucket['Name']}..........")
                    os.system(f"aws s3 rb s3://{bucket['Name']} --force")
                    print(f"..........\"{bucket['Name']}\" --> Bucket is deleted..........")
                else:
                    print(f"*******\"{bucket['Name']}\" --> This bucket can not be deleted*******")
        else:
            print("*********No bucket found*********")
    
    delete_bucket()
    session_token()

lambda_handler()