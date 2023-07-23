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

@client.event
async def on_reaction_add(reaction, user):
    if len(reaction.message.embeds) == 1:
        testGuild = client.get_guild(916526515406118933)
        db.insert(user.name, reaction.message.embeds[0].title, testGuild.name)

@client.event
async def on_reaction_remove(reaction, user):
    if len(reaction.message.embeds) == 1:
        testGuild = client.get_guild(916526515406118933)
        db.remove(user.name, reaction.message.embeds[0].title, testGuild.name)

        
        


client.run(config.API_KEY)