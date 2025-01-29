import streamlit as st 

st.navigation(
    [
        st.Page("main.py", title="m", default=True),
        st.Page("company.py", title="c"),
        st.Page("student.py", title="s"),
    ], 
    position= "hidden",
).run()