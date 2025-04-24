# Mailserver com Ansible

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
