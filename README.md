# Bot de Emails de Notificações do Google Classroom para o Discord
Este é um bot em Python que monitora contas de email em busca de novos emails e executa ações específicas com base no conteúdo dos emails. O bot foi desenvolvido para funcionar com contas do outlook e é especialmente útil para monitorar notificações do Google Classroom encaminhando as mesmas formatadas e personalizadas para um canal especifico de um servidor do Discord.

Recursos:

Conecta-se ao outlook usando o protocolo IMAP para buscar novos emails.
Verifica se o email é do Google Classroom e extrai informações relevantes.
Formata o conteúdo do email e envia para um canal no Discord para facilitar a notificação.
Executa continuamente em segundo plano, verificando periodicamente novos emails.
