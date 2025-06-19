import os
import discord
import random as r
from dotenv import load_dotenv
from discord import app_commands, Interaction, Embed

# Setup Credentials
load_dotenv()
BOT_TOKEN = os.getenv("discord_token_2")
GUILD_ID = 1361781854700572682
ALLOWED_USERS = [895402417112375296]

# Setup
intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)
fun_responses = ['ᓚᘏᗢ',
'ฅ^•ﻌ•^ฅ',
r"""(\\ (\
( -.-)
o_(")(")"""]

@client.event
async def on_ready():
    print(f"Bot is ready. Logged in as {client.user} (ID: {client.user.id})")
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print("commands synced to guild")

@tree.command(name="ping", description="sends ping of bot", guild=discord.Object(id=GUILD_ID))
async def ping(interaction: discord.Interaction):
    latency = client.latency * 1000  # Convert to ms
    await interaction.response.send_message(f'Pong! `{latency:.2f}ms`', ephemeral=True)

@tree.command(name="fun", description="List of fun commands", guild=discord.Object(id=GUILD_ID))
async def fun(interaction: discord.Interaction):
    r.seed(interaction.id)
    await interaction.response.send_message(r.choice(fun_responses), ephemeral=True)

@tree.command(name="speak", description="responds with what you type", guild=discord.Object(id=GUILD_ID))
async def speak(interaction: discord.Interaction, message: str):
    if interaction.user.id in ALLOWED_USERS:
        await interaction.response.send_message("Message sent!", ephemeral=True)
        await interaction.channel.send(message)
    else:
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)

@tree.command(name="rules", description="sends rules of the server", guild=discord.Object(id=GUILD_ID))
async def rules(interaction: discord.Interaction):
    embed = discord.Embed(title="📜 LAW OF THE LAND", description="Please read and follow these rules carefully:", color=discord.Color.dark_red())
    embed.add_field(name="1. Don't be offensive or discriminate", value="No hate speech, slurs, or targeted harassment.", inline=False)
    embed.add_field(name="2. Don't send NSFW", value="Keep all content safe for work. No explicit or suggestive material.", inline=False)
    embed.add_field(name="3. Be respectful", value="Treat everyone kindly. No bullying or toxic behavior.", inline=False)
    embed.add_field(name="4. Don't spam", value="Avoid flooding chats with messages, images, or pings.", inline=False)
    embed.add_field(name="5. English ONLY", value="English is required so mods can effectively monitor the server.", inline=False)
    embed.add_field(name="6. Have fun", value="This is a community — enjoy it! Just don’t ruin the fun for others.", inline=False)
    embed.add_field(name="⚠️ Rule Enforcement", value="Breaking rules may result in a kick or ban — **especially rule 6!**", inline=False)
    embed.set_footer(text="Thanks for being part of 780 Club!")
    await interaction.response.send_message(embed=embed)

@tree.command(name="about", description="about the bot", guild=discord.Object(id=GUILD_ID))
async def about(interaction: discord.Interaction):
    embed = discord.Embed(
        title="About The Bot",
        color=discord.Color.dark_green()
    )
    embed.add_field(name="Who it is by?", value="Its a joint effort by Vesteria_", inline=False)
    embed.set_footer(text="Thanks for being part of Vesteria Club!")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(guild=discord.Object(id=GUILD_ID), name="create_ticket", description="Create a new support ticket")
async def create_ticket(interaction: discord.Interaction):
    category = discord.utils.get(interaction.guild.categories, name="Tickets")
    if not category:
        category = await interaction.guild.create_category("Tickets")
    existing = discord.utils.get(category.channels, name=f"ticket-for-{interaction.user.name}")
    if existing:
        await interaction.response.send_message(f"You already have an open ticket: {existing.mention}", ephemeral=True)
        return
    overwrites = {
        interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
        interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True)
    }
    channel = await interaction.guild.create_text_channel(
        name=f"ticket-for-{interaction.user.name}",
        category=category,
        overwrites=overwrites
    )
    await interaction.response.send_message(f"Ticket created: {channel.mention}", ephemeral=True)


@tree.command(guild=discord.Object(id=GUILD_ID), name="close_ticket", description="Close the current ticket")
async def close_ticket(interaction: discord.Interaction):
    if "ticket—for" in interaction.channel.name:
        await interaction.channel.delete()
        await interaction.response.send_message("Ticket closed", ephemeral=True)
    else:
        await interaction.response.send_message("This isn't a ticket channel!", ephemeral=True)

@tree.command(name="help", description="sends list of commands", guild=discord.Object(id=GUILD_ID))
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title="Server Commands", description="Here is a list of available bot commands:", color=discord.Color.dark_green())
    embed.add_field(name="/ping", value="Shows the current latency of the bot.", inline=False)
    embed.add_field(name="/fun", value="Sends a fun random cat-like emoticon.", inline=False)
    embed.add_field(name="/rules", value="Displays the server rules", inline=False)
    embed.add_field(name="/about", value="Gives information about this bot and its creators.", inline=False)
    embed.add_field(name="/create_ticket", value="Creates a private support ticket channel for you.", inline=False)
    embed.add_field(name="/close_ticket", value="Closes the ticket channel you are in.", inline=False)
    embed.add_field(name="/help", value="Displays this help message.", inline=False)
    embed.add_field(name="/socials", value="Displays 780's social media.", inline=False)
    embed.set_footer(text="Thanks for being part of 780 Club!")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="socials", description="send 780's socials media", guild=discord.Object(id=GUILD_ID))
async def socials(interaction: discord.Interaction):
    embed = discord.Embed(title="Social Media")
    embed.add_field(name="Youtube", value="https://www.youtube.com/channel/UCHw4DRU1HqfVimsrVOrplBA", inline=False)
    embed.set_footer(text="Thanks for being part of 780 Club!")
    await interaction.response.send_message(embed=embed, ephemeral=True)

client.run(BOT_TOKEN)
