import smtplib
from socket import gaierror


class MailExpress:
    def __init__(self, smtp_server: str, port: int, login: str, password: str | int) -> None:
        self.smtp_server = smtp_server
        self.port = port
        self.login = login
        self.password = password

    def __str__(self):
        print(
            f'MailExpress Class for {self.smtp_server} {self.port} {self.login} {self.password}')

    def send_informative_message(self, sender: str, reciver: str, subject: str, body: str) -> None:
        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                message = f"""\
                Subject: {subject}
                To: {reciver}
                From: {sender}

                {body}

                """.encode('utf-8').strip()

                server.login(self.login, self.password)
                server.sendmail(sender, reciver, message)
        except (gaierror, ConnectionRefusedError):
            print('Failed to connect to the server. Bad connection settings?')
        except smtplib.SMTPServerDisconnected:
            print('Failed to connect to the server. Wrong user/password?')
        except smtplib.SMTPException as e:
            print(f'SMTP error occurred: {e}')
