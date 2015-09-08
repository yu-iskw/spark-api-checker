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

# Add the PySpark classes to the Python path:
export PYTHONPATH="$SPARK_HOME/python/:$PYTHONPATH"
PY4JPATH=$(find "$SPARK_HOME/python/lib" -name "py4j*zip")
export PYTHONPATH="$PY4JPATH:$PYTHONPATH"

python $SCRIPT_BASE/pyspark-api-checker.py $@
