## Molten_Core_HacktheLoop

- Our main app is _**run_app.py**_

- [Our app url hosted on Streamlit](https://moltencorehacktheloop-gzxkgpjrg7f7ibphws9pmx.streamlit.app/)

# Remember to add the following dependencies to properly run our app:
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

 
