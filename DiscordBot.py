from discord.ext import commands

import Constants
import Inference

bot = commands.Bot(command_prefix="~")

@bot.command()
async def generate_quote(ctx):
    quote = Inference.generate_quote()
    await ctx.send(quote)
    await ctx.message.delete()

@bot.command(name="plzhelp")
async def help_command(ctx):
    await ctx.send("Use ~generate_quote <prompt> to generate an Omni-like quote\n"
                   "Use ~scrape_messages to yoink messages from Omni")

@bot.command()
async def scrape_messages(ctx):
    await ctx.send("Searching for messages from Omni in the last 15,000 messages of this channel.")
    with open("./storage/omni_project/scraped_messages.txt", 'ab') as file:
        async for message in ctx.channel.history(limit = 15000):
            if message.author.id == Constants.user_id:
                # append only messages that do not contain mentions, stickers, or attachments
                if not "<" in message.content and not ">" in message.content and not "http" in message.content \
                        and len(message.attachments) == 0:
                    file.write((message.content + "\n").encode())
    await ctx.send("Done.")


bot.run(Constants.token)
