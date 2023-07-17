import discord

def createEmbed(data):
    name = data["data"][0]["titles"][0]["title"]
    embedImg = data["data"][0]["images"]["jpg"]["image_url"]
    description = data["data"][0]["synopsis"]

    newEmbed = discord.Embed(title=name, color=discord.Colour.from_rgb(219, 172, 52), description=description)
    newEmbed.set_image(url=embedImg)

    return newEmbed