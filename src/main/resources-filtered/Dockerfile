FROM manojmanivannan18/python-hellomaven:python
MAINTAINER ManojManivannan


###### Copy python package
COPY dist/${python_package}-${python_version}.tar.gz /tmp/
###### Install the python package
RUN pip3 install --no-cache-dir /tmp/${python_package}-${python_version}.tar.gz
#RUN pip3 install --no-cache-dir https://github.com/matplotlib/basemap/archive/master.zip
RUN apt-get update && apt-get install -y procps

###### Remove the packages
#RUN rm -rf /tmp/*.tar.gz

##### Copy the python folder into the docker container
# optionally create folder and copy the python project
# directory into a directory in container
# However using docker-compose we will mount the
# target/generated-sources/liveisstracker/liveisstracker into
# /home/manoj/liveisstracker
RUN mkdir -p /home/manoj/${python_package}


# create a non-root user manoj
RUN useradd -d /home/manoj -m -s /bin/bash manoj && echo "manoj:manoj" | chpasswd && adduser manoj sudo
COPY ${python_package} /home/manoj/${python_package}/
RUN chown -R manoj:manoj /home/manoj/*
#USER manoj


#Add Tini. TIni operates as a process subreaper for jupyter. This prevents kernel crahes
ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini","-s","--"]



WORKDIR /home/manoj/${python_package}

###### Entrypoint srcipt
COPY entrypoint.sh /tmp/entrypoint.sh
RUN chmod +x /tmp/entrypoint.sh
RUN chown -R manoj:manoj /tmp/entrypoint.sh



RUN chown -R manoj:manoj /home/manoj
USER manoj
EXPOSE 8501
CMD ["/tmp/entrypoint.sh"]
