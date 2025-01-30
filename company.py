import streamlit as st
import pandas as pd

st.title("HackTrack👾💻")
st.write("---")



st.subheader("Add New Activity for the Company")

company_name = st.text_input("Enter the company name: ")
camp_name = st.text_input("Enter the camp name: ")
goals = st.text_area("What are the goals of this camp: ")
description = st.text_area("What are the description for this camp:")
requirements = st.text_area("What are the requirements for this camp:")
duration = st.text_input("What is the duration of the camp: ")
age = st.number_input("What is the minimum age requirement?", min_value=0, max_value=100)
link=st.text_area("enter the link of the activity: ")


if st.button("Submit"):
    if company_name and camp_name and description and duration and age > 0:

        with open("your_file.csv", "a", newline="", encoding="utf-8") as file:
            file.write(f"{company_name},{camp_name},{description},{duration},{age},{requirements},{goals},{link}\n")
        
        st.write("Company Name:", company_name)
        st.write("Camp Name:", camp_name)
        st.write("Goals:", goals)
        st.write("Requirements:", requirements)
        st.write("Duration:", duration)
        st.write("Link: ",link)
        st.success("The camp has been successfully added!")

    else:
        st.error("Please fill in all fields before submitting.")


if st.button("Back"):
    st.switch_page("main.py")
