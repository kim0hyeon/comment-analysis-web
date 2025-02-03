import streamlit as st
from textblob import TextBlob

# 제목
st.title("댓글 감정 분석 웹 앱")

#댓글 입력받기
comment = st.text_area("댓글을 입력하세요:")
comment = comment.strip()

#댓글 분석 버튼
if st.button("분석하기"):
    if comment:
        # 감정 분석 수행
        analysis = TextBlob(comment)
        sentiment_score = analysis.sentiment.polarity
        st.info(f"점수 = {sentiment_score}")
        
        # 감정 결과 표시
        if sentiment_score > 0.1:
            st.success("긍정적인 댓글입니다! 😊")
        elif sentiment_score < -0.1:
            st.error("부정적인 댓글입니다. 😢")
        else:
            st.info("중립적인 댓글입니다. 😐")
    else:
        st.warning("댓글을 입력해주세요.")