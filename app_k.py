import streamlit as st
from langchain_community.llms import Ollama
import pandas as pd
from app_helper import *
from email_tester_testing import *

# Custom CSS for styling including gradient background
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700&display=swap');
    body {
        font-family: 'Poppins', sans-serif;
    }
    .main {
        background-color: transparent;
    }
    .title1 {
        font-family: 'Poppins', sans-serif;
        font-size: 3.5em;
        color: #ffffff;
        text-align: center;
        margin-top: 20px;
        layout="wide";
    }
    .title2 {
        font-family: 'Poppins', sans-serif;
        font-size: 6em;
        text-align: center;
        margin-top: 10px;
        layout="wide";
        background: linear-gradient(90deg, #9a2e6a, #ec4a59);
        -webkit-background-clip: text;
        color: transparent;
    }
    .subtitle {
        font-size: 1.5em;
        color: #ec8740;
        text-align: center;
        margin-bottom: 40px
        layout="wide";
    }
    .intro-text {
        font-size: 2em;
        color: #ffffff;
        text-align: center;
        width: 100%;
        margin: 20px auto;
    }
    .get-started {
        display: flex;
        justify-content: center;
        margin-top: 30px;
    }
    .header {
        text-align: center;
        color: #61dafb;
    }
    .button {
        background-color: #61dafb;
        color: #282c34;
        border: none;
        padding: 10px 20px;
        font-size: 2em;
        cursor: pointer;
        border-radius: 5px;
        text-align: center;
        display: inline-block;
        margin: 20px 10px;
        text-decoration: none;
    }
    .button:hover {
        background-color: #21a1f1;
    }
    .centered-button {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 30px;
    }
    .file-upload {
        color: #ffffff;
    }
    .stApp {
        background-color: transparent;
    }
    </style>
""", unsafe_allow_html=True)

# Setting the background image
page_bg_img = '''
<style>
.stApp {
 background: linear-gradient(to right, #061a23, #061a23);
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

# Ensure 'page' in st.session_state is set
if 'page' not in st.session_state:
    st.session_state['page'] = 'Home'

# Check the current page
page = st.session_state['page']

# Title of the app
st.markdown('<div class="title1">Welcome to our app </div>', unsafe_allow_html=True)
st.markdown('<div class="title2">EventifAI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">YOUR EVENTFUL FUTURE MADE EASY</div>', unsafe_allow_html=True)

if page == "Home":
    # Home page content
    st.markdown('<div class="intro-text">One-stop app for scheduling Google Calendar events, adding participants, and sending personalized emails with AI-chosen templates for any event.</div>', unsafe_allow_html=True)
    st.image('logo.png', use_column_width=True)
    if st.button("Get Started!"):
        st.session_state.page = "Event Planner"
        st.experimental_rerun()

if page == "Event Planner":
    # Ensure session_state for event_type
    if 'event_type' not in st.session_state:
        st.session_state['event_type'] = None

    # Event type selection page
    if st.session_state['event_type'] is None:
        st.header("Select Event Type")
        event_type = st.radio("Is the event onsite or online?", ("Onsite Event", "Online Event"), key="event_type_radio")

        if st.button("Next"):
            st.session_state['event_type'] = event_type
            st.experimental_rerun()

    # Details page for onsite events
    if st.session_state['event_type'] is not None:
        if st.session_state.get('event_type') == "Onsite Event":
            st.header("Onsite Event Details")
            st.title("Email Template Generator")

            if "email_template" not in st.session_state:
                st.session_state.email_template = ""
            if "attachment" not in st.session_state:
                st.session_state.attachment = None
            if "attachment_name" not in st.session_state:
                st.session_state.attachment_name = None

            event_type = st.text_input("Enter the type of event:")

            tone = st.radio("Choose the tone of the email:", ("formal", "informal"))
            name = st.text_input("Enter your name:")
            prompt = st.text_input("Type your prompt here (don't forget to mention the date and time!): ")

            st.header("Upload Guest/Participant list")
            uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx", key="file_uploader")

            if uploaded_file is not None:
                st.session_state['file_uploaded'] = True
                st.session_state['uploaded_data'] = pd.read_excel(uploaded_file)
                st.success("Excel file uploaded successfully!")
                emails = extract_emails(st.session_state['uploaded_data'], 'user_email')
                if emails:
                    st.session_state['emails'] = emails  # Store emails in session state
                    st.write("Extracted Emails:")
                    st.write(emails)
                else:
                    st.error("No emails found in the 'user_email' column.")
                st.dataframe(st.session_state['uploaded_data'])

            if st.button("Generate Email Template"):
                st.session_state.email_template = email_generator(prompt, name, event_type, tone)
                st.text_area("Generated Email Template:", value=st.session_state.email_template, height=200)
            else:
                st.text_area("Generated Email Template:", value=st.session_state.email_template, height=200)

            uploaded_file = st.file_uploader("Choose a file to attach")

            if uploaded_file is not None:
                st.session_state.attachment = uploaded_file
                st.session_state.attachment_name = uploaded_file.name

            if st.session_state.attachment:
                st.write(f"Attached file: {st.session_state.attachment_name}")

            if st.button("Confirm and Send Emails"):
                st.write("Sending emails...")

                try:
                    send_emails(emails, st.session_state.email_template, st.session_state.attachment, st.session_state.attachment_name)
                except Exception as e:
                    st.error(f"An error occurred: {e}")

            if st.button("Next"):
                if st.session_state['file_uploaded']:
                    st.session_state['page'] = 'chatbot'
                    st.experimental_rerun()
            st.markdown('<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3153.835434510016!2d144.96305781514882!3d-37.814107979751994!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x6ad642af0f11fd81%3A0xf57767ec3f59ffef!2sFederation%20Square!5e0!3m2!1sen!2sau!4v1627557207297!5m2!1sen!2sau" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>', unsafe_allow_html=True)

        elif st.session_state.get('event_type') == "Online Event":
            st.header("Online Event Details")
            st.header("Upload Guest/Participant list")
            uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx", key="file_uploader")

            if uploaded_file is not None:
                st.session_state['file_uploaded'] = True
                st.session_state['uploaded_data'] = pd.read_excel(uploaded_file)
                st.write("Excel file uploaded successfully!")
                emails = extract_emails(st.session_state['uploaded_data'], 'user_email')
                if emails:
                    st.session_state['emails'] = emails  # Store emails in session state
                    st.write("Extracted Emails:")
                    st.write(emails)
                else:
                    st.write("No emails found in the 'user_email' column.")
                st.dataframe(st.session_state['uploaded_data'])

            if st.button("Next"):
                if st.session_state['file_uploaded']:
                    st.session_state['page'] = 'chatbot'
                    st.experimental_rerun()

    # Chatbot page
if st.session_state['page'] == 'chatbot':
    st.header("Chatbot")
    message_container = st.container()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        avatar = "🤖" if message["role"] == "assistant" else "😎"
        with message_container.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if prompt := st.chat_input("Enter a prompt here..."):
        try:
            st.session_state.messages.append(
                {"role": "user", "content": prompt})

            message_container.chat_message("user", avatar="😎").markdown(prompt)

            with message_container.chat_message("assistant", avatar="🤖"):
                with st.spinner("Model working..."):
                    # Dummy response simulation
                    response = event_chatbot(st.session_state.get('emails', []), prompt)
                st.write(response)
        except Exception as e:
            st.error(e, icon="⛔️")

if page == "Email Generator":
    st.title("Email Template Generator")

    if "email_template" not in st.session_state:
        st.session_state.email_template = ""
    if "attachment" not in st.session_state:
        st.session_state.attachment = None
    if "attachment_name" not in st.session_state:
        st.session_state.attachment_name = None

    event_type = st.text_input("Enter the type of event:")

    tone = st.radio("Choose the tone of the email:", ("formal", "informal"))
    name = st.text_input("Enter your name:")
    prompt = st.text_input("Type your prompt here (don't forget to mention the date and time!): ")

    st.header("Upload Guest/Participant list")
    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx", key="file_uploader")

    if uploaded_file is not None:
        st.session_state['file_uploaded'] = True
        st.session_state['uploaded_data'] = pd.read_excel(uploaded_file)
        st.success("Excel file uploaded successfully!")
        emails = extract_emails(st.session_state['uploaded_data'], 'user_email')
        if emails:
            st.session_state['emails'] = emails  # Store emails in session state
            st.write("Extracted Emails:")
            st.write(emails)
        else:
            st.error("No emails found in the 'user_email' column.")
        st.dataframe(st.session_state['uploaded_data'])

    if st.button("Generate Email Template"):
        st.session_state.email_template = email_generator(prompt, name, event_type, tone)
        st.text_area("Generated Email Template:", value=st.session_state.email_template, height=200)
    else:
        st.text_area("Generated Email Template:", value=st.session_state.email_template, height=200)

    uploaded_file = st.file_uploader("Choose a file to attach")

    if uploaded_file is not None:
        st.session_state.attachment = uploaded_file
        st.session_state.attachment_name = uploaded_file.name

    if st.session_state.attachment:
        st.write(f"Attached file: {st.session_state.attachment_name}")

    if st.button("Confirm and Send Emails"):
        st.write("Sending emails...")

        try:
            send_emails(emails, st.session_state.email_template, st.session_state.attachment, st.session_state.attachment_name)
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Button to reset the session state and go back to the home page
if page != "Home":
    if st.button("Go Back"):
        st.session_state['page'] = 'Home'
        st.session_state['event_type'] = None
        st.session_state['file_uploaded'] = False
        st.experimental_rerun()
