import streamlit as st
from huggingface_hub import InferenceClient






#st.title("HackTrack👾💻")
st.write("---")
st.sidebar.title("Sidebar Menu")
page = st.sidebar.radio("Select Page:", ["Home", "About the App", "Feedback & Evaluation"])

if page == "Home": 
    st.title("Welcome to HackTrack")
    st.markdown("<h1 style='font-size: 30px;'>Login as</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
 


    with col1: 
        if st.button("Student"):
            st.switch_page("student.py")
            





    with col2:
        if st.button("Company"):
         st.switch_page("company.py")




         
elif page == "About the App":
    st.title("About the app")
    about_us = """
About HackTrack⚡: \n
Many students face difficulties in finding hackathons and training programs that align with their skills and aspirations. HackTrack offers an 
innovative solution to this problem by acting as a comprehensive platform that brings together all the events in one place. \n
The app relies on analyzing students' resumes or conducting personal interviews using artificial intelligence to provide recommendations 
that match their abilities and interests, helping them save time and effort. Additionally, HackTrack simplifies the process of sorting and 
accepting registrants for companies, making the process more organized and precise. \n
HackTrack is not just a tool for finding events; it is a complete solution that connects students with companies and 
enhances success opportunities for both sides.
    """
    st.write(about_us)


elif page =="Feedback & Evaluation":
    st.write("Rate my Website")
    sentiment_mapping = ["one", "two", "three", "four", "five"]
    selected = st.feedback("stars")
    if selected is not None:
        st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")
