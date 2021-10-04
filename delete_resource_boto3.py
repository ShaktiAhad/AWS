"""
......This scrpit is for deleting AWS resources by Python sdk(boto3)......
......Documnetation......
boto3: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/index.html
Token: get_session_token
S3: list_buckets, list_objects, delete_objects, delete_bucket
......Documnetation......

"""
import boto3


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

    def bucket():
        session = session_token()

        client= session.client('s3')
        response = client.list_buckets()
        if (len(response['Buckets']) != 0):
            for bucket in response['Buckets']:
                if not bucket['Name'].startswith('ahad'):
                    print(f"..........Working on bucket: {bucket['Name']}..........")
                    objects = client.list_objects(Bucket=bucket['Name'])
                    content = objects.get('Contents', [])
                    if (len(content) != 0):
                        updated_content = []
                        for cont in content:
                            new_cont = cont['Key']
                            cont.clear()
                            cont['Key'] = new_cont
                            updated_content.append(cont) 
                        print(f"..........Deleting objects under bucket: {bucket['Name']}..........")
                        client.delete_objects(Bucket=bucket['Name'], Delete={'Objects':updated_content})
                    client.delete_bucket(Bucket=bucket['Name'])
                    print(f"..........\"{bucket['Name']}\" --> Bucket is deleted..........")
                else:
                    print(f"*******\"{bucket['Name']}\" --> This bucket can not be deleted*******")
        else:
            print("*********No bucket found*********")
        
    session_token()
    bucket()
        
lambda_handler()
