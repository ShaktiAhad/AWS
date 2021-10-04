"""
......This scrpit is for creating AWS resources list in excel format and send by email......
"""
import smtplib, os, xlsxwriter, boto3
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

all_resources={}

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

def resrc_func():
    session = session_token()

    ###..For S3..
    s3_resource = session.client('s3')
    bucket_response = s3_resource.list_buckets()
    buckets = bucket_response.get('Buckets', [])
    if (len(buckets) != 0):
        s3=[]
        for bucket in buckets:
            if not bucket['Name'].startswith("ahad"):
                s3.append(bucket['Name'])
            all_resources["s3"] = s3
    else:
        print("______No S3 bucket found______")

    ###..EC2..
    ec2_resource = session.client('ec2')
    ec2_response = ec2_resource.describe_instances()
    ec2_instances = ec2_response.get('Reservations', [])
    if (len(ec2_instances) != 0):
        ec2 =[]
        for reservation in ec2_response["Reservations"]:
            for instance in reservation["Instances"]:
                ec2.append(instance["InstanceId"])
            all_resources["ec2"] = ec2
    else:
        print ("______No EC2 Instance found______")

    ###..Lambda_Function..
    lambda_resource = session.client('lambda')
    lambda_response = lambda_resource.list_functions()
    lambda_instances = lambda_response.get('Functions', [])
    if (len(lambda_instances) != 0):
        lmbda =[]
        for function in lambda_response['Functions']:
            lmbda.append(function['FunctionName'])
        all_resources["lambda"] = lmbda
    else:
        print ("______No Lambda Function found______")


def excel_file():
    workbook = xlsxwriter.Workbook('AWS_Resources_list.xlsx')
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

def send_email():
    SENDER_EMAIL_ADDRESS = 'xxxxxx@gmail.com'
    RECEIVER_EMAIL_ADDRESS = 'yyyyyy@gmail.com'
    PASSWORD = input(str('Enter your password: '))
    HOST = 'smtp.gmail.com'
    PORT = 587

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL_ADDRESS
    msg['To'] = RECEIVER_EMAIL_ADDRESS
    msg['Subject'] = "Test_email"
    text = """
        This is a test email with an excel file attached. 

        Regards
        Shakti
    """
    msg.attach(MIMEText(text))
    with open('AWS_Resources_list.xlsx', 'rb') as file:
            part = MIMEApplication(file.read())
            part.add_header('Content-Disposition',f'attachment; filename={os.path.basename("AWS_Resources_list.xlsx")}')
            msg.attach(part)


    try:
        smtp = smtplib.SMTP(host=HOST, port=PORT)
        smtp.starttls()
        smtp.login(SENDER_EMAIL_ADDRESS, PASSWORD)
        smtp.sendmail(SENDER_EMAIL_ADDRESS, RECEIVER_EMAIL_ADDRESS, msg.as_string())
        print("Success: Email has been sent")
    except Exception:
        print("Error: Unable to send email")
        raise Exception


resrc_func()
excel_file()
send_email()