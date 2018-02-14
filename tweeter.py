#!/usr/bin/env python
import threading, time
import multiprocessing

from kafka import KafkaConsumer, KafkaProducer

import markov
import sys


class Producer(threading.Thread):
    def __init__(self, topic):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.topic = topic
        self.model = markov.make_markov()
        self.gen = markov.generate_tweets(self.model)
        
    def stop(self):
        self.stop_event.set()

    def run(self):
        producer = KafkaProducer(bootstrap_servers='localhost:9092')


        while not self.stop_event.is_set():
            tweet = next(self.gen)
            print tweet
            producer.send(self.topic, tweet)
            time.sleep(0.5)

        producer.close()

        
        
def main(topic):
    tasks = [
        Producer(topic)
    ]

    for t in tasks:
        t.start()

    while True:
        try:
            time.sleep(100)
        except KeyboardInterrupt:
            for task in tasks:
                task.stop()
            break
        
        
if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: tweet-count.py <topic>\n")
        exit(-1)

    topic = sys.argv[-1]
    print "Topic:", topic
    main(topic)
