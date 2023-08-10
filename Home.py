import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Stock Game | HOME",
    initial_sidebar_state="expanded",
)

st.title("Stock Game")
st.markdown("### 주식게임에 오신 것을 환영합니다!")
st.markdown("##### 게임 방법")
st.markdown("""1. Register 페이지에 들어가 학번과 이름을 입력합니다. 
                \n2. Trade 페이지에서 학번을 입력하고 주식거래를 진행합니다.
                \n3. Trade 페이지에서 새로 고침시 5초간의 딜레이가 존재합니다. 참고해주세요.
                \n4. 오류 발생시 me@kimsman.kr 로 오류 메시지와 함께 캡처하여 이메일로 보내주세요.
            """)
