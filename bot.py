import discord
import random
import asyncio

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

TOKEN = 'SEU_TOKEN_AQUI'  # Substitua pelo token do seu bot
conexoes_ativas = {}

@client.event
async def on_ready():
    print(f'✅ Bot conectado como {client.user.name}')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    # .ping
    if message.content.lower().startswith('.ping'):
        await message.channel.send('🏓 Pong! Estou online.')

    # Solicitação de código de conexão
    if message.content.lower().startswith('.conectar'):
        usuario_id = message.author.id

        if usuario_id in conexoes_ativas:
            await message.channel.send('❗ Você já solicitou um código. Verifique sua DM.')
            return

        codigo = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        conexoes_ativas[usuario_id] = codigo

        try:
            await message.author.send(
                f'🔐 Seu código de conexão é: **{codigo}**\n'
                'Digite este código aqui nesta DM para concluir a autenticação.'
            )
            await message.channel.send('📩 Código enviado via mensagem privada (DM).')
        except discord.Forbidden:
            await message.channel.send('🚫 Não consegui enviar a DM. Verifique suas configurações de privacidade.')

    # Validação do código de conexão
    elif isinstance(message.channel, discord.DMChannel):
        usuario_id = message.author.id

        if usuario_id in conexoes_ativas:
            codigo_digitado = message.content.strip()
            codigo_gerado = conexoes_ativas[usuario_id]

            if codigo_digitado == codigo_gerado:
                await message.channel.send('✅ Conexão autorizada com sucesso!')
                del conexoes_ativas[usuario_id]
            else:
                await message.channel.send('❌ Código inválido. Tente novamente.')

client.run(TOKEN)
