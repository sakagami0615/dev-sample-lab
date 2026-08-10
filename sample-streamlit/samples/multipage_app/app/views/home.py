import streamlit as st


def home_page():
    st.title("Multipage App Sample")
    st.write(
        "This sample demonstrates Streamlit's `st.navigation` API. "
        "Use the sidebar to switch between pages."
    )
    st.markdown(
        """
        - **Home** — this page
        - **Data View** — browse a pandas DataFrame with a simple filter
        - **Form** — submit a form and see the result via `st.session_state`
        """
    )
