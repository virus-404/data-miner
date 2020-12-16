FROM alpine:latest
WORKDIR /usr/local/bin
COPY . ./
RUN apk add --no-cache bash tini openrc busybox-initscripts  
RUN ./startup.sh 
ENTRYPOINT [ "./entrypoint.sh" ]