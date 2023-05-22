import threading
import time

from bs4 import BeautifulSoup
from colorama import Fore, Style
from imap_tools import AND, MailBox

import discord_bot
import discord_notify

# pegar emails de um remetente para um destinatário
username = "username"
password = "password"


def iniciar_loop_procurar_email():
    # Conectar ao servidor IMAP
    with MailBox('imap').login(username, password) as mailbox:
        # Selecionar a caixa de entrada
        mailbox.folder.set('INBOX')

        print(Fore.GREEN + 'Loop de verificação de emails iniciado!' + Style.RESET_ALL)
        while True:
            # Pesquisar por e-mails não lidos
            emails = mailbox.fetch('UNSEEN')

            for email in emails:
                verificar_tipo_email(email)

            time.sleep(1)


def verificar_tipo_email(email):
    if 'New material:' in email.subject or 'Due tomorrow:' in email.subject:
        print(Fore.YELLOW + 'novo email detectado.' + Style.RESET_ALL)
        email_formatado = formatar_email_classroom(email)
        email_formatado[0][0] = f'🟡 {email_formatado[0][0]}'
        email_formatado[0][2] = f'**{email_formatado[0][2]}**'
        email_formatado[0].append('@everyone')
        discord_notify.notificar_discord(*email_formatado)
        print(Fore.GREEN + 'Email enviado para o discord' + Style.RESET_ALL)


def formatar_email_classroom(email):
    # Analisar o HTML do e-mail com BeautifulSoup
    soup = BeautifulSoup(email.html, 'html.parser')

    # obtendo todos os textos do html table
    lista_textos = []
    for texto in soup.find('table').get_text(separator='__&').split('__&'):
        if not texto or texto == ' ' or texto == '.' or \
            'Google LLC 1600 Amphitheatre Parkway, Mountain View, CA 94043 USA' in texto \
            or "If you don't want to receive emails from Classroom, you can" in texto\
                or texto == 'unsubscribe' or texto == 'Open':
            continue

        if texto == 'New material':
            texto = f'{texto}:'
        lista_textos.append(texto)

    # obtendo os links e formatando os mesmos em uma lista
    links = []
    for link in soup.find_all('a'):
        link_formatado = str(link).split('"')[1]
        if 'https://' in link_formatado:
            links.append(link_formatado)

    # removendo o indice de unsubscribe do google
    link_open = ('Open', links[1])

    return (lista_textos, link_open)


print(Fore.YELLOW + 'Iniciando')

print('Iniciando Bot...')
try:

    threading.Thread(target=discord_bot.start_bot).start()
except Exception as erro:
    print(Fore.RED + f'Não foi possivel iniciar o bot.\nerro:{erro}' + Style.RESET_ALL)

print(Fore.GREEN + 'Bot iniciado!' + Style.RESET_ALL)

try:
    iniciar_loop_procurar_email()
except Exception as erro:
    print(Fore.RED +
          f'erro ao iniciar o loop de verificação de emails.\nerro:{erro}' + Style.RESET_ALL)
