import pandas as pd
import snowflake.connector
import os

from dotenv import load_dotenv
from snowflake.connector.pandas_tools import write_pandas

# use python 3.9, snowflake connector not compatible with 3.11 yet
# set filepath(s)
directory = 'test'
queue = []
for file in os.listdir(directory):
    queue.append(f'{directory}/{file}')

# set destination table
TABLE_NAME = 'TEST_TABLE'

# load and set environment variables
vars = load_dotenv()
USERNAME = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
ACCOUNT = os.getenv('ACCOUNT')
WAREHOUSE = os.getenv('WAREHOUSE')
DATABASE = os.getenv('DATABASE')
SCHEMA = os.getenv('SCHEMA')

# initialize connection
with snowflake.connector.connect(
    user=USERNAME,
    password=PASSWORD,
    account=ACCOUNT,
    warehouse=WAREHOUSE,
    database=DATABASE,
    schema=SCHEMA
) as con:

    for filepath in queue:
        print(f'Loading {filepath}...')
        results = pd.read_pickle(filepath)

        # capitalize column names to match table
        results.columns = map(lambda x: str(x).upper(), results.columns)

        # write to snowflake
        success, nchunks, nrows, _ = write_pandas(
            con, 
            results, 
            table_name=TABLE_NAME,
            chunk_size = 300
            )

        if success:
            print(f'Loaded {nrows} rows into {nchunks} chunks to {TABLE_NAME} table from {filepath}.')
        else:
            print(f'Failed to load {filepath} to {TABLE_NAME} table.')
            break