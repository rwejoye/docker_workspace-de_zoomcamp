#!/usr/bin/env python
# coding: utf-8

#-- Import Necessary Libraries
import pandas as pd
import click
from tqdm.auto import tqdm
from sqlalchemy import create_engine

#-- Data Types and Date Parsing for Pandas DataFrame
dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

@click.command()
@click.option("--year", type=int, default=2021, show_default=True, help="Year of the data file")
@click.option("--month", type=int, default=1, show_default=True, help="Month of the data file")
@click.option("--pg-user", default="root", show_default=True, help="Postgres username")
@click.option("--pg-pass", default="root", show_default=True, help="Postgres password")
@click.option("--pg-host", default="localhost", show_default=True, help="Postgres host")
@click.option("--pg-port", type=int, default=5432, show_default=True, help="Postgres port")
@click.option("--pg-db", default="ny_taxi", show_default=True, help="Postgres database name")
@click.option("--target-table", default="yellow_taxi_data", show_default=True, help="Target table name")
@click.option("--chunksize", type=int, default=100000, show_default=True, help="Number of rows per chunk")
def run(year, month, pg_user, pg_pass, pg_host, pg_port, pg_db, target_table, chunksize):
    PREFIX = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow"
    url = f"{PREFIX}/yellow_tripdata_{year}-{month:02d}.csv.gz"
    engine = create_engine(
        f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize
    )

    first = True
    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists='replace'
            )
            first = False

        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists='append'
        )


if __name__ == '__main__':
    run()
