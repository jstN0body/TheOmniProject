from discord.ext import commands
from discord import Embed, Colour

import Constants
import Inference

bot = commands.Bot(command_prefix="~")

@bot.command()
async def generate_quote(ctx, *, arg=None):
    quote = Inference.generate_quote(arg if not arg is None else "")

    await ctx.send(quote)
    await ctx.message.delete()

@bot.command(name="plzhelp")
async def help_command(ctx):
    help_embed = Embed(
        title="Omni Project Help",
        description="~generate_quote : generates an Omni-like quote."
                    "\n~generate_quote <prompt> : generates an Omni-like quote from a given prompt.",
        type="rich",
        colour=Colour.dark_purple()
    )
    await ctx.send(embed=help_embed)
    await ctx.message.delete()

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
