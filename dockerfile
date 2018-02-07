FROM ubuntu:16.04

MAINTAINER Anirban Das <anirban.dash@gmail.com>

ENV workdir /opt

SHELL ["/bin/sh", "-c"]

RUN apt-get update && apt-get install \
    build-essential autoconf automake libtool git wget curl supervisor \
    openjdk-8-jdk maven scala sbt \
    zookeeper zookeeper-bin zookeeperd && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

RUN wget http://mirrors.ibiblio.org/apache/kafka/1.0.0/kafka_2.11-1.0.0.tgz| \
    tar xzvf -C $workdir -f - && mv $workdir/kafka* $workdir/kafka
ENV KAFKA_HOME $workdir/kafka

RUN wget http://apache.mesi.com.ar/hadoop/common/hadoop-3.0.0/hadoop-3.0.0.tar.gz | \
    tar xzv -C $workdir -f - && mv $workdir/hadoop* $workdir/hadoop
ENV HADOOP_HOME $workdir/hadoop

RUN wget http://mirrors.koehn.com/apache/spark/spark-2.2.1/spark-2.2.1-bin-hadoop2.7.tgz| \
    tar xzvf -C $workdir -f - && mv $workdir/spark* $workdir/spark

ENV PATH $workdir/hadoop/bin:$workdir/kafka/bin:$workdir/spark/bin:$workdir/sbt/bin:$PATH

RUN apt-get install -y supervisor && mkdir -p /var/log/supervisor
COPY supervisord*.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 2181 2888 3888 22 80 8080 8081 4040 4044

COPY entrypoint.sh $workdir/
RUN chmod +x $workdir/entrypoint.sh

VOLUME ["/var/log", "/tmp"]

WORKDIR $workdir
CMD ["./entrypoint.sh"]


