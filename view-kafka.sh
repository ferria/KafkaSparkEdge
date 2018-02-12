#!/bin/bash 
kafka-console-consumer --zookeeper "localhost:2181" --topic "$1" --from-beginning
