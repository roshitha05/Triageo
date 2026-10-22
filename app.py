import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from prompts  import PROMPT_V1

# load environment
load_dotenv()
# connect to tokenreoky
client = OpenAI(
    api_key=os.getenv("TOKENREPLY_API_KEY"),
    base_url="https://api.tokenreply.com/v1"
)

def analyse_ticket(ticket):
    prompt = PROMPT_V1.format(ticket=ticket)
    response = client.chat.completions.create(
        model="grok-4.20-fast",
        messages=[
            {"role": "user", "content": "prompt"}
        ]
    )
    return response.choice[0].message.content

st.title("Triageo")
st.write("Turn support request into actionable insights")

ticket = st.text_area(
    "Support Ticket",
    placeholder="Unable to access account as it keeps getting locked after the password has been changed."
)

if st.button("Analyse Ticket"):
    if ticket.strip():
        with st.spinner("Analysing ticket..."):
            result = analyse_ticket(ticket)

        st.subheader("Analysis")
        st.write(result)
    else:
        st.warning("Please enter a support ticket.")