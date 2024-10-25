import os
import smtplib as smtp
from email.message import EmailMessage

EMAIL = 'alexander.levinson.70@gmail.com'
PASSWORD = os.environ.get('APP2_PORTFOLIO_EMAIL_PASSWORD')


def send_email(tour_event: str):
    email_message = EmailMessage()
    email_message['Subject'] = 'New tour event appeared!'
    email_message.set_content(tour_event)
    gmail = smtp.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(EMAIL, PASSWORD)
    gmail.sendmail(EMAIL, EMAIL, email_message.as_string())
    gmail.quit()
    print(f"Email was sent with \"{tour_event}\" text.")


if __name__ == '__main__':
    send_email('Feng Suave, Minimalia City, 5.5.2089')
