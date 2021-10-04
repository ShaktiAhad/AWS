"""
......This scrpit is for creating xlsWriter lambda layer......

"""
import os

os.system(
    '''
    if [[ $(pip3 --version) != "command not found" ]];
    then
        echo ".............All good! Ready to go!............."
        export ZIP_FILE_NAME="xlswriter.zip" 
        cd ~/Desktop
        mkdir -p python/lib/python3.9/site-packages
        pip3 install XlsxWriter --target ~/Desktop/python/lib/python3.9/site-packages
        zip -r xlswriter.zip ./python 
        echo ".............Check the file:${ZIP_FILE_NAME} on your Desktop............."
    else
        if [ $(pip3 --version)  != "command not found" ];
        then
            echo "pip3is installed on your machine": $(python3 --version)
        else
            echo "pip3 is not installed on your machine use '"brew install pip3"'"
        fi 
    fi

    '''
)