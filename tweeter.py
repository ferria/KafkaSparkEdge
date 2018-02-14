#!/usr/bin/env python
import threading, time
import multiprocessing

from kafka import KafkaConsumer, KafkaProducer

import markov
import sys
import random

users = ["Emma","Noah","Olivia","Liam","Ava","William"]


class Producer(threading.Thread):
    def __init__(self, topic, inclUser):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.topic = topic
        self.model = markov.make_markov()
        self.gen = markov.generate_tweets(self.model)
        self.inclUser = inclUser

    def stop(self):
        self.stop_event.set()

    def run(self):
        producer = KafkaProducer(bootstrap_servers='localhost:9092')


        while not self.stop_event.is_set():
            tweet = next(self.gen)
            if self.inclUser:
                tweet = random.choice(users) + ':'  + tweet
            print tweet
            producer.send(self.topic, tweet)
            time.sleep(0.5)

        producer.close()

        
        
def main(topic, inclUser):
    tasks = [
        Producer(topic, inclUser)
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
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: tweet-count.py <topic> <add usernames?>\n")
        exit(-1)

    topic = sys.argv[-2]
    inclUser = sys.argv[-1].lower() in {'true','t', 'yes', 'y'}
    print "Topic:", topic
    print "Include usernames?:", inclUser
    main(topic, inclUser)
