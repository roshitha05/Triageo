import csv
import os
import time

from dotenv import load_dotenv
from google import genai

from prompts import PROMPT_V1, PROMPT_V2, PROMPT_V3


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


PROMPTS = {
    "V1": PROMPT_V1,
    "V2": PROMPT_V2,
    "V3": PROMPT_V3,
}


def analyse_with_prompt(ticket, prompt_template):
    prompt = prompt_template.format(ticket=ticket)

    response = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=prompt
    )

    return response.output_text


with open("data/test_tickets.csv", newline="", encoding="utf-8") as file:
    tickets = list(csv.DictReader(file))


results = []

for ticket_data in tickets:
    ticket = ticket_data["ticket"]

    print(f"\nTesting: {ticket}")

    result = {
        "ticket": ticket,
        "expected_category": ticket_data["expected_category"],
        "expected_priority": ticket_data["expected_priority"],
    }

    for version, prompt in PROMPTS.items():
        print(f"Running {version}...")

        output = analyse_with_prompt(ticket, prompt)

        result[f"{version}_output"] = output

        time.sleep(1)

    results.append(result)


fieldnames = [
"ticket",
"expected_category",
"expected_priority",
"V1_output",
"V2_output",
"V3_output",
]

with open(
"data/results.csv",
"w",
newline="",
encoding="utf-8"
) as file:

    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(results)


print("\nEvaluation complete.")
print("Results saved to data/results.csv")
