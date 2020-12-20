FROM alpine:latest
RUN apk add --no-cache busybox-initscripts mongodb-tools bash
COPY ./cronjob /etc/crontabs/root
COPY ./backup /usr/local/bin/
CMD ["crond", "-f", "-d", "8"]