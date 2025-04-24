import smtplib
from email.mime.text import MIMEText

def send_notification(message):
    msg = MIMEText(message)
    msg['Subject'] = 'Intrusion Detected'
    msg['From'] = 'your_email@example.com'
    msg['To'] = 'admin_email@example.com'

    with smtplib.SMTP('smtp.example.com') as server:
        server.login('your_email@example.com', 'your_password')
        server.send_message(msg)

if __name__ == "__main__":
    # Example Usage
    send_notification("Potential intrusion detected in the network.")