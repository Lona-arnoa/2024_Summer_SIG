import streamlit as st
from langchain_core.messages import ChatMessage

st.set_page_config (page_title = "GiftMatch", page_icon = "🎁")
    
st.title("_Gift Match :blue[QnA]_ 🎁")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "greeting_displayed" not in st.session_state:
    st.session_state["greeting_displayed"] = False

def print_messages():
    # 이전 대화기록을 출력해 주는 코드
    if "messages" in st.session_state and len(st.session_state["messages"]) > 0:
    #    for role, message in st.session_state["messages"]:
         for chat_message in st.session_state["messages"]:
        #    st.chat_message(role).write(message)
             st.chat_message(chat_message.role).write(chat_message.content)

print_messages()           

if not st.session_state["greeting_displayed"]:
    with st.chat_message("assistant"):
        st.write("안녕하세요! 선물이 고민될 땐 언제든 물어봐주세요!")
    st.session_state["greeting_displayed"] = True

if user_input := st.chat_input("질문을 입력하세요."):
    # 사용자가 입력한 내용
    st.chat_message("user").write(f"{user_input}")
    # st.session_state["messages"].append(("user", user_input))
    st.session_state["messages"].append(ChatMessage(role="user", content=user_input))

    # LLM을 사용하여 AI의 답변을 생성
# 36줄 주석 추가함.

    # AI의 답변
    with st.chat_message("assistant"):
        msg = f"당신이 입력한 내용: {user_input}"
        st.write(msg)
        # st.session_state["messages"].append(("assistant", msg))
        st.session_state["messages"].append(ChatMessage(role="assistant", content=msg))