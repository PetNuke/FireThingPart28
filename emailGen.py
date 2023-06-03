import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def sendEmail(subj, body, to):
    host = "mail.lacanterajewelry.com"
    password = "4Pandora4"  # change accordingly

    # Create a multipart message
    message = MIMEMultipart()
    message["From"] = 'pandora@lacanterajewelry.com'
    message["To"] = to  # change accordingly
    message["Subject"] = subj  # change accordingly

    user = message['From']

    # body
    html = body

    # Attach the HTML content to the email
    message.attach(MIMEText(html, "html"))

    try:
        # Establish a secure SMTP connection
        server = smtplib.SMTP(host, 587)
        server.starttls()

        # Login to the SMTP server
        server.login(user, password)

        # Send the email
        server.sendmail(user, message["To"], message.as_string())

        print("Email sent successfully!")
    except Exception as e:
        print("An error occurred while sending the email:", str(e))
    finally:
        # Close the SMTP server connection
        server.quit()

