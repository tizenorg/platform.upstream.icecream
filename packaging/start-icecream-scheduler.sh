#!/bin/bash

. /etc/sysconfig/icecream

echo -n "Starting Distributed Compiler Daemon Scheduler"
netname=
if test -n "$ICECREAM_NETNAME"; then
	netname="-n $ICECREAM_NETNAME"
fi
	
logfile=""
if test -z "$ICECREAM_SCHEDULER_LOG_FILE"; then
	ICECREAM_SCHEDULER_LOG_FILE="/var/log/icecc_scheduler"
fi
logfile="-l $ICECREAM_SCHEDULER_LOG_FILE"
: > $ICECREAM_SCHEDULER_LOG_FILE
chown icecream:icecream $ICECREAM_SCHEDULER_LOG_FILE
/usr/sbin/scheduler -d $logfile $netname
