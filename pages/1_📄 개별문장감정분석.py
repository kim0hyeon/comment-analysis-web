import streamlit as st
import os
import plotly.graph_objects as go
import onnxruntime as ort
from transformers import AutoTokenizer
import numpy as np

# -- 모델, 토크나이저 로드 (캐싱 권장) --
@st.cache_resource
def load_tokenizer_and_session():
    tokenizer = AutoTokenizer.from_pretrained(
        "Copycats/koelectra-base-v3-generalized-sentiment-analysis"
    )
    session = ort.InferenceSession(os.path.join("models", "koelectra.onnx"))
    return tokenizer, session

tokenizer, ort_session = load_tokenizer_and_session()

def analyze_sentiment(text):
    enc = tokenizer(
        text,
        return_tensors="np",
        padding=True,
        truncation=True,
        max_length=128
    )
    logits = ort_session.run(
        None,
        {"input_ids": enc["input_ids"], "attention_mask": enc["attention_mask"]}
    )[0]
    probs = np.exp(logits) / np.exp(logits).sum(axis=1, keepdims=True)
    neg, pos = probs[0]
    prob = max(neg, pos) * 100
    if neg > pos and neg > 0.9:
        sentiment = "부정"
    elif pos >= neg:
        sentiment = "긍정"
    else:
        sentiment = "중립"
    return sentiment, prob

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
    st.title("📄 개별 문장 감정 분석")

    # 사이드바를 사용방법 설명으로 꾸미기
    with st.sidebar:
        st.subheader("사용 방법")

        # 문장 입력란 (기본 문구)
        sidebar_comment = st.text_area("", value="여기에 댓글을 입력하세요!")

        # 분석하기 버튼 & 오른쪽에 "👈클릭!"
        col_sb1, col_sb2 = st.columns([1, 2])
        with col_sb1:
            sidebar_btn1 = st.button("'분석하기'")
        with col_sb2:
            st.write("👈 클릭!")
        
        # 결과 표시
        st.markdown("---")
        st.subheader("분석 결과 (예시)")
        st.image("img/page1_result_chart.png")
        st.image("img/page2_result_text.png")

        # 초기화 방법 표시
        st.markdown("---")
        st.subheader("다시 작성하고싶다면?")
        col_sb3, col_sb4 = st.columns([1, 2])
        with col_sb3:
            sidebar_btn2 = st.button("'초기화'")
        with col_sb4:
            st.write("👈 클릭!")


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

                st.session_state["individual_result"] = {
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
            st.session_state.pop("individual_result", None)
            st.rerun()

    # 🔥 분석 결과 출력 (세션 상태 활용)
    if "individual_result" in st.session_state:
        result = st.session_state["individual_result"]
        st.write("### 분석 결과")
        st.plotly_chart(result["fig"])

        if result["sentiment"] == "긍정":
            st.write(f"- 감정 상태: **:blue[{result['sentiment']}]**")
            st.write(f"- 긍정 확률: **:blue[{result['score']:.2f}%]**")
        elif result["sentiment"] == "부정":
            st.write(f"- 감정 상태: **:red[{result['sentiment']}]**")
            st.write(f"- 부정 확률: **:red[{result['score']:.2f}%]**")
        else:
            st.write(f"- 감정 상태: **{result['sentiment']}**")
            st.write(f"- 중립 확률: **{(100 - result['score']):.2f}%**")
        

# Streamlit에서 실행될 함수
if __name__ == "__main__":
    run_text_analysis()