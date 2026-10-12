
from app import classify_ticket


def test_billing_ticket():
    result = classify_ticket(
        "I was charged twice for my subscription. Please fix this immediately."
    )
    assert result["category"] == "Billing"
    assert result["priority"] == "High"
    assert result["routing_queue"] == "Billing Support"
    print("Test 1 passed: Urgent billing issue")


def test_password_reset():
    result = classify_ticket("How do I reset my password?")
    assert result["category"] == "General"
    assert result["routing_queue"] == "General Support"
    assert "password-reset assistance" in result["response_draft"]
    print("Test 2 passed: Password reset")


def test_vague_ticket():
    result = classify_ticket("Something is wrong")
    assert result["category"] == "General"
    assert result["priority"] == "Low"
    assert result["routing_queue"] == "General Support"
    print("Test 3 passed: Vague issue")


def test_technical_ticket():
    result = classify_ticket(
        "The mobile app crashes whenever I try to open it."
    )
    assert result["category"] == "Technical"
    assert result["priority"] in ["Low", "Medium", "High"]
    assert result["routing_queue"] == "Technical Support"
    print("Test 4 passed: Technical issue")


def test_invoice_ticket():
    result = classify_ticket(
        "I have a question about the amount shown on my invoice."
    )
    assert result["category"] == "Billing"
    assert result["priority"] in ["Low", "Medium"]
    assert result["routing_queue"] == "Billing Support"
    assert result["response_draft"].strip()
    print("Test 5 passed: Invoice question")


if __name__ == "__main__":
    test_billing_ticket()
    test_password_reset()
    test_vague_ticket()
    test_technical_ticket()
    test_invoice_ticket()
    print("\nAll 5 tests passed!")
