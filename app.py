import streamlit as st
from google import genai
import tempfile
import time

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

        if 'sample_file' not in st.session_state:
            with st.spinner("جاري رفع الملف ومعالجته بواسطة الذكاء الاصطناعي..."):
                file_ref = client.files.upload(file=tmp_path)
                # الانتظار حتى تنتهي معالجة الملف تماماً على السيرفر
                while file_ref.state.name == "PROCESSING":
                    time.sleep(2)
                    file_ref = client.files.get(name=file_ref.name)
                st.session_state.sample_file = file_ref
            st.success("تم رفع الملف ومعالجته بنجاح!")

        if st.button("توليد الشرح وأسئلة الامتحانات (MCQ)"):
            with st.spinner("جاري تحليل المحاضرة وكتابة الشرح والأسئلة..."):
                prompt = (
                    "قم بتحليل ملف المحاضرة المرفق الخاص بمادة التمريض، واكتب لي بشكل منظم وواضح:"
                    "1. شرح مبسط لأهم النقاط والمفاهيم الواردة."
                    "2. أسئلة اختيار من متعدد (MCQ) مع تحديد الإجابة الصحيحة لكل سؤال."
                )
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=[st.session_state.sample_file, prompt]
                )
                st.markdown("### ملخص المحاضرة وأسئلة المراجعة:")
                st.markdown(response.text)


