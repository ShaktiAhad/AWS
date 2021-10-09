## I wasn’t able to send email using Gmail username/password. I made following changes to make it work.

## Create password for external App(In our case `Lambda function`)
Got to [Google Account Security](https://myaccount.google.com/security) and Scroll down to **"Signing in to Google"** option. If you don't have 2 step verification on; enable it. Then you will see **"App passwords"** option. Generate a password for your lambda function. 
* ***Make sure to copy the Password else you will not be able to copy it later.*** 

## Sample lambda function in python to check SMTP server
I have used following code to verify my SMTP server is working. 
```
import smtplib, os

def lambda_handler(event=None, context=None):
    sender = os.getenv("SENDER")
    receiver = os.getenv("RECEIVER")
    password = os.getenv("PASSWORD")
    host = os.getenv("SMTPHOST")
    port = os.getenv("SMTPPORT")

    try:
        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg="Subject: Test\n\n This is a test from lambda")
        server.close()
        return True
    except Exception as ex:
        print (ex)
        return False

lambda_handler()
```
## Send attachment using SMTP server
***As I have used xlsWriter module to create Excel file, I had to create a lambda layer for that. First I will explain how I created the lambda layer.***

### xlsWriterlambda layer creation:
Create a file `xlsWriter.py` on your local `~/Desktop` path and copy/paste the following command. It will create  `xlswriter.zip` file on your Desktop. 
```   
"""
......This scrpit is for creating xlsWriter lambda layer......
"""
import os

os.system(
    '''
    echo ".............All good! Ready to go!............."
    export ZIP_FILE_NAME="xlswriter.zip" 
    cd ~/Desktop
    mkdir -p python/lib/python3.9/site-packages
    pip3 install XlsxWriter --target ~/Desktop/python/lib/python3.9/site-packages
    zip -r xlswriter.zip ./python 
    echo ".............Check the file:${ZIP_FILE_NAME} on your Desktop............."
    '''
)
```
After creating the zip file use following steps to upload file and create the layer. 
1. Login to your AWS account
2. Got to **Lambda** service 
3. Click **Layers** under **Additional resources** from left plane 
4. Click **Create layer** 
5. Put a name for lambda layer 
6. Upload the `xlswriter.zip` file.
7. Copy the **ARN** from the top right corner. We need the ARN to use the lambda layer in our lambda function. 

*There are some other fields such as *Description*, *Compatible architectures*, *Compatible runtimes*, etc. These are ***optionals****.

### Sample lambda function in python to send an attachment:
* **Lambda function creation and add the lambda layer**:

1. Create a lambda function `SMTP_attachment_lambda`.
2. Under **Function Overview**, Click **Layers** option just below the function name.
3. Click **Add Layer**.
4. Choose **Specify An ARN** option paste the layer ARN in the blank field.
5. Click **verify** then **Add**.
* **Make sure you create the excel file in `/tmp` folder. Else you will get following error `"errorMessage": "[Errno 30] Read-only file system: '/hello.xlsx'"`**
* **Also you need to create `__init.py__` file. Else you will get lots of following error `"File \"<frozen importlib._bootstrap>\"`**
* **Lambda Folder tree**:
```
SMTP_attachment_lambda
├── __init.py__
└── lambda_function.py
```
* **Code**:
``` 
import smtplib, os, xlsxwriter
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def lambda_handler(event=None, context=None):
    
    # Create an Excel File
    workbook = xlsxwriter.Workbook('/tmp/hello.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Hello world')
    workbook.close()
    
    # Attach Excel file and send
    sender = os.getenv("SENDER")
    receiver = os.getenv("RECEIVER")
    password = os.getenv("PASSWORD")
    host = os.getenv("SMTPHOST")
    port = os.getenv("SMTPPORT")

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "Test_email"
    text = """
        This is a test email with an excel file attached. 

        Regards,
        Lambda
    """
    msg.attach(MIMEText(text))
    with open('/tmp/hello.xlsx', 'rb') as file:
            part = MIMEApplication(file.read())
            part.add_header('Content-Disposition',f'attachment; filename={os.path.basename("hello.xlsx")}')
            msg.attach(part)


    try:
        smtp = smtplib.SMTP(host=host, port=port)
        smtp.starttls()
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        print("Success: Email has been sent")
    except Exception:
        print("Error: Unable to send email")
        raise Exception


lambda_handler()
```
