import streamlit as st
import os
from dotenv import load_dotenv
from run_wk3_l4_vector_db_rag import respond_to_query, load_yaml_config
from paths import APP_CONFIG_FPATH, PROMPT_CONFIG_FPATH

load_dotenv()

# Load configs
app_config = load_yaml_config(APP_CONFIG_FPATH)
prompt_config = load_yaml_config(PROMPT_CONFIG_FPATH)
rag_assistant_prompt = prompt_config["rag_assistant_prompt"]
vectordb_params = app_config["vectordb"]
llm = app_config["llm"]

# Custom page config
st.set_page_config(
    page_title="ARK Chat Assistant",
    page_icon="OTHER/Ark_logo.jpg",  # Use your logo file here
    layout="centered",
)

# Add logo and title
logo_path = os.path.join("OTHER", "Ark_logo.jpg")
st.image(logo_path, width=120)
st.markdown(
    "<h1 style='text-align: center; color: #0A4D68;'>ARK Chat Assistant</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #4F8A8B;'>Ask anything about your documents and get instant answers!</p>",
    unsafe_allow_html=True,
)

# At the top of your script
if "input_key" not in st.session_state:
    st.session_state.input_key = 0

# Chat input area
st.markdown("---")
st.markdown(
    "<h4 style='color: #0A4D68;'>Type your message below:</h4>", unsafe_allow_html=True
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input(
        "",
        key=f"user_input_{st.session_state.input_key}",
        placeholder="Type your question here...",
    )

with col2:
    send_clicked = st.button("Send")

if send_clicked and user_input:
    response = respond_to_query(
        prompt_config=rag_assistant_prompt,
        query=user_input,
        llm=llm,
        chat_history=st.session_state.chat_history,
        **vectordb_params,
    )
    st.session_state.chat_history.append({"role": "user", "text": user_input})
    st.session_state.chat_history.append({"role": "assistant", "text": response})
    st.session_state.input_key += 1  # Increment key to reset input field

# Chat history display
st.markdown("---")
st.markdown("<h4 style='color: #0A4D68;'>Chat History</h4>", unsafe_allow_html=True)
for turn in reversed(st.session_state.chat_history[-5:]):  # Show most recent first
    if turn["role"] == "user":
        st.markdown(
            f"<div style='background-color:#E7F6F2; border-radius:10px; padding:10px; margin-bottom:5px;'><b>You:</b> {turn['text']}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div style='background-color:#F9F7F7; border-radius:10px; padding:10px; margin-bottom:5px;'><b>Assistant:</b> {turn['text']}</div>",
            unsafe_allow_html=True,
        )

st.markdown(
    "<footer style='text-align: center; color: #888; margin-top: 30px;'>Powered by ARK & LangChain</footer>",
    unsafe_allow_html=True,
)
