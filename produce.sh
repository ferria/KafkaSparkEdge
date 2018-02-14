#!/bin/bash
kafka-console-producer.sh --broker-list localhost:9092 --topic "$1"
