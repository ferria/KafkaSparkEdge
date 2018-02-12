#!/bin/bash
echo "Starting ZooKeeper and Kafka in background at port 2181 and 9092"

/usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
