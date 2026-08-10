import streamlit as st


def form_page():
    st.title("Form")
    with st.form("sample_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        submitted = st.form_submit_button("Submit")

    if submitted:
        st.session_state["last_submission"] = {"name": name, "age": age}

    if "last_submission" in st.session_state:
        st.success("Last submission:")
        st.json(st.session_state["last_submission"])
