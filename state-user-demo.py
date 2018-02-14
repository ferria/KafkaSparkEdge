"""
Counts words in UTF8 encoded, '\n' delimited text received from the
 network every second.

 Usage: stateful_network_wordcount.py <hostname> <port>
   <hostname> and <port> describe the TCP server that Spark Streaming
    would connect to receive data.

 To run this on your local machine, you need to first run a Netcat server
    `$ nc -lk 9999`
 and then run the example
    `$ bin/spark-submit examples/src/main/python/streaming/stateful_network_wordcount.py \
        localhost 9999`

Modified this to work with KAFKA word stream

"""
from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from quiet import quiet_logs
import tweeter

def filter_fun(user):
    def filter_user(tweet):
        # PUT check for user here (true iff tweet by user)
        return True
    return filter_user


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.stderr.write("Usage: stateful_network_wordcount.py <zk> <topicname> <username>\n")
        exit(-1)

    if sys.argv[3].lower() not in map(str.lower,tweeter.users):
        sys.stderr.write('{0} not in {1}\n'.format(sys.argv[3],tweeter.users))
        sys.exit(1)

    my_filter = filter_fun(sys.argv[3])
    sc = SparkContext(appName="PythonStreamingStatefulNetworkWordCount")
    quiet_logs(sc)
    ssc = StreamingContext(sc, 10)
    ssc.checkpoint("checkpoint") #setting up the checkpoint
    
    # RDD with initial state (key, value) pairs
    initialStateRDD = sc.parallelize([])

    def updateFunc(new_values, last_sum):
        return sum(new_values) + (last_sum or 0)
    
    #kafka related stuff like the other one
    zkQuorum, topic = sys.argv[1:3]
    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
    lines = kvs.map(lambda x: x[1])

    # Need to get tweet from "user:tweet"

    # You can also write another predicate to filter just hash tags for a given user
    
    running_counts = lines.flatMap(lambda line: split(" "))\
                          .map(lambda word: (word, 1))\
                          .updateStateByKey(updateFunc, initialRDD=initialStateRDD)\
                          .transform(lambda rdd: rdd.sortBy(lambda x: x[1], ascending=False))

    running_counts.pprint()

    ssc.start()
    ssc.awaitTermination()
