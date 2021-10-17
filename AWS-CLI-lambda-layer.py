"""
......This scrpit is for creating AWS CLI layer......
Documentation: https://bezdelev.com/hacking/aws-cli-inside-lambda-layer-aws-s3-sync/
"""
import os

os.system(
    '''
    echo "python3 version": $(python3 --version)
    echo "pip3 version": $(pip3 --version)
    echo "virtualenv version": $(virtualenv --version)

    # Automatically detects python version (only works for python3.x)
    export PYTHON_VERSION=`python3 -c 'import sys; version=sys.version_info[:3]; print("{0}.{1}".format(*version))'`
    export VIRTUAL_ENV_DIR="awscli-virtualenv"              # Temporary directory for the virtual environment
    export LAMBDA_LAYER_DIR="awscli-lambda-layer"           # Temporary directory for AWS CLI and its dependencies
    export ZIP_FILE_NAME="awscli-lambda-layer.zip"          # The zip file that will contain the layer

    mkdir ${VIRTUAL_ENV_DIR}                                # Creates a directory for virtual environment
    virtualenv ${VIRTUAL_ENV_DIR}                           # Initializes a virtual environment in the virtual environment directory
    cd ${VIRTUAL_ENV_DIR}/bin/                              # Changes current dir to the virtual env directory
    source activate                                         # Activate virtual environment
    pip3 install awscli                                     # Install AWS CLI in the virtual environment
    sed -i '' "1s/.*/\#\!\/var\/lang\/bin\/python/" aws     # replace the path to Python in the aws executable path
    deactivate                                              # Deactive virtualenv

    cd ../..                                                # Changes current directory back to where it started
    mkdir ${LAMBDA_LAYER_DIR}                               # Creates a temporary directory to store AWS CLI and its dependencies
    cd ${LAMBDA_LAYER_DIR}                                  # Changes the current directory into the temporary directory
    cp ../${VIRTUAL_ENV_DIR}/bin/aws .                      # Copies aws and its dependencies to the temp directory
    cp -r ../${VIRTUAL_ENV_DIR}/lib/python${PYTHON_VERSION}/site-packages/ .
    zip -r ../${ZIP_FILE_NAME} *                            # Zips the contents of the temporary directory
    cd ..                                                   # Goes back to where it started
    rm -r ${VIRTUAL_ENV_DIR}                                # Removes virtual env and temp directories
    rm -r ${LAMBDA_LAYER_DIR}                               # Removes virtual env and temp directories
    pwd                                                     # Current folder location
    ls -al | grep awscli-lambda-layer.zip                   # Check the zip file availability
    mv awscli-lambda-layer.zip ~/Desktop                    # Move the zip file to Desktop
    echo ".............Check the file:${ZIP_FILE_NAME} on your Desktop............."
    '''
)
