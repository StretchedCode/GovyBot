import config, discord, api, asyncio, formatMessages, db

intents = discord.Intents.all()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Ready')
    print(client.guilds)

@client.event
async def on_guild_join(guild):
    print(str(guild))

@client.event
async def on_message(message):

    if message.content.startswith('$hello'):

        await message.channel.send("Hello!")

    elif message.content.startswith('$anime/'):

        msgSummary = message.content.split("/")

        data = api.getAnimeData(msgSummary[1])
        embedMsg = formatMessages.createEmbed(data)

        newMsg = await message.channel.send(embed=embedMsg)
        await newMsg.add_reaction("❤️")

    elif message.content.startswith('$list'):
        content = db.fetchList(message.author.name, message.guild.name)
        embedList = formatMessages.createList(content, message.author)

        await message.channel.send(embed=embedList)

    elif message.content.startswith('$popular'):
        content = db.fetchPopular(message.guild.name)
        embedList = formatMessages.createList(content, message.author, message.guild.name)

        await message.channel.send(embed=embedList)

@client.event
async def on_reaction_add(reaction, user):
    if len(reaction.message.embeds) == 1 and reaction.message.channel.name == 'test':
        db.insert(user.name, reaction.message.embeds[0].title, reaction.message.guild.name)

@client.event
async def on_reaction_remove(reaction, user):
    if len(reaction.message.embeds) == 1 and reaction.message.channel.name == 'test':
        db.remove(user.name, reaction.message.embeds[0].title, reaction.message.guild.name)

client.run(config.API_KEY)