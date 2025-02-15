import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
from googleapiclient.discovery import build
import urllib.parse as urlparse
import pandas as pd
import altair as alt
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
    input_seq = tokenizer.texts_to_sequences([text])
    input_padded = pad_sequences(input_seq, maxlen=100)
    prediction = model.predict(input_padded)[0][0]
    
    if prediction > 0.6:
        sentiment = "긍정"
    elif prediction < 0.4:
        sentiment = "부정"
    else:
        sentiment = "중립"
    
    prediction_percent = prediction * 100
    return sentiment, prediction_percent

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
    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=video_id,
        maxResults=max_results,
        textFormat="plainText",
        order="time"
    )
    response = request.execute()
    comments = []
    
    while True:
        for item in response.get("items", []):
            # 상위 댓글
            top_comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(top_comment)
            
            # 대댓글
            if "replies" in item:
                for reply_item in item["replies"]["comments"]:
                    reply_comment = reply_item["snippet"]["textDisplay"]
                    comments.append(reply_comment)
        
        if "nextPageToken" in response:
            next_page_token = response["nextPageToken"]
            request = youtube.commentThreads().list(
                part="snippet,replies",
                videoId=video_id,
                maxResults=max_results,
                pageToken=next_page_token,
                textFormat="plainText",
                order="time"
            )
            response = request.execute()
        else:
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


    youtube_url = st.text_input("분석할 YouTube 링크를 입력하세요 (예: https://www.youtube.com/watch?v=abcd1234)")

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
                
                st.subheader("분석 결과")
                st.write(f"***총 댓글 수: {total_count}개***")
                st.write(f"- **:blue[긍정]** 적인 댓글: **{pos_count}**개")
                st.write(f"- **:red[부정]** 적인 댓글: **{neg_count}**개")
                st.write(f"- **중립** 적인 댓글: **{neu_count}**개")

                st.markdown("---")

                st.subheader("차트")
                                
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
                                range=["#ADD8E6", "#FFA07A", "gray"]  # 연한 파란색, 연한 빨간색, 연한 회색
                            ),
                            legend=alt.Legend(labelColor="black", titleColor="black")  # 범례 텍스트를 진하게 설정
                        ),
                        tooltip=["Sentiment", "Percent"]
                    )
                    .properties(width=400, height=400)
                )

                st.altair_chart(chart, use_container_width=True)
                
                # 예시 댓글 출력
                st.write("### 예시 댓글")
                for i, (comment_text, label, s_score) in enumerate(sentiments_result[:10], start=1):
                    st.write(f"**{i}.** {comment_text}")
                    st.write(f" - 감정: {label}, 점수: {s_score:.2f}%\n")

if __name__ == "__main__":
    run_youtube_analysis()