"""
......This scrpit is for creating AWS resources list in excel format -> upload file to S3 -> send "key" by SNS......
Documentation:
boto3: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Bucket.upload_file
sns: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Client.publish
datetime: https://www.w3schools.com/python/python_datetime.asp
Lambda functions with .zip: https://docs.aws.amazon.com/lambda/latest/dg/python-package.html
"""
import xlsxwriter, boto3, datetime

all_resources={}
def lambda_handler(event=None, context=None):
    def resrc_func():

        ###..For S3..
        s3_resource = boto3.client('s3')
        bucket_response = s3_resource.list_buckets()
        buckets = bucket_response.get('Buckets', [])
        if (len(buckets) != 0):
            s3=[]
            for bucket in buckets:
                if not bucket['Name'].startswith("ahad"):
                    s3.append(bucket['Name'])
                all_resources["s3"] = s3
            print("______S3 bucket found______")
        else:
            print("______No S3 bucket found______")

        ###..EC2..
        ec2_resource = boto3.client('ec2')
        ec2_response = ec2_resource.describe_instances()
        ec2_instances = ec2_response.get('Reservations', [])
        if (len(ec2_instances) != 0):
            ec2 =[]
            for reservation in ec2_response["Reservations"]:
                for instance in reservation["Instances"]:
                    ec2.append(instance["InstanceId"])
                all_resources["ec2"] = ec2
            print ("______EC2 Instance found______")
        else:
            print ("______No EC2 Instance found______")

        ###..Lambda_Function..
        lambda_resource = boto3.client('lambda')
        lambda_response = lambda_resource.list_functions()
        lambda_instances = lambda_response.get('Functions', [])
        if (len(lambda_instances) != 0):
            lmbda =[]
            for function in lambda_response['Functions']:
                lmbda.append(function['FunctionName'])
            all_resources["lambda"] = lmbda
            print ("______Lambda Function found______")
        else:
            print ("______No Lambda Function found______")

    today = datetime.datetime.today().strftime("%d-%b-%Y")
    def excel_file():
        workbook = xlsxwriter.Workbook(f'/tmp/AWS_Resources_list_{today}.xlsx')
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})

        i=0
        row = 0
        col = 0
        while(i<len(all_resources)):
            worksheet.write(row, col, "Resource name", bold)
            worksheet.write(row, col+1, "No of resources", bold)
            for key,value in all_resources.items():
                worksheet.write(row+1, col, key)
                worksheet.write(row+1, col+1, len(value))
                row+=1
                i+=1
        
        j=0
        while(j<len(all_resources)):
            for key,value in all_resources.items():
                row = len(all_resources)
                worksheet.write(row+2, col+j, key, bold)
                for v in value:
                    worksheet.write(row+3, col+j, v)
                    row+=1
                j+=1

        workbook.close()
        print (f"______Excel file: AWS_Resources_list_{today}.xlsx is created______") 

    def upload_file():
        s3_client = boto3.resource('s3')
        s3_client.Bucket('ahad-test-3').upload_file(Filename=f'/tmp/AWS_Resources_list_{today}.xlsx', Key=f'resources/AWS_Resources_list_{today}.xlsx')
        print ("______Uploaded file to s3 bucket: ahad-test-3______")
    

    def sns ():
        sns_client = boto3.client('sns')
        sns_message = str(f"Please check the Excel file and delete unnecessary resources. It helps us to reduce AWS cost. \n\n File path: s3://ahad-test-3/resources/AWS_Resources_list_{today}.xlsx \n\n Thank you.")
        subject= "AWS Resource list"
        sns_client.publish(
                TopicArn='arn:aws:sns:ap-northeast-1:450454010996:test-sns-lambda',
                Message= str(sns_message),
                Subject= str(subject)
        )
        print ("______Email sent______")
    resrc_func()
    excel_file()
    upload_file()
    sns()

lambda_handler()
