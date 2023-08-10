import streamlit as st
import pandas as pd
from newutill import get_user, get_stock_data, get_user_stock_info, buy_stock, sell_stock
import time

data = get_stock_data()

company_list = [i['company'] for i in data]

st.title("Stock Game | 주식거래")

df = pd.DataFrame(data).drop(columns=['_id'])
df.columns = ["회사명", "가격", "수량", "뉴스", "등락률"]
df = df[["회사명", "가격", "수량", "등락률", "뉴스"]]
st.dataframe(df, use_container_width=True, hide_index=True)

id = st.text_input("학번을 입력하세요.", 0)
reload = st.button("새로고침")

if reload:
    with st.spinner("새로고침 중..."):
        time.sleep(5)
        st.experimental_rerun()

if id:
    user_info = get_user(id)
    if user_info:
        st.markdown(f"### {user_info['name']} 님의 잔액: {user_info['account']:,} 원")

        col1, col2 = st.columns(2)
        with col1:
            with st.form("Buy Stock"):
                buy_company = st.selectbox("매수할 주식을 선택하세요.", company_list)
                buy_amount = st.number_input("개수를 선택하세요", min_value=1, value=1)
                buy_submit = st.form_submit_button("매수")

                if buy_submit:
                    buy_stock(id, buy_company, buy_amount)
                    time.sleep(1)
                    st.experimental_rerun()
        with col2:
            with st.form("Sell Stock"):
                sell_comapny = st.selectbox("매도할 주식을 선택하세요.", company_list)
                sell_amount = st.number_input("개수를 선택하세요", min_value=1, value=1)
                sell_submit = st.form_submit_button("매도")

                if sell_submit:
                    sell_stock(id, sell_comapny, sell_amount)
                    time.sleep(1)
                    st.experimental_rerun()
        with st.sidebar:
            data = get_user_stock_info(id)
            st.markdown(f"## 내 보유 주식")
            if data and data['stocks']:
                df = pd.DataFrame(data['stocks'])
                df.columns = ["회사명", "수량", "평균단가", "총합"]
                df = df[["회사명", "평균단가", "수량", "총합"]]
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.warning("현재 소유하고 있는 주식이 없습니다.")
    else:
        st.error("학번을 확인해주세요.")
else:
    st.error("학번을 입력해주세요.")



