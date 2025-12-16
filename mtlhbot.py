import discord
import os
from discord.ext import commands

# -----------------------
# Bot Intents
# -----------------------
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# -----------------------
# Channel IDs
# -----------------------
SOURCE_CHANNEL_ID = 1331467178209312837
DESTINATION_CHANNEL_ID = 1331472963668541531

# -----------------------
# Events
# -----------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_message(message):
    # Ignore bots (including itself)
    if message.author.bot:
        return

    # Only act in the source channel
    if message.channel.id != SOURCE_CHANNEL_ID:
        return

    # Must contain an attachment
    if not message.attachments:
        return

    for attachment in message.attachments:
        # Only allow image files
        if attachment.filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):

            destination_channel = bot.get_channel(DESTINATION_CHANNEL_ID)
            if not destination_channel:
                print("Destination channel not found.")
                return

            # Create embed
            embed = discord.Embed(
                description=f"Posted by {message.author.mention}",
                color=discord.Color.blue()
            )
            embed.set_image(url=attachment.url)

            # Send embed
            await destination_channel.send(embed=embed)

            # Delete original message
            await message.delete()

            # DM confirmation to user
            try:
                await message.author.send(
                    "✅ Your profile picture has been submitted.\n"
                    "Please allow some time for an R4 to verify it."
                )
            except discord.Forbidden:
                print(f"Could not DM {message.author} (DMs disabled).")

            break  # Only process first valid image

    await bot.process_commands(message)

# -----------------------
# Start Bot (Railway-safe)
# -----------------------
bot.run(os.getenv("DISCORD_TOKEN"))
