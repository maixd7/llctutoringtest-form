import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
st.cache_data.clear()
conn = st.connection("gsheets", type=GSheetsConnection)
existing_data = conn.read(worksheet="Lesson", usecols=list(range(6)))
student_data = conn.read(worksheet="Client", usecols=list(range(7)))
package_data = conn.read(worksheet="Lesson Package", usecols=list(range(4)))
existing_data = existing_data.dropna(how="all")
max_id = existing_data['ID'].max()


with st.form(key="llctutoring_form"):
    studentName = st.text_input(label="Student Name*", )
    tutorName = st.text_input(label="Tutor Name*")
    subject = st.text_input(label="Subject*")
    lessonDate = st.date_input(label="Lesson Date*")
    notes = st.text_input(label="Notes:*")

    submit_button = st.form_submit_button(label="Submit")
    st.markdown("**required*")

    if submit_button:
        if not studentName or tutorName or subject or lessonDate or notes:
            st.warning("Ensure all mandatory fields are filled.")
            st.stop()
        else:
            st.write("You have submitted")
            form_data = pd.DataFrame(
                [
                    {
                        "ID": max_id+1,
                        "Student Name": studentName,
                        "Tutor Name": tutorName,
                        "Subject": subject,
                        "Lesson Date": lessonDate,
                        "Notes": notes,
                    }
                ]
            )
            update_df = pd.concat([existing_data, form_data])
            conn.update(worksheet = "Lesson", data=update_df)
            st.cache_data.clear()
            
        
        
