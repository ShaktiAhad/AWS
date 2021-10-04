# This repo is for creating different AWS resources(Lambda,SNS,cloudFormation,..)
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
