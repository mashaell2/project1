import streamlit as st
import pandas as pd
import google.generativeai as genai
from huggingface_hub import InferenceClient
from fuzzywuzzy import process
import requests

st.title("HackTrack👾💻")
st.write("Student Page")
st.write("---")

option = st.selectbox("Choose a service?", ("View All Available Activities", "Discover Events Based on My Skills and Interests"))

# View Available Activities
if option == "View All Available Activities":
    st.write("Here you can explore all the available activities and events.")
    file_path = "data1.csv"  # Update the path to your CSV file
    try:
        df = pd.read_csv(file_path)
        st.dataframe(df)  # Display the activities table
    except Exception as e:
        st.write(f"Error reading the file: {e}")

elif option == "Discover Events Based on My Skills and Interests": 
    

    # إعدادات الـ API
    API_KEY = "AIzaSyDgKh9QFCc9O7vkfAxYyJOtG4z1v4m_wWI"  # ضع هنا مفتاح الـ API الخاص بك
    genai.configure(api_key=API_KEY)

    # ملف إكسل يحتوي على بيانات البرامج التدريبية
    prog_file = r"C:\Users\shoog\OneDrive\المستندات\data11.xlsx"  # تأكد من مسار الملف

    # تحميل البيانات من ملف Excel
    df = pd.read_excel(prog_file)

    # دالة لتوليد ردود باستخدام DeepSeek أو Google Gemini
    def get_deepseek_response(prompt):
        model = genai.GenerativeModel("gemini-1.5-flash-8b")
        return model.generate_content(prompt).text

    # دالة لتقديم البرنامج التدريبي المناسب بناءً على المدخلات
    def recommend_training(user_data):
        # استخدام fuzzywuzzy للبحث عن البرنامج الأقرب بناءً على العمود "Name"
        best_match = process.extractOne(user_data['interest'], df['Name'])  # هنا تم تعديل الاسم إلى 'Name'
        recommended_program_name = best_match[0]  # اسم البرنامج الموصى به
        recommended_program_info = df.loc[df['Name'] == recommended_program_name, 'Info'].values[0]  # الوصف
        recommended_program_link = df.loc[df['Name'] == recommended_program_name, 'Link'].values[0]  # رابط التسجيل (إذا كان موجودًا)
        return recommended_program_name, recommended_program_info, recommended_program_link

    # واجهة المستخدم باستخدام Streamlit
    st.title("🤖 HackTrack - Your AI Assistant")
    st.caption("🚀 Let's find the best training program for you!")

    # التحقق من وجود conversation_history في الجلسة وإذا لم يكن موجودًا نقوم بتهيئته
    if "conversation_history" not in st.session_state:
        st.session_state["conversation_history"] = ""

    if "has_entered_name_age" not in st.session_state:
        st.session_state["has_entered_name_age"] = False

    if not st.session_state["has_entered_name_age"]:
        # جمع اسم المستخدم والعمر أولاً
        user_name = st.text_input("Enter your name: / أدخل اسمك:")
        user_age = st.number_input("Enter your age: / أدخل عمرك:", min_value=18, max_value=100, step=1)
        
        if user_name and user_age:
            # زر "Let's Start!"
            start_button = st.button("Let's Start! / ابدأ الآن!")
            
            if start_button:
                st.session_state["has_entered_name_age"] = True
                st.session_state["user_name"] = user_name
                st.session_state["user_age"] = user_age
                st.success(f"Thank you for providing your name and age, {user_name}! Let's continue... / شكراً لإدخال اسمك وعُمرك، {user_name}! دعنا نكمل...")
                
                # إرسال رسالة النظام في بداية المحادثة فقط، لا تعرض للمستخدم
                system_message = """
                You are an AI assistant conducting a text interview with the user. 
                Your goal is to understand their interests in order to suggest relevant training programs.
                Start by asking questions to learn more about their interests, background, and goals.
                Ask the user for their field of interest and follow-up questions based on their responses.
                Finally, recommend a relevant training program based on the information you have gathered.
                """
                # نرسل رسالة النظام لتوجيه الـ AI لكن لا نعرضها للمستخدم
                _ = get_deepseek_response(system_message)

    else:
        # بعد الضغط على زر "Let's Start!"، نعرض الأسئلة الأخرى
        user_interest = st.text_input("What field are you interested in? (e.g., programming, design, management) / ما هو المجال الذي تهتم به؟ (مثل البرمجة، التصميم، الإدارة)")

        if user_interest:
            st.session_state["conversation_history"] += f"\nUser: {user_interest}"
            # استخدم DeepSeek لتوليد ردود ذكية
            bot_response = get_deepseek_response(st.session_state["conversation_history"])
            st.session_state["conversation_history"] += f"\nBot: {bot_response}"
            st.markdown(f"Bot: {bot_response}")
            
            # سؤال آخر حول المستوى الدراسي أو الخبرات الأخرى
            user_education = st.text_input("What is your education level? (e.g., High School, Bachelor's, Master's) / ما هو مستوى تعليمك؟ (مثل الثانوية، بكاليروس، ماجستير)")

            if user_education:
                st.session_state["conversation_history"] += f"\nUser: {user_education}"
                # يمكن إضافة ردود ذكية أخرى هنا
                bot_response = get_deepseek_response(st.session_state["conversation_history"])
                st.session_state["conversation_history"] += f"\nBot: {bot_response}"
                st.markdown(f"Bot: {bot_response}")

                # جمع المزيد من البيانات إذا لزم الأمر
                user_goals = st.text_input("What are your goals or what are you hoping to learn? / ما هي أهدافك أو ما الذي تأمل في تعلمه؟")

                if user_goals:
                    st.session_state["conversation_history"] += f"\nUser: {user_goals}"
                    # التفاعل مع DeepSeek للحصول على ردود أكثر ذكاءً
                    bot_response = get_deepseek_response(st.session_state["conversation_history"])
                    st.session_state["conversation_history"] += f"\nBot: {bot_response}"
                    st.markdown(f"Bot: {bot_response}")
                    
                    # بعد جمع جميع المعلومات المطلوبة، ابحث في الـ Excel sheet
                    user_data = {
                        'name': st.session_state['user_name'],
                        'age': st.session_state['user_age'],
                        'interest': user_interest,
                        'education': user_education,
                        'goals': user_goals
                    }
                    
                    # التوصية بالبرنامج التدريبي المناسب
                    recommended_program_name, recommended_program_info, recommended_program_link = recommend_training(user_data)
                    
                    # عرض اسم البرنامج، الوصف، ورابط التسجيل
                    st.markdown(f"### {recommended_program_name}")  # اسم البرنامج
                    st.markdown(f"Description: / الوصف: {recommended_program_info}")  # الوصف
                    if recommended_program_link:
                        st.markdown(f"[سارع بالتسجيل الآن!]( {recommended_program_link} )")  # رابط التسجيل
                    else:
                        st.markdown("لا يوجد رابط تسجيل متاح حالياً.")  # إذا لم يوجد رابط

if st.button("back"):
    st.switch_page("main.py")
