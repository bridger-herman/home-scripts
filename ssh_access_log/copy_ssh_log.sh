#!/usr/bin/bash


LOG_SRC="/var/log/auth.log"
LOG_DST="/home/be/ha_config/auth.log"
FILTER_PATTERN="sshd"

echo "Copying $LOG_SRC to $LOG_DST, filtering by $FILTER_PATTERN"
echo "Num lines: $(wc -l $LOG_DST)"



cat $LOG_SRC | grep $FILTER_PATTERN > $LOG_DST



echo "Done copying."
echo "Num lines: $(wc -l $LOG_DST)"
