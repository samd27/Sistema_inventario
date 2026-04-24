import os

import requests


class EmailService:
    def __init__(self, app_config):
        self.brevo_api_key = app_config.get("BREVO_API_KEY") or os.environ.get("BREVO_API_KEY", "")
        self.brevo_sender_email = app_config.get("BREVO_SENDER_EMAIL") or os.environ.get("BREVO_SENDER_EMAIL", "")
        self.brevo_sender_name = app_config.get("BREVO_SENDER_NAME") or os.environ.get("BREVO_SENDER_NAME", "")
        self.brevo_api_url = app_config.get("BREVO_API_URL") or os.environ.get(
            "BREVO_API_URL",
            "https://api.brevo.com/v3/smtp/email",
        )
        self.alerts_to_email = app_config.get("ALERTS_TO_EMAIL") or os.environ.get("ALERTS_TO_EMAIL", "")

    def is_configured(self) -> bool:
        return all([
            self.brevo_api_key,
            self.brevo_sender_email,
            self.alerts_to_email,
        ])

    def send_low_stock_alert(self, subject: str, body: str):
        if not self.is_configured():
            return False, "Brevo no configurado"

        payload = {
            "sender": {
                "name": self.brevo_sender_name or "Sistema Inventario",
                "email": self.brevo_sender_email,
            },
            "to": [{"email": self.alerts_to_email}],
            "subject": subject,
            "htmlContent": f"<html><body><p>{body}</p></body></html>",
            "textContent": body,
        }

        headers = {
            "api-key": self.brevo_api_key,
            "accept": "application/json",
            "content-type": "application/json",
        }

        try:
            response = requests.post(self.brevo_api_url, json=payload, headers=headers, timeout=20)
            if 200 <= response.status_code < 300:
                return True, "Email enviado"
            return False, f"Brevo error {response.status_code}: {response.text}"
        except Exception as exc:
            return False, str(exc)
