import discord

def createEmbed(data):
    name = data["data"][0]["titles"][0]["title"]
    embedImg = data["data"][0]["images"]["jpg"]["image_url"]

    newEmbed = discord.Embed(title=name)
    newEmbed.set_image(url=embedImg)

    return newEmbed