import streamlit as st

# 페이지 설정은 Streamlit 명령 중 가장 먼저 호출하는 것이 권장됩니다.
st.set_page_config(
    page_title="프로젝트 소개",
    layout="centered"
)

def main():
    # 메인 타이틀
    st.title("🔥 프로젝트 소개")
    
    # 팀 소개
    st.subheader("팀명: 쏘세지야채볶음")
    st.write("**이름**: 김영현")
    st.write("**학번**: 2020006108")
    st.write("*(본 프로젝트는 1인 팀으로 진행됩니다.)*")

    st.markdown("---")

    # 추가로 넣으면 좋을 것 같은 내용 제안
    st.subheader("프로젝트 설명")
    st.write("**프로젝트의 배경 및 목표**")
    st.write("- **배경**: Microsoft Azure를 활용한 클라우드 서비스를 학습하고 댓글 감정 분석을 해주는 AI를 알게 되어 이 두 가지를 활용한 웹을 만들어보고 싶다는 마음에서 출발했습니다.")
    st.write("- **목표**: 직접 댓글 감정 분석 모델을 만들어서 Google API, Microsoft Azure와 GitHub Actionos를 이용해 일반 자유롭게 사용할 수 있게 하는 것")
    
    # 노션 페이지 연결(링크 자리만 마련)
    st.markdown("---")
    st.subheader("프로젝트에 대한 더 자세한 설명")
    
    # 각 링크의 텍스트와 연결될 URL을 직접 넣어주시면 됩니다.
    st.write("- [Microsoft Azure와 연결](https://chain-maple-8e6.notion.site/Microsoft-Azure-18e76c8cc99f802d9642e4f5de7b62ae)")
    st.write("- [한국어 댓글 감정 분석 모델](https://chain-maple-8e6.notion.site/18f76c8cc99f80b09953c630f0f43ef0?pvs=4)")
    st.write("- [Page작성](https://chain-maple-8e6.notion.site/Page-19a76c8cc99f80e4aa43f3a89a2d2be3?pvs=4)")
    
    
    

if __name__ == "__main__":
    main()