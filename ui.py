import requests
import streamlit as st
from configs.app_config import AppConfig

conf = AppConfig()
API = conf.RAG_APP_URL

st.session_state.setdefault("user", None)


def login_view():
    st.title("Đăng nhập")
    with st.form("login"):
        email = st.text_input("Email")
        password = st.text_input("Mật khẩu", type="password")
        submitted = st.form_submit_button("Đăng nhập", type="primary")

    if submitted:
        try:
            r = requests.post(
                f"{API}/user/login",
                json={"email": email, "password": password},
                timeout=30,
            )
        except Exception as e:
            st.error(f"Không kết nối được server: {e}")
            return

        if not r.ok:
            st.error("Sai email hoặc mật khẩu")
        elif r.json()["role"] != "admin":
            st.error("Tài khoản này không phải admin")
        else:
            st.session_state.user = r.json()
            st.rerun()


def upload_view():
    col1, col2 = st.columns([5, 1])
    col1.title("Upload tài liệu")
    col1.caption(f"Đăng nhập: {st.session_state.user['email']}")
    if col2.button("Đăng xuất"):
        st.session_state.user = None
        st.rerun()

    uploaded_files = st.file_uploader(
        "Upload files", accept_multiple_files=True, type=["pdf"]
    )

    if st.button("Upload tất cả", type="primary"):
        for f in uploaded_files:
            try:
                r = requests.post(
                    f"{API}/files/upload",
                    files={"file": (f.name, f.getvalue(), f.type or "application/pdf")},
                    timeout=300,
                )
                if r.ok:
                    st.success(f.name)
                    st.json(r.json())
                else:
                    st.error(f"{f.name}: {r.status_code}")
                    st.code(r.text)
            except Exception as e:
                st.json({"error": str(e)})

        try:
            requests.post(f"{API}/ingest", timeout=300)
        except Exception as e:
            st.json({"state": "ingest", "error": str(e)})


if st.session_state.user:
    upload_view()
else:
    login_view()