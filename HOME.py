import streamlit as st

# 페이지 설정은 Streamlit 명령 중 가장 먼저 호출하는 것이 권장됩니다.
st.set_page_config(
    page_title="프로젝트 소개",
    layout="centered"
)

def main():
    # 메인 타이틀
    st.title("🔥 프로젝트 소개")

    with st.sidebar:
        # 노션 페이지 연결
        st.subheader("프로젝트에 대한 더 자세한 설명 ！")
        
        # 각 링크의 텍스트와 연결될 URL을 직접 넣어주시면 됩니다.
        st.write("💭 [Microsoft Azure와의 연동](https://chain-maple-8e6.notion.site/Microsoft-Azure-18e76c8cc99f802d9642e4f5de7b62ae) 👈click!")
        st.write("🇰🇷 [감정 분석 모델](https://chain-maple-8e6.notion.site/koelectra-base-v3-generalized-sentiment-analysis-1e476c8cc99f807bbcbae9360a57cbd7?source=copy_link) 👈 click!")
        st.write("💾 [YouTube API와 연동](https://chain-maple-8e6.notion.site/YouTube-Data-API-19b76c8cc99f809db281ca8eba3f3d9b?pvs=4) 👈 click!")
        st.write("🫙 [GitHub 저장소](https://github.com/kim0hyeon/comment-analysis-web) 👈 click!")
        st.markdown("---")
        st.image("img/hanyang_logo.png")


    # 팀 소개
    st.subheader("팀명: 쏘세지야채볶음")
    st.write("**이름**: 김영현")
    st.write("**학번**: 2020006108")
    st.write("**지도교수**: 박서연 교수님")

    st.markdown("---")

    # 추가로 넣으면 좋을 것 같은 내용 제안
    st.subheader("**프로젝트의 :red[배경] 및 :red[목표]**")
    st.markdown("""
            - **:red[프로젝트 계획 배경]**

            이 프로젝트를 선정한 이유는 다음과 같습니다.

            첫째, YouTube에는 12세 미만 어린이를 위한 'YouTube Kids' 서비스가 있어 부적절한 영상 노출을 방지합니다. 그러나 성인을 대상으로 한

            유사한 필터링 기능은 제공되지 않고 있습니다. 실제로 성인 시청자들도 성인용 콘텐츠 중에 불건전하거나 자극적인 썸네일 낚시 영상에 노출되는 경우가 많습니다.
                
            한편 '좋아요, 싫어요' 기반의 평가는 있지만, 싫어요 수는 공개되지 않아 시청 전 해당 영상의 문제점을 파악하기 어렵습니다. 따라서 시청자들이 남긴
                
            댓글을 사전 분석하여 불건전 영상을 미리 경고한다면, 보다 안전한 시청 환경을 제공할 수 있다고 판단했습니다.

            둘째, YouTube Premium 구독료가 초기 8,900원에서 14,900으로 크게 인상되면서, 광고 차단 앱 사용이나 저가 해외 구독 등 편법을 이용하는 사례가 늘고                

            있습니다. 현재 Premium이 제공하는 핵심 기능(광고 제거, 오프라인 저장, 백그라운드 재생)은 일반 사용자들에게 차별적 가치를 제공하기에 다소 부족합니다.
                
            이때, '불건전 영상 식별'기능을 Premium 전용 혜택으로 추가한다면, 구독자가 체감하는 서비스 가치를 높여 합리적인 구독 비용으로 받아들일 수 있을 것으로
                
            기대합니다.
            """)
    st.markdown("""                
            \n\n\n
                
            - **:red[프로젝트 수행 및 목표]**
                
            한국어 감정 분석 모델을 이용해서 긍정적인 댓글, 큰 감정표현이 없는 중립적인 댓글, 어떤 사람이 보더라도 부적절해 보이는 부정적인 댓글로 분류합니다.

            YouTube API를 이용해 YouTube 링크를 입력하면 해당 영상의 댓글을 불러와 댓글 감정 분석 모델이 분석해 긍정적인 댓글의 비율, 부정적인 댓글의 비율, 중립적인 댓글의 비율을 보여줍니다.

            그리고 댓글 분석이 잘 이루어진건지 확인하고 싶은 사용자들을 위해 예시 댓글 10개를 불러와 해당 댓글을 어떤 감정 상태로 분석했는지 샘플을 보여줍니다.

            이 프로젝트의 목표는 감정 분석 모델의 신뢰성을 보여주어 "YouTube에 이 기능을 추가해 볼만 하다"라는 생각이 들게끔 하는 것입니다.
                
            비록 YouTube 앱에 직접 적용해 볼 순 없었지만, Microsoft Azure를 이용해 웹을 배포함으로써 사용자들이 어디서든 부적절한 영상인지 확인할 수 있게끔 대체하였습니다.
             """)
    
    st.markdown("---")
    st.image("img/hanyang_logo.png")
    
    

if __name__ == "__main__":
    main()