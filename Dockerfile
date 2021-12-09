FROM talend/datacatalog-remote-harvesting-agent:7.3-20211028
RUN useradd -ms /bin/bash  1001
USER 1001
