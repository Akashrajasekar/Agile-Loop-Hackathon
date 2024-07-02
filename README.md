# 📆 Welcome to our app _EventifAI_ 📆
by team Molten_Core 🌋

_**Your Eventful future made easy**_
---

# About our app:

This is your one-stop app for seamlessly planning out all your events. 
Schedule 🌍 on-site and 💻 online events on 📆 Google Calendar, and send out personalized Invite 📧 Emails to your invitees, all with a simple prompt to our AI 🦙

---

- Our main app is _**run_app.py**_

- [Check out our app hosted on 👑Streamlit](https://moltencorehacktheloop-gzxkgpjrg7f7ibphws9pmx.streamlit.app/)

---

# 
- A google cloud console project with valid API's and OAuth ClientID's which gives you a valid credentials (configs.json as referenced in our program)
- Add configs.json to the same directory => then run autherizor_for_tokens.py to generate a token.py file
- The Gmail and Google Calendar API enabled with scopes set to the following: https://www.googleapis.com/auth/calendar and https://www.googleapis.com/auth/gmail.send

# We leverage Llama 3 8B as our llm. Using Ollama:
- Run Command Prompt as Administrator

- Update pip and reinstall dependencies:
```
pip install --upgrade pip
pip uninstall ollama
pip install ollama
```
- Reinstall PyTorch (example, make sure to install the correct version for your needs)
```
pip install torch torchvision torchaudio
```

 
