import streamlit as st
import pandas as pd
import time
from newutill import get_stock_data, update_stock_info, get_user, get_users, initial_stock

st.title("Stock Game | Game Setting Page")
st.markdown("### 게임 설정 페이지 입니다.")
st.warning("관리자외에는 접근할 수 없습니다.")
id = st.text_input("ID를 입력해주세요.", 0)

user = get_user(id)

if id and user:
    if st.secrets["mongo"]["adminId"] == str(user['_id']):
        tab1, tab2 = st.tabs(["주식정보", "유저정보"])
        with tab1:
            st.markdown("### 주식정보")
            stocks = get_stock_data()
            df = pd.DataFrame(stocks).drop(columns=['_id'])
            df.columns = ["회사명", "가격", "수량", "뉴스", "등락률"]
            df = df[["회사명", "가격", "수량", "등락률", "뉴스"]]
            config = {"등락률" : st.column_config.NumberColumn(format="%f%%")}
            st.dataframe(df, use_container_width=True, hide_index=True, column_config=config)

        with tab2:
            st.markdown("### 유저 정보")
            users = get_users()
            user_df = pd.DataFrame(users).drop(columns=['_id']).astype({'id' : 'str'})
            st.dataframe(user_df, use_container_width=True, hide_index=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            reload = st.button("주식 데이터 변경", use_container_width=True)
        with col2:
            initail_setting = st.button("게임 초기화", use_container_width=True)
        with col3:
            restart = st.button("새로고침", use_container_width=True)

        if restart:
            with st.spinner("새로고침 중..."):
                time.sleep(1)
                st.experimental_rerun()
        if reload:
            update_stock_info()
            st.experimental_rerun()
        
        if initail_setting:
            initial_stock()
            st.experimental_rerun()