import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import os
import plotly.graph_objects as go

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
    if prediction > 0.6:
        sentiment = "긍정"
    elif prediction < 0.4:
        sentiment = "부정"
    else:
        sentiment = "중립"
    
    prediction_percent = prediction * 100
    return sentiment, prediction_percent

def make_chart(score):
    # 가로 그래프 만들기
    positive = int(score)
    negative = 100 - int(score)

    # Figure 생성
    fig = go.Figure()

    # 긍정 (왼쪽)
    fig.add_trace(go.Bar(
        x=[positive],  # 🔥 숫자 값으로 유지
        y=["Sentiment"],
        orientation='h',
        name="Positive",
        marker=dict(color="#ADD8E6", line=dict(color="blue", width=1.5)),  # 테두리 추가
        text=[f"{positive}%"],  # 퍼센트 표시
        textposition="inside",
        insidetextanchor="middle"
    ))

    # 부정 (오른쪽)
    fig.add_trace(go.Bar(
        x=[negative],  # 🔥 숫자 값으로 유지
        y=["Sentiment"],
        orientation="h",
        name="Negative",
        marker=dict(color="#FFA07A", line=dict(color="red", width=1.5)),  # 테두리 추가
        text=[f"{negative}%"],  # 퍼센트 표시
        textposition="inside",
        insidetextanchor="middle"
    ))

    # 레이아웃 설정
    fig.update_layout(
        title="감정분석 차트",
        xaxis=dict(
            title="Percentage",
            tickmode="linear",  # 눈금 간격을 선형적으로 설정
            tick0=-100,            # 시작점 (0부터 시작)
            dtick=10,           # 10 단위로 눈금 생성
            range=[0,100],
            showgrid=True,      # 🔥 그리드 표시 활성화
            gridwidth=1,        # 🔥 그리드 선 두께
            gridcolor="gray",   # 🔥 그리드 선 색상 (연한 회색)
        ),
        yaxis=dict(
            showgrid=False  # Y축에는 그리드 표시하지 않음
        ),
        barmode="relative",
        showlegend=True,
        height=250
    )

    return fig

def run_text_analysis():
    st.title("개별 문장 감정 분석")

    # 🔥 세션 상태에 입력값 저장 (초기화 버튼을 위해 필요)
    if "user_input" not in st.session_state:
        st.session_state["user_input"] = ""

    # 입력 필드 (세션 상태 반영)
    user_input = st.text_area("감정을 분석할 문장을 입력하세요:", value=st.session_state["user_input"], key="input_text")

    # 버튼 레이아웃 (분석하기 + 초기화 버튼 나란히)
    col1, col2, col3 = st.columns([3, 3, 1])

    with col1:
        if st.button("분석하기"):
            if user_input.strip():
                sentiment, score = analyze_sentiment(user_input.strip())

                fig = make_chart(score)

                st.session_state["result"] = {
                    "sentiment": sentiment,
                    "score": score,
                    "fig": fig
                }
                st.session_state["user_input"] = user_input  # 🔥 입력값 유지
                
            else:
                st.warning("문장을 입력해주세요.")

    with col3:
        if st.button("초기화"):
            # 🔥 입력 필드 및 결과 초기화
            st.session_state["user_input"] = ""
            st.session_state.pop("result", None)
            st.rerun()

    # 🔥 분석 결과 출력 (세션 상태 활용)
    if "result" in st.session_state:
        result = st.session_state["result"]
        st.write("### 분석 결과")
        st.plotly_chart(result["fig"])

        if result["sentiment"] == "긍정":
            st.write(f"- 감정 상태: **:blue[{result['sentiment']}]**")
            st.write(f"- {result['sentiment']}적일 확률:  **:blue[{result['score']:.2f}%]**")
        elif result["sentiment"] == "부정":
            st.write(f"- 감정 상태: **:red[{result['sentiment']}]**")
            st.write(f"- {result['sentiment']}적일 확률:  **:red[{(100 - result['score']):.2f}%]**")
        else:
            st.write(f"- 감정 상태: **{result['sentiment']}**")
            st.write(f"- {result['sentiment']}적일 확률  **높음**")
        

# Streamlit에서 실행될 함수
if __name__ == "__main__":
    run_text_analysis()