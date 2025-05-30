# Copyright [2025-05-28] [monologg]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from googleapiclient.discovery import build
import urllib.parse as urlparse
import pandas as pd
import altair as alt
import onnxruntime as ort
from transformers import AutoTokenizer
import numpy as np
import os
from googleapiclient.errors import HttpError
import time
import random
import json
from azure.storage.blob import BlobServiceClient
from pathlib import Path

MODEL_PATH = Path("models/koelectra.onnx")
CONTAINER_NAME = "models"
BLOB_NAME = "koelectra.onnx"

def download_model_from_blob():
    conn_str = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    service = BlobServiceClient.from_connection_string(conn_str)
    container = service.get_container_client(CONTAINER_NAME)
    MODEL_PATH.parent.mkdir(exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        f.write(container.get_blob_client(BLOB_NAME).download_blob().readall())

# Download the model if not already present
if not MODEL_PATH.exists():
    download_model_from_blob()

# 만약 모델의 크기가 너무 작다면 Blob에서 다시 내려받는다.
def should_download():
    return not MODEL_PATH.exists() or MODEL_PATH.stat().st_size < 1_000_000

if should_download():
    download_model_from_blob()

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
    if neg > pos and neg > 0.75:
        label = "부정"
    elif pos >= neg:
        label = "긍정"
    else:
        label = "중립"
    return label, prob


##################################
#  Youtube API 관련
##################################
API_key = "AIzaSyBrafWWm7JMMHCSe4SpB6vfqfx4YroAOoM"  # 실제 값으로 교체
youtube = build("youtube", "v3", developerKey=API_key)

def get_video_id_from_url(url: str):
    parsed_url = urlparse.urlparse(url)
    query_dict = urlparse.parse_qs(parsed_url.query)
    video_id_list = query_dict.get("v")
    if video_id_list and len(video_id_list) > 0:
        return video_id_list[0]
    return None

def get_comments_by_video_id(video_id, max_results=50):
    comments = []
    page_token = None
    while True:
        # Build request parameters
        params = {
            "part": "snippet,replies",
            "videoId": video_id,
            "maxResults": max_results,
            "textFormat": "plainText",
            "order": "time"
        }
        if page_token:
            params["pageToken"] = page_token

        # Retry loop for transient errors
        for attempt in range(3):
            try:
                request = youtube.commentThreads().list(**params)
                response = request.execute()
                break
            except HttpError as e:
                # Parse error reason
                try:
                    err = json.loads(e.content.decode())
                    reason = err["error"]["errors"][0].get("reason", "")
                except:
                    raise
                if reason == "processingFailure":
                    backoff = (2 ** attempt) + random.random()
                    time.sleep(backoff)
                    continue
                else:
                    raise
        else:
            raise RuntimeError("댓글을 가져오는 중 반복 오류가 발생했습니다.")

        # Extract comments
        for item in response.get("items", []):
            top_comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(top_comment)
            if "replies" in item:
                for reply_item in item["replies"]["comments"]:
                    comments.append(reply_item["snippet"]["textDisplay"])

        # Next page or break
        page_token = response.get("nextPageToken")
        if not page_token:
            break

    return comments

def run_youtube_analysis():
    st.title("📑 유튜브 영상 댓글 감정 분석")

    # 사용방법 설명하는 사이드바
    with st.sidebar:
        st.subheader("사용 방법")
        sidebar_url = st.text_area("", value="여기에 유튜브 url을 입력하세요!")

        # 분석하기 버튼 & 오른쪽에 "👈클릭!"
        col_sb1, col_sb2 = st.columns([3, 1])
        with col_sb1:
            sidebar_btn1 = st.button("'유튜브 댓글 추출 & 감정 분석'")
        with col_sb2:
            st.write("👈 클릭!")

        # 분석 결과
        st.markdown("---")
        st.subheader("분석 결과 (예시)")
        st.image("img/page2_result_count.png")
        st.image("img/page2_result_chart.png")
        st.image("img/page2_result_text.png")

        # 초기화 방법 표시
        st.markdown("---")
        st.subheader("다시 작성하고싶다면?")
        col_sb3, col_sb4 = st.columns([1, 2])
        with col_sb3:
            sidebar_btn2 = st.button("'초기화'")
        with col_sb4:
            st.write("👈 클릭!")


    youtube_url = st.text_input("""분석할 YouTube 링크를 입력하세요 (예시)\n
                                https://www.youtube.com/watch?v=fvaJDMD5xSk\n
                                """)

    # 버튼 레이아웃 (분석하기 + 초기화 버튼 나란히)
    col1, col2, col3 = st.columns([3, 3, 1])

    with col1:
        if st.button("유튜브 댓글 추출 & 감정 분석"):
            if not youtube_url.strip():
                st.warning("YouTube 링크를 입력해주세요.")
            else:
                video_id = get_video_id_from_url(youtube_url)
                if not video_id:
                    st.error("유효한 유튜브 URL이 아닙니다. v= 파라미터가 없습니다.")
                else:
                    st.session_state["YouTube_result"] = {
                        "video_id": video_id
                    }
                    st.session_state["youtube_url"] = youtube_url
                    st.session_state["popup_shown"] = False  # 팝업 초기화

    with col3:
        if st.button("초기화"):
            st.session_state["youtube_url"] = ""
            st.session_state.pop("YouTube_result", None)
            st.rerun()

    if "YouTube_result" in st.session_state:
        with st.spinner("댓글을 가져오고 있습니다..."):
            result = st.session_state["YouTube_result"]
            video_id = result["video_id"]
            comments = get_comments_by_video_id(video_id, max_results=50)
        
            if len(comments) == 0:
                st.warning("댓글이 없거나, 댓글 설정이 비활성화된 영상일 수 있습니다.")
            else:
                st.success(f"총 {len(comments)}개의 댓글을 가져왔습니다.")
                
                sentiments_result = []
                with st.spinner("댓글 감정 분석중..."):
                        for cmt in comments:
                            s_label, s_score = analyze_sentiment(cmt)
                            sentiments_result.append((cmt, s_label, s_score))
                
                # 통계
                total_count = sum(1 for _, label, _ in sentiments_result)
                pos_count = sum(1 for _, label, _ in sentiments_result if label == "긍정")
                neg_count = sum(1 for _, label, _ in sentiments_result if label == "부정")
                neu_count = sum(1 for _, label, _ in sentiments_result if label == "중립")

                if neg_count/total_count*100 >= 15:
                    st.error("시청에 주의가 필요합니다!")
                else:
                    st.info("시청에 문제가 없습니다!")

                st.markdown(
                    "<h3 style='margin-top:0;'>차트</h3>",
                    unsafe_allow_html=True
                )
                                
                # 차트 시각화
                df = pd.DataFrame({
                    "Sentiment": ["Positive", "Negative", "Neutral"],
                    "Percent": [
                        float(f"{(pos_count/total_count * 100):.2f}"),
                        float(f"{(neg_count/total_count * 100):.2f}"),
                        float(f"{(neu_count/total_count * 100):.2f}")
                    ]
                })

                chart = (
                    alt.Chart(df)
                    .mark_arc(stroke="black", strokeWidth=2)  # 테두리를 검정색, 두께 2로 설정
                    .encode(
                        theta=alt.Theta(field="Percent", type="quantitative"),
                        color=alt.Color(
                            field="Sentiment",
                            type="nominal",
                            scale=alt.Scale(
                                domain=["Positive", "Negative", "Neutral"],
                                range=["#ADD8E6", "#FFA07A", "gray"]  # 연한 파란색, 연한 빨간색, 회색
                            ),
                            legend=alt.Legend(labelColor="black", titleColor="black")  # 범례 텍스트를 진하게 설정
                        ),
                        tooltip=["Sentiment", "Percent"]
                    )
                    .properties(width=400, height=400)
                )

                st.altair_chart(chart, use_container_width=True)
                
                # 분석 결과 박스 (한 번의 HTML 마크다운으로 렌더링)
                html_summary = (
                    "<div style='border:1px solid #ccc; padding:15px; border-radius:8px; "
                    "background-color:#fafafa;'>"
                    "<h3 style='margin-top:0;'>분석 결과</h3>"
                    f"<p style='margin:4px 0;'><strong>총 댓글 수: {total_count}개</strong></p>"
                    f"<p style='margin:4px 0;'><span style='color:blue; font-weight:bold;'>긍정</span> "
                    f"적인 댓글: {pos_count}개</p>"
                    f"<p style='margin:4px 0;'><span style='color:red; font-weight:bold;'>부정</span> "
                    f"적인 댓글: {neg_count}개</p>"
                    f"<p style='margin:4px 0;'><span style='font-weight:bold;'>중립</span> "
                    f"적인 댓글: {neu_count}개</p>"
                    "</div>"
                    "<br>"
                    "<br>"
                )
                st.markdown(html_summary, unsafe_allow_html=True)
                
                # 예시 댓글 출력 (HTML 박스 전체 생성 후 한 번에 렌더링)
                html_comments = "<div style='border:1px solid #ccc; padding:15px; border-radius:8px; background-color:#f9f9f9;'>"
                html_comments += "<h3 style='margin-top:0;'>예시 댓글</h3>"
                for i, (comment_text, label, s_score) in enumerate(sentiments_result[:10], start=1):
                    # 댓글 본문
                    html_comments += f"<p style='margin-bottom:4px;'><strong>{i}. {comment_text}</strong></p>"
                    # 감정 레이블
                    color = 'blue' if label == '긍정' else 'red' if label == '부정' else 'gray'
                    html_comments += f"<p style='margin-top:0; margin-bottom:8px;'><span style='color:{color}; font-weight:bold;'>{label}</span> (s_score: {s_score:.2f}%)</p>"
                    html_comments += "<br>"
                html_comments += "</div>"
                st.markdown(html_comments, unsafe_allow_html=True)
                        

if __name__ == "__main__":
    run_youtube_analysis()