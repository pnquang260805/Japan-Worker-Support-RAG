import streamlit as st
from io import StringIO
from configs.app_config import AppConfig
import requests

conf = AppConfig()

uploaded_files = st.file_uploader(
"Upload files", accept_multiple_files=True, type=['pdf']
)

if st.button("Upload tất cả", type="primary"):
    for f in uploaded_files:
        try:
            response = requests.post(
                f"{conf.RAG_APP_URL}/files/upload",
                files={"file": (f.name, f.getvalue(), f.type or "application/pdf")},
                timeout=300
            )
            if response.ok:
                st.success(f"{f.name}")
                st.json(response.json())
            else:
                st.error(f"{f.name}: {response.status_code}")
                st.code(response.text)
        except Exception as e:
            st.json({"error": e})
    try:
        ingest_resq = requests.post(f"{conf.RAG_APP_URL}/ingest")
    except Exception as e:
        st.json({"state": "ingest", "error": e})
