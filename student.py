import streamlit as st
import pandas as pd
import google.generativeai as genai

st.title("HackTrack👾💻")
st.write("---")
option = st.selectbox("Choose a service?", ("View All Available Activities", "Discover Events Based on My Skills and Interests"))

if option == "View All Available Activities":
    st.write("Here you can explore all the available activities and events.")
    

    file_path = "data.csv" 
    
    try:
        df = pd.read_csv(file_path)
        st.dataframe(df)
    except Exception as e:
        st.write(f"Error reading the file: {e}")
        

elif option == "Discover Events Based on My Skills and Interests":
    provider="together"
    API_KEY = "AIzaSyDw_VJYuaeeJbzXuih3Dosz2M1JpuCIFXg" 
    genai.configure(api_key=API_KEY)

    st.title("🤖 HackTrack - Your AI Assistant")
    st.caption("🚀 Discover relevant training programs based on your interests")

    if "conversation_history" not in st.session_state:
        st.session_state["conversation_history"] = ""

    def get_gemini_response(conversation_history):
        prompt = (
            "You are HackTrack, an AI assistant that helps users discover relevant training programs. "
            "You ask questions to understand the user's interests and suggest training programs based on their responses.\n"
            "You will be conducting a conversation and dynamically asking questions based on the user's responses.\n"
            "Here is the conversation history:\n"
            f"{conversation_history}\n"
            "Your response should be a question to continue the conversation.\n"
            "HackTrack: "
        )

        try:
            response = genai.Chat(messages=[{"role": "system", "content": prompt}]).send()
            
            return response['messages'][0]['content']
        
        except Exception as e:
            return f"Sorry, I encountered an issue connecting to Gemini API. Error: {str(e)}"

    if "has_entered_name_age" not in st.session_state:
        user_name = st.text_input("Enter your name:")
        user_age = st.number_input("Enter your age:", min_value=18, max_value=100, step=1)
        
        if user_name and user_age:
            st.session_state["has_entered_name_age"] = True
            st.session_state["user_name"] = user_name
            st.session_state["user_age"] = user_age

            st.session_state["conversation_history"] += f"\nUser: Name: {user_name}, Age: {user_age}"

            st.success(f"Thank you for providing your name and age, {user_name}! Let's continue...")

            st.stop()

    if "has_entered_name_age" in st.session_state:
        st.markdown(f"### Hello {st.session_state['user_name']}! Let's start with something simple.")

        with st.container():
            user_interest = st.text_input("What field are you interested in? (e.g., programming, design, management)")

            if user_interest:
                st.session_state["conversation_history"] += f"\nUser: {user_interest}"

                hacktrack_response = get_gemini_response(st.session_state["conversation_history"])
                st.session_state["conversation_history"] += f"\nHackTrack: {hacktrack_response}"

                st.markdown(f"**HackTrack:** {hacktrack_response}")


















if st.button("back"):
    st.switch_page("main.py")
