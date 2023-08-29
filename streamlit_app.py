import openai
import streamlit as st

# Set page configuration
st.set_page_config(page_title="OpenAI Translator")

# Initialize target_language if not present in session_state
if "target_language" not in st.session_state:
    st.session_state.target_language = "French"

with st.sidebar:
    st.title('🤖💬 OpenAI Translator..')
    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        openai.api_key = st.secrets['OPENAI_API_KEY']
    else:
        openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
        if not (openai.api_key.startswith('sk-') and len(openai.api_key)==51):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('API key set successfully!', icon='👍')

# Language translation function using OpenAI
def translate_text(text, target_language):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Translate the following English text to {target_language}:\n{text}\nTranslation:",
        temperature=0,
        max_tokens=500
    )
    translation = response.choices[0].text.strip()
    return translation

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter text to translate:"):
    translation = translate_text(prompt, st.session_state.target_language)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": translation})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        st.markdown(translation)

# Convert target_language to its corresponding index
target_language_options = ['French', 'Spanish', 'German', 'Italian','Telugu','Hindi']
target_language_index = target_language_options.index(st.session_state.target_language)

# Use the correct index for selectbox
target_language = st.selectbox('Select Target Language', target_language_options, index=target_language_index)

st.session_state.target_language = target_language



