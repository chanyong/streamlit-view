import streamlit as st
import mysql.connector
import pandas as pd
import pymysql
import altair as alt
import requests

st.title('상품권 시세 차트')
st.subheader(' ')

ip = requests.get('https://api.ipify.org').text
st.write("📡 Streamlit Cloud 서버의 외부 IP 주소는:")
st.code(ip)


st.markdown(
    '<a href="https://1bang.kr/pages/tp" target="_blank">'
    '<img src="https://1bang.kr/upload/195ca21600a64c248e1f68ee37b0e6ff.webp" />'
    '</a>',
    unsafe_allow_html=True
)

# Initialize connection.
# Uses st.cache_resource to only run once.
# @st.cache_resource
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()
curs = conn.cursor()

# 여러개 선택할 수 있을 때는 multiselect를 이용하실 수 있습니다
# return : list
select_ticket = st.selectbox(
    '✅ 확인하고자 하는 상품권을 선택해 주세요.',
    ['All', '롯데', '신세계', '현대']
)

# Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)

# Set All
if select_ticket != 'All':
    select_ticket = select_ticket + '10만'
print(select_ticket)

N = 2
for idx in range(N):

    # 매입 / 판매
    if idx == 0:
        sell_buy_nm = 'buy'
        subheader_nm = '상품권 시세 차트(매입)'
    else:
        sell_buy_nm = 'sell'
        subheader_nm = '상품권 시세 차트(판매)'

    ## 상품권 판매
    if select_ticket == 'All':
        db_condition = (sell_buy_nm, )
        sql = " select price_date , ticket_nm, ROUND(ticket_rate*100,2) \
            from ticket_price_daily where store_nm  = '미래' and sell_buy_nm  = %s and \
            ticket_nm in ('롯데10만','신세계10만', '현대10만' ) order by price_date desc "
    else:
        db_condition = (sell_buy_nm, select_ticket)
        sql = " select price_date , ticket_nm, ROUND(ticket_rate*100,2) \
            from ticket_price_daily where store_nm  = '미래' and sell_buy_nm  = %s and \
            ticket_nm in ('롯데10만','신세계10만', '현대10만' ) and ticket_nm = %s order by price_date desc "

    print(db_condition)
    curs.execute(sql, db_condition)

    result = curs.fetchall()
    result_df = pd.DataFrame(result)
    result_df.columns = ['일자', '티켓종류', '할인율']

    st.subheader(subheader_nm)
    st.write(result_df)

    chart = alt.Chart(result_df).mark_line().encode(
        x=alt.X('일자:N'),
        y=alt.Y('할인율:Q', scale=alt.Scale(domain=(1, 5.5))),
        color=alt.Color('티켓종류', legend=alt.Legend(
            orient='none',
            direction='horizontal',
            legendX=50, legendY=0,
            titleAnchor='middle'))
    )
    st.altair_chart(chart, use_container_width=True)



