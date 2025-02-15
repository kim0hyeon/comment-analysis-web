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
    st.write("""- **:red[배경]**: 학교 강의를 들으면서 Microsoft Azure를 활용한 클라우드 서비스를 학습하고 댓글 감정 분석을 해주는 AI를 알게 되었습니다.
             클라우드 기술을 활용해 직접 무언가를 배포해보고 싶다는 생각에 댓글의 감정을 분석해서 통계로 보여주는 웹 사이트를 만들어보면 좋겠다는 생각이 들어 이 프로젝트를 진행하게 되었습니다. """)
    st.write("- **:red[목표]**: 직접 댓글 감정 분석 모델을 만들어서 Google API, Microsoft Azure와 GitHub Actionos를 이용해 직접 웹 페이지를 배포해 보기")
    
    st.markdown("---")
    st.image("img/hanyang_logo.png")
    
    

if __name__ == "__main__":
    main()