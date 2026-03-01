import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///stratiq.db')

def save_scenario(data):
    df = pd.DataFrame([data])
    df.to_sql("scenarios", engine, if_exists="append", index=False)

def load_scenarios():
    try:
        return pd.read_sql("SELECT * FROM scenarios", engine)
    except:
        return pd.DataFrame()