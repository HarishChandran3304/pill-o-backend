import streamlit as st
import requests

def send_post_request(data):
    url = 'https://positive-clearly-tiger.ngrok-free.app/doctors'
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            st.success("Post request sent successfully!")
        else:
            st.error(f"Failed to send post request. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def main():
    st.title("Doctor Signup")

    with st.form("my_form", clear_on_submit=True):
        docID = st.text_input("Doctor ID")
        name = st.text_input("Doctor Name")
        age = st.text_input("Age")
        speciality = st.text_input("Speciality")
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        if docID and name and age and speciality:
            send_post_request({"docID": docID, "name": name, "age": age, "speciality": speciality})
        else:
            st.warning("Please enter data before submitting")

if __name__ == "__main__":
    main()
