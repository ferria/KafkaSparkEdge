#!/bin/bash
spark-submit --jars spark-streaming-kafka-0-8-assembly_2.11-2.0.0-preview.jar --master local[2] "$@"
