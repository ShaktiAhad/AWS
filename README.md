# This repo is for playing around with different AWS resources(Lambda,SNS,cloudFormation,..)
## Useful links
* Create lambda layer: https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html
* Deployment package with dependencies in the same function: https://docs.aws.amazon.com/lambda/latest/dg/python-package.html#python-package-create-package-with-dependency
* AWS CLI layer creation: https://bezdelev.com/hacking/aws-cli-inside-lambda-layer-aws-s3-sync/

## Lambda layer creation:
### Lambda layer creation from Mac terminal:
1. Create a folder: mkdir -p python/lib/python3.9/site-packages
2. Install the dependency: pip3 install <Dependency_Name> --target python/lib/python3.9/site-packages
3. Zip the folder: zip -r <File_Name>.zip ./python  

### Lambda layer zip file creation on local
* Execute the **AWS-CLI-lambda-layer.py** for AWS Cli
* Execute the **xlsWriter-lambda-layer.py** for xlsWriter

### Script description
* **delete_resource_boto3.py**: Delete AWS resources by using python boto3 SDK.
* **delete_resource_CLI.py**: Delete AWS resources by using AWS Command. *Must use AWS CLI lambda layer*.
* **list-resource-SMTP.py**: Create an Excel file of AWS resources and send the file to email by SMTP server.
* **list-resource-SNS.py**: Create an Excel file of AWS resources, Put the file in S3 and send the file location by SNS.
* **miscellaneous-test.py**: Small code test.
* **lambda-role-policy-function.yaml**: CloudFormation template to create Lambda Role, Policy, Function(*Resource-deletion*).
* **lambda-resource-list-function.yaml**: CloudFormation template to create Lambda Function(*AWS Resource containing Excel File*). ***index.py** contain the Lambda Function code. Zip it(*zip -r index.zip index.py*) and upload to S3 bucket.*
