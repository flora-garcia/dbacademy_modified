def init_locals():
    from pyspark.sql import SparkSession

    # noinspection PyGlobalUndefined
    global spark, sc, dbutils

    try:
        spark
    except NameError:
        spark = SparkSession.builder.getOrCreate()

    try:
        sc
    except NameError:
        sc = spark.sparkContext

    try:
        dbutils
    except NameError:
        if spark.conf.get("spark.databricks.service.client.enabled") == "true":
            from pyspark.dbutils import DBUtils
            dbutils = DBUtils(spark)
        else:
            import IPython
            dbutils = IPython.get_ipython().user_ns["dbutils"]

    return sc, spark, dbutils


def get_tags() -> dict:
    # noinspection PyProtectedMember
    return sc._jvm.scala.collection.JavaConversions.mapAsJavaMap(
        dbutils.entry_point.getDbutils().notebook().getContext().tags())


def get_tag(tag_name: str, default_value: str = None) -> str:
    values = get_tags()[tag_name]
    try:
        if len(values) > 0:
            return values
    except KeyError:
        return default_value


def get_username() -> str:
    return get_tags()["user"]


def get_notebook_path() -> str:
    return dbutils.entry_point.getDbutils().notebook().getContext().notebookPath().getOrElse(None)


def get_notebook_name() -> str:
    return get_notebook_path().split("/")[-1]


def get_notebook_dir(offset=-1) -> str:
    return "/".join(get_notebook_path().split("/")[:offset])


def get_notebooks_api_endpoint() -> str:
    return dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiUrl().getOrElse(None)


def get_notebooks_api_token() -> str:
    return dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().getOrElse(None)
