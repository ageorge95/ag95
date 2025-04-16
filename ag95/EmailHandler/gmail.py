from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from traceback import format_exc

def send_mail_from_gmail(subject: str,
                         message: str,
                         send_from: str,
                         send_to: str,
                         password: str):
    '''

    Args:
        subject: The subject of the email.
        message: The body of the email.
        send_from: The sender address; Must be a gmail address.
        send_to: The receiver of the email; Currently only 1 receiver is supported.
        password: The password used to log in to the send_from gmail account.

    Returns:
        {'success': True, 'extra': ''} if everything was ok OR
         {'success': True, 'extra': <the traceback message>} if there was an error
    '''
    try:
        # setup the parameters of the message
        msg = MIMEMultipart()
        msg['From'] = send_from
        msg['To'] = send_to
        msg['Subject'] = subject

        # add in the message body
        msg.attach(MIMEText(message
                            .replace('\n', '<br>')
                            .replace('\t', 4*'&nbsp;')
                            .replace('  ', 2*'&nbsp;'), 'html'))

        #create the server
        server = SMTP('smtp.gmail.com: 587')

        server.starttls()

        # Login Credentials for sending the mail
        server.login(msg['From'], password)

        # send the message via the server
        server.sendmail(msg['From'], msg['To'], msg.as_string())

        server.quit()

        print("successfully sent email to %s" % (msg['To']))

        return {'success': True, 'extra': ''}

    except:
        traceback_message = format_exc(chain=False)
        print(f'Failed to send the email !\n{traceback_message}')

        return {'success': False,
                'extra': traceback_message}

if __name__ == '__main__':
    send_from = ''
    send_to = ''
    password = ''

    send_mail_from_gmail(subject='My test email subject',
                         message='My test email body',
                         send_from=send_from,
                         send_to=send_to,
                         password=password)

    print(f'No automatic tests implemented so far;'
          f' Please check the expected behavior manually:'
          f' an email should have been sent from {send_from} to {send_to}')