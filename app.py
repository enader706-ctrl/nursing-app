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

        if 'sample_file' not in st.session_state:
            with st.spinner("جاري رفع الملف إلى الذكاء الاصطناعي..."):
                st.session_state.sample_file = client.files.upload(file=tmp_path)
            st.success("تم رفع الملف بنجاح وربطه بالذكاء الاصطناعي!")

        if st.button("توليد الشرح وأسئلة الامتحانات (MCQ)"):
            with st.spinner("جاري تحليل المحاضرة وكتابة المراجعة والأسئلة..."):
                prompt = (
                    "قم بتحليل ملف المحاضرة المرفق الخاص بمادة التمريض، واكتب لي:"
                    "1. شرح مبسط وواضح لأهم النقاط والمفاهيم الواردة فيه."
                    "2. مجموعة من أسئلة الاختيار من متعدد (MCQ) مع ذكر الإجابة الصحيحة لكل سؤال لتغطية الامتحانات."
                )
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[st.session_state.sample_file, prompt]
                )
                st.markdown("### ملخص المحاضرة وأسئلة المراجعة:")
                st.markdown(response.text)

