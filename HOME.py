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
        st.write("🇰🇷 [한국어 댓글 감정 분석 모델](https://chain-maple-8e6.notion.site/18f76c8cc99f80b09953c630f0f43ef0?pvs=4) 👈 click!")
        st.write("📜 [Page 구성](https://chain-maple-8e6.notion.site/Page-19a76c8cc99f80e4aa43f3a89a2d2be3?pvs=4) 👈 click!")
        st.write("💾 [YouTube API와 연동](https://chain-maple-8e6.notion.site/YouTube-Data-API-19b76c8cc99f809db281ca8eba3f3d9b?pvs=4) 👈 click!")
        st.write("🫙 [GitHub 저장소](https://github.com/kim0hyeon/comment-analysis-web) 👈 click!")
        st.markdown("---")
        st.image("img/hanyang_logo.png")


    # 팀 소개
    st.subheader("팀명: 쏘세지야채볶음")
    st.write("**이름**: 김영현")
    st.write("**학번**: 2020006108")

    st.markdown("---")

    # 추가로 넣으면 좋을 것 같은 내용 제안
    st.subheader("**프로젝트의 :red[배경] 및 :red[목표]**")
    st.markdown("""
            - **:red[프로젝트 계획 배경]**

            이 아이디어는 YouTube Kids 서비스에서 떠올렸습니다. 현재 YouTube에는 YouTube Kids라는 서비스를 제공합니다.

            YouTube Kids에서는 12세 미만의 아이들이 부적절한 영상에 노출되지 않도록 영상 알고리즘을 제한합니다.

            하지만 요즘 YouTube에 게시되는 영상들 중엔 성인들도 시청하고 싶지 않은 썸네일 낚시 영상이나 콘텐츠 내용 자체가 부적절한 영상도 많습니다.

            그래서 이런 영상들을 시청하기 전에 미리 알림을 받을 수 있다면 어떨까? 하는 생각에서 이 아이디어를 떠올렸습니다.

            게다가 YouTube 프리미엄의 구독 가격이 점점 올라 8,900원에서 14,900원까지 상승했습니다. 또, 돈을 내지 않고 광고를 제거하는 광고 차단 앱을 사용하는 사용자들도 많이 늘었습니다.

            현재 YouTube 프리미엄 사용자들에게만 제공하는 기능은 광고 없는 시청, 오프라인 저장, 백그라운드 재생 등 일반 사용자들과 비교해 차별성이 적다고 보여집니다.

            그런 점에서 부적절한 영상 체크 기능을 YouTube Premium 사용자들에게 제공한다면, 사용자들이 더 납득할만한 구독 서비스로 받아들일 수 있을 것입니다.
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