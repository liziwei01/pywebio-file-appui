#version 1.0
FROM python3:latest
LABEL maintainer="alssylk@gmail.com"
RUN ["mkdir", "-p", "/home/liziwei01/OpenSource/github.com/liziwei01/pywebio-file-appui"]
WORKDIR /home/liziwei01/OpenSource/github.com/liziwei01/pywebio-file-appui
COPY . /home/liziwei01/OpenSource/github.com/liziwei01/pywebio-file-appui
CMD ["/home/liziwei01/OpenSource/github.com/liziwei01/pywebio-file-appui/docker_run"] 
