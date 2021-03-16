FROM alpine:latest
RUN apk add --no-cache busybox-initscripts mongodb-tools bash
RUN mkdir -p /etc/periodic/6h
COPY ./backup /etc/periodic/6h/
RUN echo "0 0 * * * run-parts /etc/periodic/6h >> /var/opt/backups/backup.log 2>&1" >> /etc/crontabs/root