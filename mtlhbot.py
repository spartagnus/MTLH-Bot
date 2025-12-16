import discord
import aiohttp
import io
import os
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

SOURCE_CHANNEL_ID = 1331467178209312837
DESTINATION_CHANNEL_ID = 1331472963668541531

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != SOURCE_CHANNEL_ID:
        return

    if not message.attachments:
        return

    for attachment in message.attachments:
        if attachment.filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
            dest_channel = bot.get_channel(DESTINATION_CHANNEL_ID)
            if not dest_channel:
                print("Destination channel not found")
                return

            # Download and attach file to avoid broken images
            async with aiohttp.ClientSession() as session:
                async with session.get(attachment.url) as resp:
                    if resp.status == 200:
                        data = await resp.read()
                        file = discord.File(io.BytesIO(data), filename=attachment.filename)
                        embed = discord.Embed(
                            description=f"Posted by {message.author.mention}",
                            color=discord.Color.blue()
                        )
                        embed.set_image(url=f"attachment://{attachment.filename}")
                        await dest_channel.send(embed=embed, file=file)

            # Delete original message
            try:
                await message.delete()
            except discord.Forbidden:
                print("Cannot delete message - missing permissions")

            # DM confirmation
            try:
                await message.author.send(
                    "✅ Your profile picture has been submitted. Please allow some time for an admin to verify."
                )
            except discord.Forbidden:
                print(f"Cannot DM {message.author}")

            break  # only first valid attachment

    await bot.process_commands(message)

bot.run(os.getenv("DISCORD_TOKEN"))
