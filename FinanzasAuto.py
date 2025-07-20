import streamlit as st
import pandas as pd

# ─── Page Setup ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Auto-Fin Dashboard", layout="wide")
st.title("Auto-Fin Dashboard")
st.image(
    "https://raw.githubusercontent.com/jagm1421/Auto-Fin/main/logo.png",
    caption="Logo de Auto-Fin",
    use_container_width=True,
)
st.markdown("## 🔐 Secure Login System")

# ─── Session-State Defaults ────────────────────────────────────────────────────
for key, default in {
    "logged_in": False,
    "username":  None,
    "role":      None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ─── Login Page ────────────────────────────────────────────────────────────────
def login_page():
    st.subheader("Login")

    # wrap inputs in a form so they don't vanish mid-click
    with st.form("login_form", clear_on_submit=False):
        user = st.text_input("Username")
        pwd  = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        users = st.secrets["users"]

        if user not in users:
            st.error("❌ Username not found")
            return

        if pwd != users[user]["password"]:
            st.error("❌ Incorrect password")
            return

        # ✅ Success path
        st.session_state.logged_in = True
        st.session_state.username  = user
        st.session_state.role      = users[user]["role"]
        st.success(f"Logged in as **{st.session_state.role}**")

        # NEW: explicit rerun if you want to jump straight to upload_page()
        st.rerun()

# ─── Upload Page ───────────────────────────────────────────────────────────────
def upload_page():
    st.subheader("📤 Upload Your Excel File")

    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            st.success("✅ File uploaded and read successfully!")
            st.dataframe(df)
        except Exception as e:
            st.error(f"❌ Error reading Excel file: {e}")

    if st.button("Logout"):
        for key in ("logged_in", "username", "role"):
            st.session_state[key] = None
        st.rerun()

# ─── App Entry ────────────────────────────────────────────────────────────────
if st.session_state.logged_in:
    upload_page()
else:
    login_page()