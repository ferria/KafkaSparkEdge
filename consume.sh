#!/bin/bash 
kafka-console-consumer.sh --zookeeper "localhost:2181" --topic "$1" --from-beginning
