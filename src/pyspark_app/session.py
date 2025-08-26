import os
from pyspark.sql import SparkSession

def build_spark(app_name: str = "PySparkJupyter") -> SparkSession:
    """
    Cria uma SparkSession pronta para usar JDBC do Postgres.
    Requer o driver .jar já presente em /usr/local/spark/jars (feito no Dockerfile).
    """
    # Opções comuns; ajuste conforme seu caso
    spark = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        # Recomendações para Arrow/Parquet e performance em notebook
        .config("spark.sql.execution.arrow.pyspark.enabled", "true")
        .config("spark.sql.shuffle.partitions", "200")
        .getOrCreate()
    )

    # Variáveis do Postgres, lidas do ambiente (passadas pelo docker-compose)
    spark.conf.set("spark.app.postgres.host", "postgres")
    spark.conf.set("spark.app.postgres.port", os.getenv("POSTGRES_PORT", "5432"))
    spark.conf.set("spark.app.postgres.db", os.getenv("POSTGRES_DB", "meubanco"))
    spark.conf.set("spark.app.postgres.user", os.getenv("POSTGRES_USER", "meuusuario"))
    spark.conf.set("spark.app.postgres.password", os.getenv("POSTGRES_PASSWORD", "senha_super_secreta"))

    return spark

def jdbc_url() -> str:
    host = "postgres"
    port = os.getenv("POSTGRES_PORT", "5432")
    db   = os.getenv("POSTGRES_DB", "meubanco")
    return f"jdbc:postgresql://{host}:{port}/{db}"

def jdbc_props() -> dict:
    return {
        "user": os.getenv("POSTGRES_USER", "meuusuario"),
        "password": os.getenv("POSTGRES_PASSWORD", "senha_super_secreta"),
        "driver": "org.postgresql.Driver",
        # "ssl": "true",  # habilite se necessário
    }
