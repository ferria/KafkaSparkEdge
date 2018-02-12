#!/bin/bash 
echo "$1" | kafka-console-producer --broker-list "localhost:9092" --topic "$2"
