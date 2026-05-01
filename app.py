import streamlit as st
import uuid
from userfuc import message_box

st.set_page_config(page_title="ChatGPT Style Chat", layout="wide")

st.title("💬 Chat")

# ---------- SESSION INIT ----------
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "chat_order" not in st.session_state:
    st.session_state.chat_order = []

if "current_chat_id" not in st.session_state:
    new_id = str(uuid.uuid4())
    st.session_state.current_chat_id = new_id
    st.session_state.chats[new_id] = {"messages": [], "title": "New Chat"}
    st.session_state.chat_order.insert(0, new_id)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.header("💬 Chats")

    # ➕ New Chat
    if st.button("➕ New Chat"):
        new_id = str(uuid.uuid4())
        st.session_state.current_chat_id = new_id
        st.session_state.chats[new_id] = {"messages": [], "title": "New Chat"}
        st.session_state.chat_order.insert(0, new_id)  # put on top
        st.rerun()

    st.divider()

    # 📜 Chat List (latest first)
    for chat_id in st.session_state.chat_order:
        chat = st.session_state.chats[chat_id]

        if chat["title"]=="New Chat":
            continue;

        if st.button(chat["title"], key=chat_id) :
            st.session_state.current_chat_id = chat_id
            st.rerun()

# ---------- CURRENT CHAT ----------
current_chat = st.session_state.chats[st.session_state.current_chat_id]
messages = current_chat["messages"]

# ---------- DISPLAY CHAT ----------
for msg in messages:
    with st.chat_message(msg["role"]):
        message_box(msg["role"],msg["content"])

# ---------- USER INPUT ----------
prompt = st.chat_input("Enter your message...")

if prompt:
    # Save user message
    messages.append({"role": "user", "content": prompt})

    # Auto title (first message only)
    if current_chat["title"] == "New Chat":
        current_chat["title"] = prompt[:30] + "..." if len(prompt) > 30 else prompt

    with st.chat_message("user"):
        message_box("user",prompt)

    # Fake response
    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            response = f"{prompt}"
            message_box("assistant",response)
            

    messages.append({"role": "assistant", "content": response})