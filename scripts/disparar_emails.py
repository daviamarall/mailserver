import csv
import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "mail.seudominio.com"
SMTP_PORT = 25

with open("lista_emails.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        nome = row.get("nome", "")
        msg = MIMEText(f"Olá {nome}, tudo bem?")
        msg["Subject"] = "Campanha Teste"
        msg["From"] = "contato@seudominio.com"
        msg["To"] = row["email"]

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.send_message(msg)

print("Emails enviados com sucesso.")
