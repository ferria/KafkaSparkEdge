# A container for deploying an Apache Kafka+Spark container on the edge

## Helpful Docker tips

You can find the container id with ```docker ps```   

Copy a file to docker with ```docker cp <local file> <container id>:<container filepath>```


Open another terminal into container: ```docker exec -it <container id> bash```  
   
You may need to run these commands as root. 

### Cleanup

Delete all containers: ```docker rm $(docker ps -a -q)```

Delete all images: ```docker rmi $(docker images -q)```


## Running Kafka with Spark Streaming

Download: `docker pull ferria/kafkaspark`

Run: `docker run -p 2181:2181 -p 9092:9092 -it ferria/kafkaspark`

Leave this terminal running and open two more terminals side by side with ```docker exec -it <container id> bash```.

### Ports

ZooKeeper: 2181

Kafka: 9092

## Shell Scripts

Terminal producer: ```./produce.sh <topic>```

Terminal Consumer: ```./consume.sh <topic>```

Running programs with spark streaming: ```./run.sh <program> <args...>```

## Python Scripts

### Spark Streaming (Consumer)

Word Count: ```wc.py localhost:2181 <topic>```

Top Hashtags: ```state-tweet-count.py localhost:2181 <topic>```

The above scripts get passed to ```run.sh```.  For example, ```./run.sh wc.py localhost:2181 <topic>```

### Producer

Tweeter: ```python tweeter.py <topic>```




