import config, discord, api, asyncio, formatMessages

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Ready')

@client.event
async def on_message(message):

    if message.content.startswith('$hello'):

        await message.channel.send("Hello!")

    elif message.content.startswith('$anime'):

        def id_check(m):
            return len(m.content) >- 1

        await message.channel.send('Please enter the name of the anime you would like to search for: ')
        
        try:
            msg = await client.wait_for('message', check=id_check, timeout=10.0)
        except asyncio.TimeoutError:
            await message.channel.send("Request failed")
        else:
            await message.channel.send(f"Request succeeded, {msg.author}")

            data = api.getAnimeData(msg.content)
            embedMsg = formatMessages.createEmbed(data)

            await message.channel.send(embed=embedMsg)
        
        


client.run(config.API_KEY)