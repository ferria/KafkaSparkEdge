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
            producer.send(self.topic, next(self.gen))
            time.sleep(0.5)

        producer.close()

        
        
def main(topic):
    tasks = [
        Producer(topic)
    ]

    for t in tasks:
        t.start()

    """
    time.sleep(10)
    
    for task in tasks:
        task.stop()

    for task in tasks:
        task.join()
    """
        
        
if __name__ == "__main__":

    topic = sys.argv[-1]
    main(topic)
