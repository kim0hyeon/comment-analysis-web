import streamlit as st

def main():
    st.set_page_config(
        page_title="감정 분석 앱 데모",
        layout="centered"
    )
    st.title("감정 분석 앱 데모")
    st.write("왼쪽 사이드바에서 페이지를 선택해주세요.")

if __name__ == "__main__":
    main()