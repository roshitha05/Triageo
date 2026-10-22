import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from prompts  import PROMPT_V1, PROMPT_V2, PROMPT_V3

# load environment
load_dotenv()
# connect to tokenreoky
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def analyse_ticket(ticket):
    prompt = PROMPT_V3.format(ticket=ticket)
    response = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=prompt
    )
    return response.output_text

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