import pandas as pd
import streamlit as st

_SAMPLE_DATA = pd.DataFrame(
    {
        "name": ["Alice", "Bob", "Carol", "Dave", "Eve"],
        "department": ["Engineering", "Sales", "Engineering", "Marketing", "Sales"],
        "age": [29, 34, 41, 26, 38],
    }
)


def data_view_page():
    st.title("Data View")
    departments = sorted(_SAMPLE_DATA["department"].unique())
    selected = st.multiselect("Department", departments, default=departments)
    filtered = _SAMPLE_DATA[_SAMPLE_DATA["department"].isin(selected)]
    st.dataframe(filtered, use_container_width=True)
