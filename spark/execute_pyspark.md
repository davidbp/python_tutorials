### Executing pyspark scripts

In order to execute pyspark script do the following:

```
PYTHONSTARTUP=dummy_collect.py pyspark
```

- https://github.com/kayousterhout/trace-analysis
- https://stackoverflow.com/questions/31233830/apache-spark-setting-spark-eventlog-enabled-and-spark-eventlog-dir-at-submit-or


In this case `dummy_collect.py` contains

```
x = sc.parallelize(range(10000))
aux = x.collect()
print("\n\nCollected first item", aux[0],"\n\n")
exit()
```
