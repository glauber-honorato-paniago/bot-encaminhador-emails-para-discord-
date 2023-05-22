import discord
import pyshorteners


class MyButton(discord.ui.Button):
    def __init__(self, titlulo_botao, link):
        super().__init__(style=discord.ButtonStyle.link, label=titlulo_botao, url=link)


def enviar_mensagem_discord(mensagem, link):
    class MyClient(discord.Client):
        async def on_ready(self):
            print(f'Logged on as {self.user}!')

            curto = pyshorteners.Shortener()
            link_curto = (link[0], curto.tinyurl.short(link[1]))
            channel_id = 'channel id'
            channel = client.get_channel(channel_id)

            if channel:
                button = MyButton(*link_curto)
                message = await channel.send('\n'.join(mensagem))
                view = discord.ui.View()
                view.add_item(button)
                await message.edit(view=view)

            await client.close()

    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)
    client.run('token')
