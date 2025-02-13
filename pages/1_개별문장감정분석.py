import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import os

# -- 모델, 토크나이저 로드 (캐싱 권장) --
@st.cache_resource
def load_sentiment_model():
    model_path = os.path.join("models", "sentiment_model.h5")
    return load_model(model_path)

@st.cache_resource
def load_tokenizer():
    tokenizer_path = os.path.join("models", "tokenizer.pkl")
    with open(tokenizer_path, "rb") as file:
        return pickle.load(file)

model = load_sentiment_model()
tokenizer = load_tokenizer()

def analyze_sentiment(text):
    """
    단일 문장(텍스트)에 대해 감정분석을 수행.
    결과(긍정/부정/중립)와 예측 스코어(%)를 반환합니다.
    """
    input_seq = tokenizer.texts_to_sequences([text])
    input_padded = pad_sequences(input_seq, maxlen=100)

    prediction = model.predict(input_padded)[0][0]  # 0~1 사이 값
    if prediction > 0.55:
        sentiment = "긍정"
    elif prediction < 0.45:
        sentiment = "부정"
    else:
        sentiment = "중립"
    
    prediction_percent = prediction * 100
    return sentiment, prediction_percent

def run_text_analysis():
    st.title("개별 문장 감정 분석")
    user_input = st.text_area("감정을 분석할 문장을 입력하세요:")

    if st.button("분석하기"):
        if user_input.strip():
            sentiment, score = analyze_sentiment(user_input.strip())
            st.write("### 분석 결과")
            st.write(f"- 감정 상태: **{sentiment}**")
            st.write(f"- 점수 (0~100%): **{score:.2f}%**")
        else:
            st.warning("문장을 입력해주세요.")

# Streamlit에서 실행될 함수
if __name__ == "__main__":
    run_text_analysis()