import streamlit as st

def login():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = None

    if st.session_state.authenticated:
        return True

    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = st.secrets["auth"]["users"]

        matched_user = next(
            (u for u in users if u["username"] == username and u["password"] == password),
            None
        )

        if matched_user:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Invalid username or password")

    return False


def logout():
    st.session_state.authenticated = False
    st.session_state.username = None
    st.rerun()


def require_auth():
    if not login():
        st.stop()