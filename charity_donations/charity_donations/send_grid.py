import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from local_settings import EMAIL_PASSWORD

# try:
#     from charity_donations.local_settings import EMAIL_PASSWORD
# except ModuleNotFoundError:
#     print("No password in local_settings.py!")
#     print("Update data and try again!")
#     exit(0)

message = Mail(
    from_email='szachista49@wp.pl',
    to_emails='szachista49@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient('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')
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)


