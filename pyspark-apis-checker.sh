#!/usr/bin/env bash

#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

export SCRIPT_BASE="$(cd "`dirname "$0"`"; pwd)"
export SPARK_HOME="$SCRIPT_BASE/spark"
cd "$SPARK_HOME"

# Determine the Python executable to use if PYSPARK_PYTHON or PYSPARK_DRIVER_PYTHON isn't set:
if hash python2.7 2>/dev/null; then
  # Attempt to use Python 2.7, if installed:
  DEFAULT_PYTHON="python2.7"
else
  DEFAULT_PYTHON="python"
fi

TAGS_AND_BRANCHES=`cat << EOM
0.3-scala-2.8
0.3-scala-2.9
alpha-0.1
alpha-0.2
v0.5.0
v0.5.1
v0.5.2
v0.6.0
v0.6.0-yarn
v0.6.1
v0.6.2
v0.7.0
v0.7.0-bizo-1
v0.7.1
v0.7.2
v0.8.0-incubating
v0.8.1-incubating
v0.9.0-incubating
v0.9.1
v0.9.2
v1.0.0
v1.0.1
v1.0.2
v1.1.0
v1.1.1
v1.2.0
v1.2.1
v1.2.2
v1.3.0
v1.3.1
v1.4.0
v1.4.1
v1.5.0
v1.5.1
master
EOM
`

MODULES=`cat << EOM
pyspark.mllib.classification
pyspark.mllib.clustering
pyspark.mllib.evaluation
pyspark.mllib.feature
pyspark.mllib.fpm
pyspark.mllib.random
pyspark.mllib.recommendation
pyspark.mllib.regression
pyspark.mllib.tree
pyspark.mllib.util
pyspark.ml.classification
pyspark.ml.clustering
pyspark.ml.recommendation
pyspark.ml.regression
pyspark.ml.tuning
pyspark.ml.util
pyspark.ml.param
EOM
`

# Make a directory to store result files
RESULT_DIR="$SCRIPT_BASE/pyspark-apis-checker-result"
if [ ! -d "$RESULT_DIR" ] ; then
  mkdir -p "$RESULT_DIR"
fi

for i in $TAGS_AND_BRANCHES
do
  echo $i
  git checkout -f $i

  for m in $MODULES
  do
    echo $m
    if [ ! -d "$RESULT_DIR/$m" ] ; then
      mkdir -p "$RESULT_DIR/$m"
    fi

    # Add the PySpark classes to the Python path:
    PY4JPATH=$(find "$SPARK_HOME/python/lib" -name "py4j*zip")
    export PYTHONPATH="$SPARK_HOME/python/:$PYTHONPATH"
    export PYTHONPATH="$PY4JPATH:$PYTHONPATH"

    # Delete cache files
    find "$SPARK_HOME/python" -name "*.pyc" -delete

    JSON=`python "$SCRIPT_BASE/pyspark-api-checker.py" "$m"`
    if [ `echo "$JSON" | wc -c` -gt 1 ] ; then
      echo "$JSON" > "$RESULT_DIR/$m/$m.$i.json"
    fi
  done
done
