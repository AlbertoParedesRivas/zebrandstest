import os
from requests import Response, post
from typing import List

# MUST ADD NEW RECIPIENTS TO MAILGuN FREE ACCOUNT
class MailgunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class Mailgun:

    MAILGUN_DOMAIN = os.environ.get("MAILGUN_DOMAIN")
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
    FROM_TITLE = "Changes in products catalog"
    FROM_EMAIL = f"mailgun@{MAILGUN_DOMAIN}"

    @classmethod
    def send_email(cls, email: List[str], subject: str, text: str, html:str) -> Response:
        if cls.MAILGUN_API_KEY is None:
            raise MailgunException("Failed to load API key")
        if cls.MAILGUN_DOMAIN is None:
            raise MailgunException("Failed to load Mailgun Domain")

        response = post(
            f"https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages",
            auth=("api",cls.MAILGUN_API_KEY),
            data={
                "from": f"{cls.FROM_TITLE} <{cls.FROM_EMAIL}>",
                "to": email,
                "subject": subject,
                "text": text,
                "html": html
            }
        )

        if response.status_code != 200:
            raise MailgunException("Error sending email")
        
        return response