FROM ubuntu:16.04

MAINTAINER Anirban Das <anirban.dash@gmail.com>

ENV workdir /opt
ENV SBT_VERSION 1.1.0

COPY *.sh $workdir/
COPY *.py $workdir/
COPY *.jar $workdir/
COPY *.txt $workdir/

RUN chmod +x $workdir/*.sh

RUN apt-get update && apt-get -y install \
    build-essential autoconf automake libtool git wget curl supervisor \
    openjdk-8-jdk maven scala \
    python-pip nano \
    zookeeper zookeeper-bin zookeeperd && \
    rm -rf /var/lib/apt/lists/*

RUN curl -L -o sbt-$SBT_VERSION.deb https://dl.bintray.com/sbt/debian/sbt-$SBT_VERSION.deb && \
  dpkg -i sbt-$SBT_VERSION.deb && \
  rm sbt-$SBT_VERSION.deb && \
  apt-get update && \
  apt-get install sbt && \
  sbt sbtVersion
  
RUN pip install --upgrade pip

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

RUN curl -L http://mirrors.ibiblio.org/apache/kafka/1.0.0/kafka_2.11-1.0.0.tgz| \
    tar xzv -C $workdir -f - && mv $workdir/kafka* $workdir/kafka
ENV KAFKA_HOME $workdir/kafka

RUN curl -L http://apache.mesi.com.ar/hadoop/common/hadoop-3.0.0/hadoop-3.0.0.tar.gz | \
    tar xzv -C $workdir -f - && mv $workdir/hadoop* $workdir/hadoop
ENV HADOOP_HOME $workdir/hadoop

RUN curl -L http://mirrors.koehn.com/apache/spark/spark-2.2.1/spark-2.2.1-bin-hadoop2.7.tgz| \
    tar xzv -C $workdir -f -  && mv $workdir/spark-2.2.1-bin-hadoop2.7 $workdir/spark

ENV PATH $workdir/hadoop/bin:$workdir/kafka/bin:$workdir/spark/bin:$workdir/sbt/bin:$PATH

RUN pip install --no-cache-dir pyspark tweepy kafka-python python-twitter markovify

RUN apt-get install -y supervisor && mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 9092 2181 2888 3888 22 80 8080 8081 4040 4044

VOLUME ["/var/log", "/tmp"]

WORKDIR $workdir
CMD ["./entrypoint.sh"]
