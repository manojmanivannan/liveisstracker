FROM manojmanivannan18/python-hellomaven:python
LABEL maintainer="ManojManivannan"

COPY entrypoint.sh /tmp/

###### Copy python package
COPY dist/${python_package}-${python_version}.tar.gz /tmp/
###### Install the python packages
RUN pip3 install --no-cache-dir /tmp/${python_package}-${python_version}.tar.gz
#RUN pip3 install --no-cache-dir https://github.com/matplotlib/basemap/archive/master.zip

RUN apt-get install -y supervisor

###### Remove the packages
RUN rm -rf /tmp/*.tar.gz

##### Copy the python folder into the docker container
# optionally create folder and copy the python project
# directory into a directory in container
# However using docker-compose we will mount the
# target/generated-sources/liveisstracker/liveisstracker into
# /home/manoj/liveisstracker
RUN mkdir -p /home/manoj/${python_package}
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
RUN chown manoj:manoj /var/log/supervisor/supervisord.log

# create a non-root user manoj
RUN useradd -d /home/manoj -m -s /bin/bash manoj && echo "manoj:manoj" | chpasswd && adduser manoj sudo
RUN chown -R manoj:manoj /home/manoj
USER manoj

###### Entrypoint srcipt

#Add Tini. TIni operates as a process subreaper for jupyter. This prevents kernel crahes
#ENV TINI_VERSION v0.6.0
#ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
#RUN chmod +x /usr/bin/tini
#ENTRYPOINT ["/usr/bin/tini","--"]

WORKDIR /home/manoj/${python_package}
EXPOSE 8501
# CMD ["python","track_iss.py"]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
