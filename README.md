### A container for deploying an Apache Kafka+Spark container on the edge

## Helpful Docker tips

You can find the container id with ```docker ps```   

Copy a file to docker with ```docker cp <local file> <container id>:<container filepath>```


Open another terminal into container: ```docker exec -it <container id> bash```  

    
You may need to run these commands as root. 


## Running Kafka with Spark Streaming

Download: `docker pull ferria/kafkaspark`

Run: `docker run -p 2181:2181 -p 9092:9092 -it ferria/kafkaspark`

## Shell Scripts

```./produce.sh <topic>```

```./consume.sh <topic>```

```./run.sh <program> <args...>```