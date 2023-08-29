import pikepdf
import s3cret5 as passwords


def remove_password_from_pdf(filename, password=passwords.DOCUMENTS_PDF_PASSWORD):
    pdf = pikepdf.open(filename, password=password)
    # pdf.save("pdf_file_with_no_password.pdf")
    pdf.save(filename)
