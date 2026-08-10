import streamlit as st

from views.data_view import data_view_page
from views.form_view import form_page
from views.home import home_page

st.set_page_config(page_title="Multipage App Sample", page_icon="📄")

pages = [
    st.Page(home_page, title="Home", icon="🏠", default=True),
    st.Page(data_view_page, title="Data View", icon="📊"),
    st.Page(form_page, title="Form", icon="📝"),
]

nav = st.navigation(pages)
nav.run()
