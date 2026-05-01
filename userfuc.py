import streamlit as st

def message_box(role, content):
    if role == "user":
        st.markdown(
            f"""
            <div style='text-align: right;'>
                {content}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style='text-align: left;'>
                {content}
            </div>
            """,
            unsafe_allow_html=True
        )