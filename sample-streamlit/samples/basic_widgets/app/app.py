from datetime import date

import streamlit as st

st.set_page_config(page_title="Basic Widgets Sample", page_icon="🧩")
st.title("Basic Widgets Sample")
st.write("Streamlit の主要ウィジェットを一覧で確認できるサンプルです。")

st.header("Text input")
name = st.text_input("Your name", "World")
st.write(f"Hello, {name}!")

st.header("Slider")
value = st.slider("Pick a number", 0, 100, 50)
st.write(f"Selected value: {value}")

st.header("Checkbox")
agree = st.checkbox("I agree")
st.write("Checked" if agree else "Unchecked")

st.header("Selectbox")
option = st.selectbox("Choose an option", ["Option A", "Option B", "Option C"])
st.write(f"You chose: {option}")

st.header("Radio")
choice = st.radio("Pick one", ["Cat", "Dog", "Bird"])
st.write(f"You picked: {choice}")

st.header("Date input")
selected_date = st.date_input("Pick a date", date.today())
st.write(f"Selected date: {selected_date}")

st.header("Color picker")
color = st.color_picker("Pick a color", "#00A0FF")
st.write(f"Selected color: {color}")

st.header("File uploader")
uploaded = st.file_uploader("Upload a text file", type=["txt", "csv"])
if uploaded is not None:
    st.write(f"Uploaded file: {uploaded.name} ({uploaded.size} bytes)")

st.header("Button")
if st.button("Click me"):
    st.success("Button clicked!")
