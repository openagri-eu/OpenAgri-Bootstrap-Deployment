import docker
import requests
import logging
from datetime import datetime

# Docker client
client = docker.from_env()

# Log file setup
LOG_FILE = "./docker_service_monitor.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

# Postmark Email Config
POSTMARK_API_KEY = "API_KEY"
EMAIL_FROM = "FROM_EMAIL"
EMAIL_TO = ["TO_EMAILS"]
POSTMARK_API_URL = "https://api.postmarkapp.com/email"

# Events to monitor
ALERT_EVENTS = ["stop", "kill", "restart"]

def send_email(service_name, status):
    """Send an email alert via Postmark if a service status changes."""
    subject = f"[ALERT] Service {service_name} is now {status}"
    body = f"Service '{service_name}' changed status to '{status}' at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."

    email_data = {
        "From": EMAIL_FROM,
        "To": ", ".join(EMAIL_TO),
        "Subject": subject,
        "TextBody": body
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Postmark-Server-Token": POSTMARK_API_KEY
    }

    try:
        response = requests.post(POSTMARK_API_URL, json=email_data, headers=headers)
        response.raise_for_status()  # Raise an error for non-200 responses
        logging.info(f"Email sent successfully: {service_name} is now {status}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send email: {str(e)}")


def monitor_services():
    """Monitor Docker events and log service status changes."""
    for event in client.events(decode=True):
        if event.get("Type") == "container":
            container_id = event.get("id")
            status = event.get("status")
            container = client.containers.get(container_id)
            service_name = container.name

            # Send email only if status is stop, kill, or restart
            if status in ALERT_EVENTS:
                logging.info(f"Service {service_name} changed to {status}")
                send_email(service_name, status)


if __name__ == "__main__":
    logging.info("Starting Docker Service Monitor...")
    monitor_services()
