import streamlit as st
import requests

api_url = "https://hanyang-language-001.cognitiveservices.azure.com/language/:query-knowledgebases?projectName=SEOUL-FAQ&api-version=2021-10-01&deploymentName=production"
api_key = "ALRcv7L1DuXo6VYAlDtCBsAH0PzO2XaYUqDmiQ9EaAnqREWzkzgHJQQJ99BAACYeBjFXJ3w3AAAaACOGtKFb"

# 헤더 부분의 설정
headers = {
    "Ocp-Apim-Subscription-Key": api_key,
    "Content-Type": "application/json"
}

def ask_question(question):
    payload = {
        "question": question
    }

    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["answers"][0]["answer"]
    else:
        return "Error: Unable to get a response"

# UI 부분
st.title("SEOUL FAQ Question & Answer")
st.write("서울시 관광과 관련된 궁금한 사항을 물어보세요")

# 질문을 입력받는 부분
question = st.text_input("Ask a question about SEOUL!")
button_click = st.button("Query")

if button_click:
    with st.spinner('Wait for it...'):
        answer  = ask_question(question)
        st.write(f"Answer: {answer}")
        st.success("Done!")

