import streamlit as st



st.title("HackTrack👾💻")
st.write("---")

file_path = "data1.csv"

company_name = st.text_input("Enter the company name: ")

camp_name = st.text_input("Enter the camp name: ")

goals = st.text_area("What are the goals of this camp: ")

description = st.text_area("What are the description for this camp:")

requirements = st.text_area("What are the requirements for this camp:")

duration = st.text_input("What is the duration of the camp: ")

age = st.number_input("What is the minimum age requirement?", min_value=0, max_value=100)


new_data = "\n" + str(camp_name) + "," + str(description) + "," + str(duration) + "," + str(age) + "," + str(requirements) + "," + str(goals)
with open("your_file.csv", "w", encoding="utf-8") as file:
    file.write(new_data)


if st.button("Submit"):

    st.write("Company Name:", company_name)
    st.write("Camp Name:", camp_name)
    st.write("Goals:", goals)
    st.write("Requirements:", requirements)
    st.write("Duration:", duration)
    st.success("The camp has been successfully added!")



if st.button("back"):
    st.switch_page("main.py")