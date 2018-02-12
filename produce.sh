#!/bin/bash 
echo "$1" | kafka-console-producer.sh --broker-list "localhost:9092" --topic "$2"
