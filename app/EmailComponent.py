from RPA.Email.ImapSmtp import ImapSmtp

from app.Constants import Constants

from qrlib.QRComponent import QRComponent
from qrlib.QREnv import QREnv
from qrlib.QRRunItem import QRRunItem


class EmailComponent(QRComponent):

    def __init__(self):
        super().__init__()
        self.gmail_account = None
        self.gmail_password = None
        self.smtp_server = None
        self.smtp_port = None
        self.logger = self.run_item.logger

        self.recipients_account = None

        self.mail = None
    
    def load_vault(self):
        self.gmail_account = QREnv.VAULTS["gmail"]["account"]
        self.gmail_password = QREnv.VAULTS["gmail"]["password"]
        self.smtp_server = QREnv.VAULTS["gmail"]["smtp_server"]
        self.smtp_port = QREnv.VAULTS["gmail"]["smtp_port"]
        self.recipients_account = QREnv.VAULTS["gmail"]["recipients_account"]

    def authorize(self):
        self.load_vault()

        self.mail = ImapSmtp(smtp_server=self.smtp_server, smtp_port=self.smtp_port)
        
        try:
            self.logger.info(f"Authorizing gmail as {self.gmail_account}")
            self.mail.authorize(account=self.gmail_account, password=self.gmail_password)
        except Exception as e:
            self.run_item.logger.info(f"Failed to authorize: {e}")
            raise e

    def send_mail(self):
        try:
            self.logger.info(f"Email sent successfully to {self.recipients_account}")
            self.mail.send_message(
                sender=self.gmail_account,
                recipients=self.recipients_account,
                subject="Message from Nishant's Bot",
                body="Here is summary of the scrapped movies data:",
                attachments=[Constants.excel_output_file_path]  
            )
        except Exception as e:
            self.run_item.logger.info(f"Failed to send email: {e}")
            raise e
