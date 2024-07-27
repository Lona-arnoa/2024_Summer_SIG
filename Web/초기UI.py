import streamlit as st
from langchain_core.messages import ChatMessage

st.set_page_config(page_title="present picks", page_icon="🎁")

# 웹 폰트 설정
st.markdown('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display&display=swap">', unsafe_allow_html=True)

# 말풍선 폰트 설정
st.markdown('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+KR&display=swap">', unsafe_allow_html=True)

# 제목 및 부제목 표시
st.markdown("""
    <h1 style='text-align: center; font-family: "Playfair Display", sans-serif; color: #000080; font-size: 75px;'>
        Present Picks
    </h1>
    <h2 style='text-align: center; font-family: "Playfair Display", sans-serif; color: #6495ED; font-size: 30px;'>
         - Tailored Gifts for Every Personality -
    </h2>
""", unsafe_allow_html=True)

# 구분선 표시
st.markdown("<hr style='border: 1.5px solid black;'>", unsafe_allow_html=True)

# 세션 상태 초기화
if "messages" not in st.session_state: 
    st.session_state["messages"] = []
if "sidebar_messages" not in st.session_state:
    st.session_state["sidebar_messages"] = []

# 인사말 출력
if len(st.session_state["messages"]) == 0:
    greeting_message = ChatMessage(role="assistant", content="안녕하세요! 선물이 고민될 땐 언제든 물어봐주세요!")
    st.session_state["messages"].append(greeting_message)

def print_messages():
    # 메시지 출력
    if "messages" in st.session_state and len(st.session_state["messages"]) > 0:
        for chat_message in st.session_state["messages"]:
            if chat_message.role == "user":
                alignment = 'flex-end'  # 오른쪽 정렬
                bubble_color = '#87CEEB'
                icon = "😄"
                message_html = f"""
                    <div style='display: flex; align-items: center; justify-content: {alignment};'>
                        <div style='display: inline-block; max-width: 90%; background-color: {bubble_color}; padding: 10px; border-radius: 10px; margin: 10px;'>
                             <p style='margin: 0; font-weight: bold; font-family: "Noto Serif KR", sans-serif;'>{chat_message.content}</p>
                        </div>
                        <div style='font-size: 2em; margin-left: 10px;'>{icon}</div>
                    </div>
                """
            else: 
                alignment = 'flex-start'  # 왼쪽 정렬
                bubble_color = '#B0C4DE'
                icon = "🤖"
                message_html = f"""
                    <div style='display: flex; align-items: center; justify-content: {alignment};'>
                        <div style='font-size: 2em; margin-right: 10px;'>{icon}</div>
                        <div style='display: inline-block; max-width: 90%; background-color: {bubble_color}; padding: 10px; border-radius: 10px; margin: 10px;'>
                             <p style='margin: 0; font-weight: bold; font-family: "Noto Serif KR", sans-serif;'>{chat_message.content}</p>
                        </div>
                    </div>
                """
            st.markdown(message_html, unsafe_allow_html=True)

def update_sidebar():
    st.sidebar.markdown("""
        <style>
            .sidebar-header {
                text-align: center; 
                margin-bottom: 0px; 
                font-family: "Playfair Display", sans-serif; 
                color: #000080; 
            }
            hr {
                margin-top: 0px; /* 줄 위쪽 간격 조정 */
                margin-bottom: 20px; /* 줄 아래쪽 간격 조정 */
            }
            .sidebar-message {
                text-align: center; 
                font-family: "Noto Serif KR", sans-serif; 
                font-size: 16px; 
                margin-bottom: 5px; 
            }
        </style>
        <h2 class='sidebar-header'>Recent products</h2>
        <hr style='border: 1.5px solid black;'>
    """, unsafe_allow_html=True)


    # 사이드바에 최근 상품 정보 출력
    if "sidebar_messages" in st.session_state:
        for message in st.session_state["sidebar_messages"]:
            st.sidebar.markdown(f"<div class='sidebar-message'>{message}</div>", unsafe_allow_html=True)

# 사용자 입력 처리
if user_input := st.chat_input("질문을 입력하세요."):
    user_message = ChatMessage(role="user", content=user_input)
    st.session_state["messages"].append(user_message)

    # AI 응답 
    assistant_response = ChatMessage(role="assistant", content=f"답변: {user_input}에 대한 정보입니다.")
    st.session_state["messages"].append(assistant_response)
    
    # 사이드바에 응답 추가
    st.session_state["sidebar_messages"].append(assistant_response.content)

    # 새로운 메시지 추가 후 메시지 출력
    print_messages()
    update_sidebar()
else:
    # 사용자 입력이 없을 경우 메시지 출력
    print_messages()
    update_sidebar()
