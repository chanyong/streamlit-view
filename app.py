import streamlit as st
import mysql.connector
import pandas as pd
import pymysql

# Initialize connection.
# Uses st.cache_resource to only run once.
# @st.cache_resource
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()

curs = conn.cursor()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)
sql = "SELECT * from ticket_price_daily;"
curs.execute(sql)
result = curs.fetchall()
result_df = pd.DataFrame(result)
st.table(result_df.head())
