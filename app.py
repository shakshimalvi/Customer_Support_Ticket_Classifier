
import os
import json
from unittest import result
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

if not NVIDIA_API_KEY:
    try:
        import streamlit as st
        NVIDIA_API_KEY = st.secrets["NVIDIA_API_KEY"]
    except Exception:
        NVIDIA_API_KEY = None

if not NVIDIA_API_KEY:
    raise ValueError(
        "NVIDIA_API_KEY is missing. Configure it in your .env "
        "file locally or in Streamlit Cloud Secrets."
    )

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)

MODEL = "openai/gpt-oss-20b"


def classify_ticket(ticket_text):
    prompt = f"""

You are a customer support ticket classifier.

Analyze only the provided customer ticket.
Do not use external information or invent facts.

Return exactly four JSON fields:
category, priority, routing_queue, response_draft.

CATEGORY RULES:
1. Use "Billing" for duplicate charges, payments,
   invoices, and billing-related problems.
2. Use "Technical" for software errors, app crashes,
   and technical malfunctions.
3. Use "General" for general questions, password-reset
   questions, vague messages, or issues that do not
   clearly fit another category.

PRIORITY RULES:
1. Use "High" for explicitly urgent billing issues
   or issues clearly blocking essential work.
2. Use "Medium" for specific problems that need
   attention but are not described as urgent.
3. Use "Low" for general questions and vague messages
   without signs of urgency.
4. Never infer urgency without evidence in the ticket.

ROUTING RULES:
1. Billing -> "Billing Support"
2. Technical -> "Technical Support"
3. General -> "General Support"


RESPONSE RULES:
1. Be polite, concise, and professional.
2. Do not invent troubleshooting steps or company policies.
3. Do not claim that a refund, repair, or account change
   has already happened.
4. Do not promise a resolution or a timeline.
5. If details are missing, ask a short clarifying question.
6. For password-reset questions, ask what assistance
   the customer needs instead of inventing instructions.
7. Use grammatically correct sentences.
8. Use only information supported by the ticket.


Return valid JSON only, without Markdown fences.

Customer ticket:
{json.dumps(ticket_text)}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Return exactly one valid JSON object with "
                    "category, priority, routing_queue, and "
                    "response_draft. Do not use Markdown."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=800
    )

    choice = response.choices[0]

    if choice.finish_reason == "length":
        raise ValueError(
            "Response was truncated. Please retry."
        )

    result_text = choice.message.content

    if not result_text:
        raise ValueError("The model returned an empty response.")

    result = json.loads(result_text)

    required_fields = {
        "category",
        "priority",
        "routing_queue",
        "response_draft"
    }

    if not isinstance(result, dict):
        raise ValueError("Output must be a JSON object.")

    if set(result.keys()) != required_fields:
        raise ValueError("Unexpected output fields.")

    for field in required_fields:
        if not isinstance(result[field], str):
            raise ValueError(
                f"Field '{field}' must contain text."
            )

    if result["priority"] not in {"Low", "Medium", "High"}:
        raise ValueError("Invalid priority returned by model.")
    
    # Check that the category is supported.
    allowed_categories = {"Billing", "Technical", "General"}

    if result["category"] not in allowed_categories:
        raise ValueError("Invalid category returned by model.")

    # Check that the routing queue matches the category.
    expected_queues = {
        "Billing": "Billing Support",
        "Technical": "Technical Support",
        "General": "General Support"
    }

    expected_queue = expected_queues[result["category"]]

    if result["routing_queue"] != expected_queue:
        raise ValueError("Routing queue does not match category.")
    
    # Safe response for password-reset questions.
    if (
        result["category"] == "General"
        and "password" in ticket_text.lower()
        and "reset" in ticket_text.lower()
    ):
        result["response_draft"] = (
            "Thank you for reaching out. "
            "Could you please share more details about "
            "the password-reset assistance you need?"
        )

    # Safe, consistent response for duplicate billing charges.
    if (
        result["category"] == "Billing"
        and "charged twice" in ticket_text.lower()
    ):
        result["response_draft"] = (
            "Thank you for reaching out. "
            "I'm sorry to hear you were charged twice. "
            "Could you please provide the dates or transaction IDs "
            "of the charges so we can investigate further?"
        )

    return result

if __name__ == "__main__":
    test_tickets = [
        "I was charged twice for my subscription. "
        "Please fix this immediately.",
        "How do I reset my password?",
        "Something is wrong",
        "The mobile app crashes whenever I try to open it.",
        "I have a question about the amount shown on my invoice."
    ]

    for i, ticket in enumerate(test_tickets, start=1):
        print(f"\n--- Test Case {i} ---")
        print("Ticket:", ticket)

        try:
            output = classify_ticket(ticket)
            print(json.dumps(output, indent=4))
        except Exception as e:
            print(f"Error: {e}")
