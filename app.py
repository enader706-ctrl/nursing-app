import streamlit as st
from google import genai

st.set_page_config(page_title="منصة تمريض كفر الشيخ الذكية", page_icon="🩺", layout="centered")

st.title("🩺 منصة المراجعة الذكية - تمريض كفر الشيخ")
st.write("ارفع ملف المحاضرة أو كتاب المنهج (PDF)، واحصل على شرح مبسط وأهم أسئلة الامتحانات (MCQ).")

# إدخال مفتاح الـ API
api_key = st.text_input("أدخل مفتاح Google Gemini API الخاص بك:", type="password")

if api_key:
    client = genai.Client(api_key=api_key)
    
    uploaded_file = st.file_uploader("اختر ملف المحاضرة (PDF)", type=["pdf"])
    
    if uploaded_file is not None:
        with st.spinner("جاري قراءة الملف وتحليل محتواه الطبي... ⏳"):
            # رفع الملف لمعالجة الذكاء الاصطناعي
            sample_file = client.files.upload(file=uploaded_file)
            
            if st.button("🚀 توليد الشرح وأسئلة الامتحان"):
                prompt = """
                أنت أستاذ تمريض خبير. بناءً على محتوى هذا الملف:
                1. قدم ملخصاً شاملاً ومبسطاً لأهم النقاط الإكلينيكية والعلمية.
                2. استخرج أهم 10 أسئلة امتحانات (MCQ) متوقعة مع الخيارات (أ، ب، ج، د).
                3. اذكر الإجابة الصحيحة لكل سؤال مع تفسير قصير لسبب صحتها.
                رتب الإجابة بتنسيق منظم وواضح جداً للطلاب.
                """
                
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[sample_file, prompt]
                )
                
                st.success("تم التوليد بنجاح! 🎉")
                st.markdown(response.text)
import tempfile

uploaded_file = st.file_uploader("اختر ملف المحاضرة (PDF)", type="pdf")

if uploaded_file is not None:
    # حفظ الملف المرفوع مؤقتاً على النظام
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    # رفع الملف للذكاء الاصطناعي باستخدام المسار المؤقت
    sample_file = client.files.upload(file=tmp_path)
