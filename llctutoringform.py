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
existing_data = conn.read(worksheet="Lesson", usecols=list(range(7)))
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
        if not (studentName or tutorName or subject or lessonDate or notes):
            st.warning("Ensure all mandatory fields are filled.")
            st.stop()
        else:
            st.write("You have submitted")
            # Identifying lesson package id
            student_row = student_data[student_data["Student Name"] == studentName.title().strip()]
            lesson_package_id = student_row.iloc[0]['Lesson Package id']
            # Updating lesson package
            package_row = package_data[package_data["id"] == lesson_package_id]
            current_count = package_row.iloc[0]['Current Lesson Count']
            new_count = current_count+1
            package_data.loc[package_data["id"] == lesson_package_id, "Current Lesson Count"] = new_count
            form_data = pd.DataFrame(
                [
                    {
                        "ID": max_id+1,
                        "Student Name": studentName.title().strip(),
                        "Tutor Name": tutorName.title().strip(),
                        "Subject": subject,
                        "Lesson Date": lessonDate,
                        "Notes": notes,
                        "Lesson Number": current_count
                    }
                ]
            )
            #Update spreadsheet
            update_df = pd.concat([existing_data, form_data])
            conn.update(worksheet = "Lesson", data=update_df)
            conn.update(worksheet="Lesson Package", data=package_data)
            conn.update(worksheet = "Lesson", data=update_df)
            st.cache_data.clear()
            
        
        
