from fpdf import FPDF
from django.core.files.uploadedfile import UploadedFile
from io import BufferedReader
from django.core.mail import EmailMessage
from GlazerBank import settings


MSG_FOR_SENDER = '''
<h1 style="text-align-center">Glazer bank limited</h1>
<p style="font-weight:bold;font-size:20px;">Hellow Mr/Ms {name}. For ur recent Transaction the ammount {ammount}
has been deduced from ur account.
Here is ur bank receipt:</p>
'''

MSG_FOR_RECEPIENT = '''
<h1 style="text-align-center">Glazer bank limited</h1>
<p style="font-weight:bold;font-size:20px;">Hellow Mr/Ms {name}. You have received a payment {ammount}$
From Mr/Ms{sender}
Here is ur bank receipt:</p>
'''



class PDF(FPDF):
    def header(self):
        # Set font and size
        self.set_font("Arial", size=12)

        # Add a title to the header
        self.cell(0, 10, "Sender and Receiver Information", align="C")
        self.ln()

    def footer(self):
        # Go to 1.5 cm from bottom
        self.set_y(-15)

        # Select Arial italic 8
        self.set_font("Arial", style="I", size=8)

        # Page number
        self.cell(0, 10, "Page %s" % self.page_no(), align="C")


def get_pdf_obj(sender_name, sender_id, receiver_name, receiver_id):
    pdf = PDF()

    # Add a page
    pdf.add_page()

    # Set font and size
    pdf.set_font("Arial", size=12)

    # Add sender information
    pdf.cell(0, 10, "Sender Name: " + sender_name, align="L")
    pdf.ln()
    pdf.cell(0, 10, "Sender ID: " + sender_id, align="L")
    pdf.ln()

    # Add receiver information
    pdf.cell(0, 10, "Receiver Name: " + receiver_name, align="L")
    pdf.ln()
    pdf.cell(0, 10, "Receiver ID: " + receiver_id, align="L")

    return pdf

    # Save the PDF

    # pdf.output("my_temp_pdf.pdf", "F")


def send_html_mail(subject, msg, recipient, attachments=None):
    mail = EmailMessage(
        subject=subject,
        body=msg,
        from_email=settings.EMAIL_HOST_USER,
        to=recipient
    )
    for attachment in attachments:
        mail.attach_file(attachment)
    mail.content_subtype = 'html'
    mail.send()
