
## Installation

1) Download spark zip file
2) Unzip the folder and move it to your home directory
3) Add the following to your `.bash_profile` in mac or `.basrc` in linux


```
######## Setting path for pyspark ###################################### 

export SPARK_PATH=~/spark-2.3.0-bin-hadoop2.7
export PYSPARK_PYTHON=python3
export SPARK_HOME=~/spark-2.3.0-bin-hadoop2.7
alias pyspark=$SPARK_PATH/bin/pyspark

###################################################################### 
```

```
######## Setting path for spark ###################################### 

export SPARK_PATH=~/spark-2.3.0-bin-hadoop2.7
export PYSPARK_DRIVER_PYTHON="jupyter"
export PYSPARK_DRIVER_PYTHON_OPTS="notebook"
# For python 3, You have to add the line below or you will get an error
export PYSPARK_PYTHON=python3
alias snotebook='$SPARK_PATH/bin/pyspark --master local[2]'
alias pyspark='~/spark-2.3.0-bin-hadoop2.7/bin/pyspark  local[4]'
###################################################################### 
```

- Notice that `local[2]` indicates the number of CPU cores that will be used by spark


4) Make the changes visible doing `source .bash_profile`

