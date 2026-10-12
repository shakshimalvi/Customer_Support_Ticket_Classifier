# Customer Support Ticket Classifier

An AI-powered application that automatically classifies customer support tickets, assigns a priority, routes them to the appropriate support team, and generates a suggested response.

## Problem Statement

Manually sorting customer support tickets can delay responses. This project uses a language model to help organize tickets consistently and reduce manual classification effort.

## Features

- **Ticket Classification:** Categorizes tickets as Billing, Technical, or General.
- **Priority Assignment:** Assigns Low, Medium, or High priority.
- **Automatic Routing:** Recommends the appropriate support queue.
- **Response Drafting:** Generates a polite response based on the ticket text.
- **Structured Output:** Returns the result as JSON.
- **Interactive Dashboard:** Provides a Streamlit interface for entering and analyzing tickets.
- **API Key Protection:** Uses environment variables to keep credentials out of source code.

## Technology Stack

- Python
- NVIDIA API
- OpenAI-compatible Python client
- Streamlit
- python-dotenv
- JSON

## Project Structure

```text
Customer_Support_Ticket_Classifier/
├── app.py
├── streamlit_app.py
├── test_app.py
├── requirements.txt
├── .gitignore
├── .env                 
└── README.md
```

## Example

**Input:**

```text
I was charged twice for my subscription.
Please fix this immediately.
```

**Example output:**

```json
{
  "category": "Billing",
  "priority": "High",
  "routing_queue": "Billing Support",
  "response_draft": "Thank you for reaching out. I'm sorry to hear you were charged twice. Could you please provide the dates or transaction IDs of the charges so we can investigate further?"
}
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Customer_Support_Ticket_Classifier
```


### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project folder:

```text
NVIDIA_API_KEY=your_nvidia_api_key_here
```

### 5. Run the application

```bash
python -m streamlit run streamlit_app.py
```

### 6. Run automated tests

```bash
python test_app.py
```

## Expected Output Fields

| Field | Description |
|---|---|
| `category` | Billing, Technical, or General |
| `priority` | Low, Medium, or High |
| `routing_queue` | Recommended support team |
| `response_draft` | Suggested reply to the customer |

## Limitations

- Results depend on the language model and may vary between runs.
- Suggested responses should be reviewed before being sent to customers.
- The application does not independently verify account details, payments, or refunds.
- The model requires a valid API key and network access.

## Future Improvements

- Improve consistency of priority assignment.
- Add more automated test cases.
- Deploy the Streamlit application online.
- Add ticket history and analytics.

## Disclaimer

This project is intended for learning and demonstration. It assists with ticket triage but does not replace human review.
