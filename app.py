
import streamlit as st
from google import genai
import tempfile

st.title("منصة المراجعة الذكية - تمريض كفر الشيخ")
st.write("ارفع ملف المحاضرة أو كتاب المنهج (PDF) واحصل على شرح مبسط وأهم أسئلة الامتحانات (MCQ).")

api_key = st.text_input("أدخل مفتاح Google Gemini API الخاص بك:", type="password")

if api_key:
    client = genai.Client(api_key=api_key)
    uploaded_file = st.file_uploader("اختر ملف المحاضرة (PDF)", type="pdf")

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        sample_file = client.files.upload(file=tmp_path)
        st.success("تم رفع الملف بنجاح وربطه بالذكاء الاصطناعي!")
