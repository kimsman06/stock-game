import streamlit as st
import pandas as pd
from newutill import get_stock_data, update_stock_info, get_user, initial_stock

st.title("Stock Game | Game Setting Page")
st.markdown("### 게임 설정 페이지 입니다.")
st.warning("관리자외에는 접근할 수 없습니다.")
id = st.text_input("ID를 입력해주세요.", 0)

user = get_user(id)

if id and user:
    if st.secrets["mongo"]["adminId"] == str(user['_id']):        
        data = get_stock_data()
        df = pd.DataFrame(data).drop(columns=['_id'])
        df.columns = ["회사명", "가격", "수량", "뉴스", "등락률"]
        df = df[["회사명", "가격", "수량", "등락률", "뉴스"]]
        st.dataframe(df, use_container_width=True, hide_index=True)
        reload = st.button("주식 데이터 변경")
        initail_setting = st.button("게임 초기화")

        if reload:
            update_stock_info()
            st.experimental_rerun()
        
        if initail_setting:
            initial_stock()
            st.experimental_rerun()