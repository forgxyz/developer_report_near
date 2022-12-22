import pandas as pd
import snowflake.connector

from dotenv import load_dotenv
from os import getenv
from snowflake.connector.pandas_tools import write_pandas

# load necessary local files
vars = load_dotenv()
results = pd.read_pickle('results.pkl')

# sample = results[5:10]

# set environment variables
USERNAME = getenv('LOGIN')
PASSWORD = getenv('PASSWORD')
ACCOUNT = getenv('ACCOUNT')
WAREHOUSE = getenv('WAREHOUSE')
DATABASE = getenv('DATABASE')
SCHEMA = getenv('SCHEMA')
TABLE_NAME = getenv('TABLE_NAME')



# capitalize column names to match table
results.columns = map(lambda x: str(x).upper(), results.columns)
# sample.columns = map(lambda x: str(x).upper(), sample.columns)

# initialize connection
with snowflake.connector.connect(
    user=USERNAME,
    password=PASSWORD,
    account=ACCOUNT,
    warehouse=WAREHOUSE,
    database=DATABASE,
    schema=SCHEMA
) as con:

    # write to snowflake
    success, nchunks, nrows, _ = write_pandas(
        con, 
        results, 
        table_name=TABLE_NAME,
        chunk_size = 300
        )
