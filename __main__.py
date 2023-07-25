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

    elif message.content.startswith('$anime'):

        msgSummary = message.content.split("$anime")

        data = api.getAnimeData(msgSummary[1])
        embedMsg = formatMessages.createEmbed(data)

        newMsg = await message.channel.send(embed=embedMsg)
        await newMsg.add_reaction("❤️")

    elif message.content.startswith('$list'):

        params = message.content.split(" ")
        limit = 10
        user = message.author.name
        guild = message.guild.name
        

        for x in range(1, len(params) - 1):

            if params[x] == '-u':
                user = params[x + 1]
            elif params[x] == '-l':
                limit = int(params[x + 1])

        content = db.fetchList(user=user, limit=limit, guildname=guild)

        embedList = formatMessages.createList(data=content, user=user, limit=limit)
        

        await message.channel.send(embed=embedList)

    elif message.content.startswith('$popular'):

        params = message.content.split(" ")

        if len(params) > 1:
            content = db.fetchPopular(message.guild.name, limit=int(params[1]))
            embedList = formatMessages.createList(data=content, user=message.author, guildname=message.guild.name, limit=int(params[1]))
        else:
            content = db.fetchPopular(message.guild.name)
            embedList = formatMessages.createList(data=content, user=message.author, guildname=message.guild.name)

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