# Apache Spark MLlib API checker

These scripts is used for extracting when a PySpark API is available based on the Spark `master` branch.

For example, `DecisionTree` is like below:

where,
- `version`: when it was available
- `class_methods`: `staticmethod` and `classmethods`
- `instance_methods`: `@property`, `function` abd `instancemethods`
- `type`: the result of `type()`

That is, `DecisionTree` was released at `v1.1.0` and `trainRegressor` was also released at `v1.1.0`.

```
{
  "instance_methods": [],
  "version": "v1.1.0",
  "name": "DecisionTree",
  "class_methods": [
    {
      "version": "v1.1.0",
      "type": "instancemethod",
      "name": "trainRegressor"
    },
    {
      "version": "v1.2.0",
      "type": "instancemethod",
      "name": "_train"
    },
    {
      "version": "v1.1.0",
      "type": "instancemethod",
      "name": "trainClassifier"
    }
  ]
}
```

## Pre-Requirement

```
git clone https://github.com/apache/spark.git
```

## How to Use

### Get the definitions of `pyspark.mllib.clustering`

```
bash pyspark-api-checker.sh pyspark.mllib.clustering
```

### Get the definitions of the whole modules

```
bash pyspark-apis-checker.sh
mkdir pyspark-differ
python pyspark-differ.py
```
