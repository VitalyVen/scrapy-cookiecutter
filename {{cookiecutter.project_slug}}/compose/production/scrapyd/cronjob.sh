#! /bin/bash
set -e
declare -p | grep -Ev 'BASHOPTS|BASH_VERSINFO|EUID|PPID|SHELLOPTS|UID' > /opt/scrapyd/container.env
echo "* * * * * BASH_ENV=/container.env curl http://scrapyd:6800/schedule.json -d project=crawler -d spider=spider" > /etc/cron.d/scrapyd
service cron start
crontab /etc/cron.d/scrapyd
