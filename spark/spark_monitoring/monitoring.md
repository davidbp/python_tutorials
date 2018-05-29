

## Spark instrumentation

1) Web UI
2) REST API
3) Eventlog
4) Executor/Task Metrics
5) Dropwizard metrics library



### 1) Web UI

When opening pyspark (or executing a spark application)
```
 pyspark
```
You will be prompted with a similar message

```
Python 2.7.13 |Anaconda custom (64-bit)| (default, Dec 20 2016, 23:09:15) 
[GCC 4.4.7 20120313 (Red Hat 4.4.7-1)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
Anaconda is brought to you by Continuum Analytics.
Please check out: http://continuum.io/thanks and https://anaconda.org
2018-05-28 16:35:26 WARN  Utils:66 - Your hostname, bsc-laptop resolves to a loopback address: 127.0.1.1; using 84.88.50.108 instead (on interface eth0)
2018-05-28 16:35:26 WARN  Utils:66 - Set SPARK_LOCAL_IP if you need to bind to another address
2018-05-28 16:35:26 WARN  NativeCodeLoader:62 - Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
2018-05-28 16:35:27 WARN  Utils:66 - Service 'SparkUI' could not bind on port 4040. Attempting port 4041.
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 2.3.0
      /_/

Using Python version 2.7.13 (default, Dec 20 2016 23:09:15)
SparkSession available as 'spark'.
```

Notice that the message suggests that `http://localhost:4041/jobs` will contain the `SparkUI`. If we go to our browser and we write `http://localhost:4041/jobs` we will see a dashboard with information related to the execution of the Spark engine. By default the port should be `4040`.

### 2) REST API

Sometimes we don't want to look at a webpage but we would like to make a program gather data from the spark jobs and make actions depending on the data. There is a way to parse the data displayed in the `SparkUI` without the need to make a parser of the html source file of the page.


For exmaple: `http://localhost:4042/api/v1/applications/` will contain
```
[ {
  "id" : "local-1527523284699",
  "name" : "PySparkShell",
  "attempts" : [ {
    "startTime" : "2018-05-28T16:01:23.887GMT",
    "endTime" : "1969-12-31T23:59:59.999GMT",
    "lastUpdated" : "2018-05-28T16:01:23.887GMT",
    "duration" : 0,
    "sparkUser" : "david",
    "completed" : false,
    "appSparkVersion" : "2.3.0",
    "startTimeEpoch" : 1527523283887,
    "endTimeEpoch" : -1,
    "lastUpdatedEpoch" : 1527523283887
  } ]
} ]
```
Which can be parsed
```python
import urllib3
file = urllib3.urlopen("http://localhost:4042/api/v1/applications/")

data = file.read()
file.close()
data
'[ {\n  "id" : "local-1527523284699",\n  "name" : "PySparkShell",\n  "attempts" : [ {\n    "startTime" : "2018-05-28T16:01:23.887GMT",\n    "endTime" : "1969-12-31T23:59:59.999GMT",\n    "lastUpdated" : "2018-05-28T16:01:23.887GMT",\n    "duration" : 0,\n    "sparkUser" : "david",\n    "completed" : false,\n    "appSparkVersion" : "2.3.0",\n    "startTimeEpoch" : 1527523283887,\n    "endTimeEpoch" : -1,\n    "lastUpdatedEpoch" : 1527523283887\n  } ]\n} ]'
```
We can make this as follows (THIS CODE IS NOT CORRECT)

```python
import urllib2
import xmltodict
def parse_from_url(url):
   file = urllib2.urlopen(url, encoding='utf-8')
   data = file.read()
   file.close()
   data = xmltodict.parse(data)
   return data

parse_from_url("http://localhost:4042/api/v1/applications/")
```

## 3) Eventlog


### Saving log files from spark


Inside `/spark-2.3.0-bin-hadoop2.7/conf/spark-defaults.conf`  write the following

```
# spark.master                     spark://master:7077
# spark.eventLog.enabled           true
# spark.eventLog.dir               hdfs://namenode:8021/directory
# spark.serializer                 org.apache.spark.serializer.KryoSerializer
# spark.driver.memory              5g
# spark.executor.extraJavaOptions  -XX:+PrintGCDetails -Dkey=value -Dnumbers="one two three"

spark.eventLog.enabled           true
spark.eventLog.dir    /home/david/spark_eventlogs
```

#### tracelogs: Library to read eventlogs

- https://github.com/kayousterhout/trace-analysis

#### About eventlogs

- Enable spark log history: https://www.ibm.com/support/knowledgecenter/en/SS3MQL_1.1.1/management_sym/spark_configuring_history_service.html

- About monitoring spark: http://spark.apache.org/docs/latest/monitoring.html#spark-configuration-options



#### What's the difference between spark.eventLog.dir and spark.history.fs.logDirectory?

Notice that in `spark-defaults.conf` you can set

```
spark.eventLog.dir hdfs:///var/log/spark/apps
spark.history.fs.logDirectory hdfs:///var/log/spark/apps
```

At a high level `spark.eventLog.dir` is to generate logs while `spark.history.fs.logDirectory` is the place where Spark History Server finds log events. 

- `spark.eventLog.dir` is the base directory in which Spark events are logged, if spark.eventLog.enabled is true. Within this base directory, Spark creates a sub-directory for each application, and logs the events specific to the application in this directory. Users may want to set this to a unified location like an HDFS directory so history files can be read by the history server
- `spark.history.fs.logDirectory` is for the filesystem history provider, the URL to the directory containing application event logs to load. This can be a local file:// path, an HDFS path hdfs://namenode/shared/spark-logs or that of an alternative filesystem supported by the Hadoop APIs.



http://spark.apache.org/docs/latest/configuration.html#spark-ui

https://stackoverflow.com/questions/32001248/whats-the-difference-between-spark-eventlog-dir-and-spark-history-fs-logdirecto



## Relevant links

#### Spark logs

- https://www.linkedin.com/pulse/apache-spark-streaming-logging-driver-executor-logs-right-prakash/


#### SparkMeasure library

- https://github.com/LucaCanali/sparkMeasure
    - https://www.youtube.com/watch?v=JoQ8m-kM_ZY

#### Sparklint

- https://github.com/groupon/sparklint

About CPU utilization
- http://www.brendangregg.com/blog/2017-05-09/cpu-utilization-is-wrong.html
- https://github.com/LucaCanali/Miscellaneous/blob/master/Spark_Notes/Tools_Linux_Memory_Perf_Measure.md