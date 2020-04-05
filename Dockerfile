FROM centos
MAINTAINER ray <zengyanren@foxmail.com>

RUN mkdir /home/project
ENV DOCKER_PROJECT /home/project
#COPY ./ ./
#RUN pip install -r requirements.txt

#安装python3.6.5
RUN yum -y install wget && \
        yum -y install openssl-devel && \
        yum -y install bzip2-devel && \
        yum -y install expat-devel &&\
        yum -y install gdbm-devel &&\
        yum -y install readline-devel &&\
        yum -y install sqlite-devel &&\
        yum -y install make &&\
        yum -y install gcc &&\
        yum -y groupinstall "fonts" &&\
        export LC_ALL=en_US.utf8

WORKDIR $DOCKER_PROJECT
RUN wget http://cdn.npm.taobao.org/dist/python/3.6.5/Python-3.6.5.tgz && \
        tar -xzvf Python-3.6.5.tgz && \
        cd Python-3.6.5 && \
        ./configure --prefix=/usr/local && \
        make && \
        make altinstall && \
        rm /usr/bin/python && \
        ln -s /usr/local/bin/python3.6 /usr/bin/python && \
        ln -s /usr/local/bin/python3.6 /usr/bin/python3 &&\
        ln -s /usr/local/bin/pip3.6 /usr/bin/pip

RUN sed '1c #!/usr/bin/python2' -i /bin/yum && \
        sed '1c #!/usr/bin/python2' -i /bin/yum-config-manager && \
        sed '1c #!/usr/bin/python2' -i /bin/yum-debug-restore && \
        sed '1c #!/usr/bin/python2' -i /bin/yumdownloader && \
        sed '1c #!/usr/bin/python2' -i /bin/yum-builddep && \
        sed '1c #!/usr/bin/python2' -i /bin/yum-debug-dump && \
        sed '1c #!/usr/bin/python2' -i /bin/yum-groups-manager && \
        sed '1c #!/usr/bin/python2' -i /usr/libexec/urlgrabber-ext-down

WORKDIR $DOCKER_PROJECT

COPY ./requirements.txt ./
RUN pip install --default-timeout=100 --trusted-host=mirrors.aliyun.com --upgrade pip &&\
    pip install -r requirements.txt --default-timeout=100 --trusted-host=mirrors.aliyun.com -i https://mirrors.aliyun.com/pypi/simple/&&\
    rm requirements.txt

# RUN pip install -r requirement.txt
EXPOSE 8080
EXPOSE 7070

#执行权限
#RUN chmod u+x entrypoint.sh
#容器启动后要执行的命令
#ENTRYPOINT ["./entrypoint"]
