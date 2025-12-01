from infra.logger import get_logger

logger = get_logger("custom_tool")

def send_email_stub(to: str, subject: str, body: str) -> dict:
    """
    Stub function to simulate sending an email.
    Replace with actual email API integration if needed.
    Logs the action and returns a simulated success response.
    """
    logger.info(f"[CustomTool] Sending email to {to} with subject: {subject}")
    print(f"[stub] Sending email to {to} with subject: {subject}")
    
    return {
        "status": "sent",
        "to": to,
        "subject": subject,
        "body": body
    }