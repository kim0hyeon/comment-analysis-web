import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# 1. 모델과 토크나이저 로드
model = load_model("models/sentiment_model.h5")

with open("models/tokenizer.pkl", "rb") as file:
    tokenizer = pickle.load(file)

# 2. Streamlit 앱 UI
st.title("당신의 댓글을 분석해드립니다!")
user_input = st.text_area("댓글을 입력하세요:")

# 3. 댓글 분석 수행
if st.button("분석하기"):
    if user_input.strip():
        # 입력 텍스트 전처리
        input_seq = tokenizer.texts_to_sequences([user_input])
        input_padded = pad_sequences(input_seq, maxlen=100)

        # 모델 예측 수행
        prediction = model.predict(input_padded)[0][0]

        # 결과 해석
        sentiment = "긍정" if prediction > 0.5 else "부정"

        if prediction > 0.6 :
            sentiment = "긍정"
        elif prediction < 0.4 :
            sentiment = "부정"
        else:
            sentiment = "중립"
        
        prediction *= 100 # %로 나타내기 위해 x100

        st.text("100%에 가까울수록 긍정적이고 0%에 가까울수록 부정적입니다.\n")
        st.success(f"댓글 감정 분석 결과: {sentiment} ({prediction:.4f}%)")
    else:
        st.warning("댓글을 입력해주세요.")
