import streamlit as st
from newutill import create_user

st.title("Stock Game | 유저정보 등록")

with st.form("resgister-user-info"):
    user_id = st.text_input("학번을 입력하세요.")
    username = st.text_input("이름을 입력하세요.")
    submit = st.form_submit_button("제출하기")

if user_id and username and submit:
    with st.spinner("전송중..."):
        if create_user(user_id, username):
            st.success("정상 제출되었습니다.")
        else:
            st.error("오류가 발생했습니다.")
else:
    st.error("학번과 이름을 입력해주세요.")