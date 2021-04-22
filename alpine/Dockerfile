FROM alpine:latest
RUN apk add --no-cache busybox-initscripts mongodb-tools bash
RUN mkdir -p /etc/periodic/24h
COPY ./backup /etc/periodic/24h/
RUN echo "0 0 * * * run-parts /etc/periodic/24h >> /var/opt/backups/backup.log 2>&1" >> /etc/crontabs/root