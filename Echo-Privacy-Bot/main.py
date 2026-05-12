import discord
from discord import app_commands
import datetime
from groq import Groq

# ========================== TOKENS ==========================
DISCORD_TOKEN = "MTUwMzU2NjAwNDgyMTk1MDU5NQ.GPwP8j.4HXZX_IkHRTEb0KzslL6Bt2k7CEsw2qmhM7f1Y"
GROQ_API_KEY = "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"

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

groq_client = Groq(api_key=GROQ_API_KEY)

# ====================== 3 CUSTOM TOOLS ======================
@tree.command(name="calculator", description="Simple calculator")
@app_commands.describe(operation="add/subtract/multiply/divide", a="first number", b="second number")
async def calculator(interaction: discord.Interaction, operation: str, a: float, b: float):
    if operation == "add":
        result = a + b
    elif operation == "subtract":
        result = a - b
    elif operation == "multiply":
        result = a * b
    elif operation == "divide":
        result = a / b if b != 0 else "Cannot divide by zero"
    else:
        result = "Unknown operation"
    embed = discord.Embed(title="Calculator", description=f"{a} {operation} {b} = {result}", color=0x00ff88)
    await interaction.response.send_message(embed=embed)

@tree.command(name="time", description="Current UTC time")
async def current_time(interaction: discord.Interaction):
    now = datetime.datetime.now(datetime.UTC)
    embed = discord.Embed(title="Current Time (UTC)", description=now.strftime("%Y-%m-%d %H:%M:%S UTC"), color=0x00ff88)
    await interaction.response.send_message(embed=embed)

@tree.command(name="privacy", description="Privacy reminder")
async def privacy_check(interaction: discord.Interaction):
    embed = discord.Embed(title="Privacy Check", description="Echo Privacy Bot respects your privacy 100%. No data is sent to third-party servers.", color=0x00ff88)
    await interaction.response.send_message(embed=embed)

# ====================== AI CHAT ======================
@tree.command(name="chat", description="Talk to the AI agent")
@app_commands.describe(message="Your message")
async def chat(interaction: discord.Interaction, message: str):
    await interaction.response.defer()
    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": message}],
            temperature=0.7,
            max_tokens=800
        )
        reply = completion.choices[0].message.content
    except Exception as e:
        reply = f"Error: {str(e)}"
    embed = discord.Embed(title="Echo Privacy Bot", description=reply, color=0x00ff88)
    await interaction.followup.send(embed=embed)

@bot.event
async def on_ready():
    await tree.sync()
    print(f"{bot.user} is online! (Echo Privacy Bot)")
    print("Slash commands are ready. Test them in your Discord server now!")

bot.run(DISCORD_TOKEN)