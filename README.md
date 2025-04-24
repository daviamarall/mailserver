# ServerMail com Ansible

Este projeto configura um servidor de email local com Postfix usando Ansible. Além disso, inclui um script Python para realizar disparos de email em massa usando uma lista CSV de destinatários.

## Estrutura

- `playbook.yml`: Playbook principal do Ansible.
- `inventory.ini`: Inventário contendo os hosts gerenciados.
- `templates/main.cf.j2`: Template de configuração do Postfix.
- `scripts/disparar_emails.py`: Script para envio de emails em massa.

## Pré-requisitos

- Servidor Linux com acesso SSH.
- Python 3 e Ansible instalados localmente.

## Execução

```bash
ansible-playbook -i inventory.ini playbook.yml
```

## Disparo de Emails

Prepare um `lista_emails.csv` com o seguinte formato:

```csv
email,nome
usuario1@dominio.com,Fulano
usuario2@dominio.com,Ciclano
```

E execute o script:

```bash
python3 scripts/disparar_emails.py
```
---

## ✅ **Postfix + Domínio + Autenticação**
### 🔧 Pré-requisitos:
1. **Servidor Linux (Ubuntu/Debian de preferência)**
2. **Um domínio próprio** (ex: `seudominio.com`)
3. **Acesso ao painel DNS do domínio** (para configurar SPF, DKIM, etc.)
4. **IP fixo público** (opcional, mas altamente recomendado)
5. **Instalar o Postfix**

---

## 🚀 Passo a passo para Postfix como servidor SMTP local:

### 1. **Instale o Postfix e dependências**
```bash
sudo apt update
sudo apt install postfix mailutils libsasl2-2 ca-certificates libsasl2-modules -y
```

Durante a instalação, escolha:
- **"Internet Site"**
- Nome do sistema de e-mail: `mail.seudominio.com`

---

### 2. **Configure o Postfix**
Edite o arquivo principal:
```bash
sudo nano /etc/postfix/main.cf
```

Adicione ou ajuste essas linhas:
```ini
myhostname = mail.seudominio.com
mydomain = seudominio.com
myorigin = $mydomain
inet_interfaces = all
mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain
relayhost =
mynetworks = 127.0.0.0/8
home_mailbox = Maildir/
smtpd_banner = $myhostname ESMTP
smtpd_tls_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem
smtpd_tls_key_file=/etc/ssl/private/ssl-cert-snakeoil.key
smtpd_use_tls=yes
smtpd_sasl_auth_enable = yes
smtpd_sasl_type = dovecot
smtpd_sasl_path = private/auth
smtpd_sasl_security_options = noanonymous
```

---

### 3. **Configure SPF/DKIM/DMARC no DNS**
- **SPF**:  
  ```
  v=spf1 mx ip4:SEU_IP_PUBLICO include:_spf.google.com ~all
  ```

- **DKIM**: Use o `opendkim` para gerar e configurar.
- **DMARC** (opcional mas recomendado):  
  ```
  v=DMARC1; p=none; rua=mailto:admin@seudominio.com
  ```

---

### 4. **Teste envio de e-mail**
```bash
echo "Mensagem de teste" | mail -s "Assunto" destino@exemplo.com
```

---

## 📤 Disparo em Massa com Python + CSV

Crie um script simples que envia lendo de um CSV:

```python
import csv
import smtplib
from email.mime.text import MIMEText

# Configurações do servidor SMTP local
SMTP_SERVER = "127.0.0.1"
SMTP_PORT = 25

with open("lista.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        msg = MIMEText("Olá, segue nosso conteúdo exclusivo.")
        msg["Subject"] = "Campanha"
        msg["From"] = "suaempresa@seudominio.com"
        msg["To"] = row["email"]

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.send_message(msg)
```

---

## 🔒 Cuidado com:
- **Blacklist:** IPs dinâmicos e servidores sem reputação são bloqueados por muitos provedores.
- **Limite de envios:** Evite muitos disparos em curto tempo ou sem opt-in → risco de SPAM.
- **Considere usar Amazon SES, Mailgun, Sendgrid** se for para produção e precisar de escala.

---
**script + playbook Ansible** 

1. Instala e configura o **Postfix**.
2. Usa o domínio e hostname corretos.
3. Te prepara pra configurar **SPF, DKIM, DMARC**.
4. Te entrega o ambiente pronto pra enviar emails lendo um **CSV com Python**.

---

## 📁 Estrutura do projeto

```plaintext
email-disparador/
├── inventory.ini
├── playbook.yml
└── templates/
    └── main.cf.j2
```

---

### 🗂️ `inventory.ini`
```ini
[servidor_email]
192.168.1.100 ansible_user=seu_usuario ansible_ssh_private_key_file=~/.ssh/id_rsa
```

---

### 📜 `playbook.yml`

```yaml
---
- name: Configurar servidor de email com Postfix
  hosts: servidor_email
  become: yes

  vars:
    dominio_email: "seudominio.com"
    hostname_email: "mail.seudominio.com"

  tasks:
    - name: Instalar pacotes necessários
      apt:
        name:
          - postfix
          - mailutils
          - libsasl2-2
          - ca-certificates
          - libsasl2-modules
        update_cache: yes
        state: present

    - name: Configurar arquivo main.cf
      template:
        src: templates/main.cf.j2
        dest: /etc/postfix/main.cf
        owner: root
        group: root
        mode: '0644'
      notify: Reiniciar Postfix

    - name: Definir hostname
      hostname:
        name: "{{ hostname_email }}"

    - name: Habilitar serviço do Postfix
      service:
        name: postfix
        enabled: true
        state: started

  handlers:
    - name: Reiniciar Postfix
      service:
        name: postfix
        state: restarted
```

---

### 📄 `templates/main.cf.j2`

```ini
myhostname = {{ hostname_email }}
mydomain = {{ dominio_email }}
myorigin = $mydomain
inet_interfaces = all
mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain
relayhost =
mynetworks = 127.0.0.0/8
home_mailbox = Maildir/
smtpd_banner = $myhostname ESMTP
smtpd_tls_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem
smtpd_tls_key_file=/etc/ssl/private/ssl-cert-snakeoil.key
smtpd_use_tls=yes
smtpd_sasl_auth_enable = yes
smtpd_sasl_type = dovecot
smtpd_sasl_path = private/auth
smtpd_sasl_security_options = noanonymous
```

---

## 🚀 Como rodar

1. Edite o `inventory.ini` com o IP do seu servidor.
2. Rode o playbook:

```bash
ansible-playbook -i inventory.ini playbook.yml
```

---

## 🐍 Script Python para disparar com CSV

Salve como `disparar_emails.py`:

```python
import csv
import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "mail.seudominio.com"
SMTP_PORT = 25

with open("lista_emails.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        msg = MIMEText("Olá {{nome}}, tudo bem?")
        msg["Subject"] = "Campanha Teste"
        msg["From"] = "contato@seudominio.com"
        msg["To"] = row["email"]

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.send_message(msg)

print("Emails enviados com sucesso.")
```

---








