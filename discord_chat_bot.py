from discord.ext import commands
import asyncio
import discord
import datetime
import requests
from discord import File
from PIL import Image, ImageFont, ImageDraw
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

TOKEN = ''

url = "https://dad-jokes.p.rapidapi.com/random/joke"

offensive_words = []

client = commands.Bot(command_prefix='/', intents=discord.Intents.all(),
                      activity=discord.Activity(type=discord.ActivityType.playing))


@client.event
async def on_member_join(member):
    await client.get_channel().send("Обръщение към: " + "{}".format(member.mention))
    image = Image.open('bojigol.png')

    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('times.ttf', 30)
    text = "Здраве желаем, другарю.\nДобре дошъл в {} {}".format(member.guild.name, member.mention)

    text_x = 280
    text_y = 5
    text_color = (255, 255, 255)

    lines = ["Здраве желаем, другарю.", "Добре дошъл в:", "{}".format(member.guild.name)]
    for line in lines:
        draw.text((text_x, text_y), line, fill=text_color, font=font)
        text_y += 50
    image.save('image_with_text.jpg')

    file_path = os.path.join(os.getcwd(), 'image_with_text.jpg')
    with open(file_path, 'rb') as f:
        image_with_text = discord.File(f)

    await client.get_channel().send(file=image_with_text)
    role = discord.utils.get(member.guild.roles, name='НР България')
    await member.add_roles(role)


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.command()
async def helpme(ctx):
    help_embed = discord.Embed(title="Команди", description="Списък на командите:", color=discord.Color.red())
    help_embed.add_field(name="weather", value="Показва температурата в реално време", inline=False)
    help_embed.add_field(name="koi sme nie / кои сме ние", value="Ем показва кои сме ние", inline=False)
    help_embed.add_field(name="time", value="Показва колко е часа", inline=False)
    help_embed.set_footer(text="По бай Тошево време нямаше такива Ботове")
    await ctx.send(embed=help_embed)


is_message_sent = False


@client.event
async def on_message(message):
    global is_message_sent
    if message.content == "dad joke" or message.content == "dad jokes":
        headers = {
            "X-RapidAPI-Key": "55c599f48amshbc09d50aed85e7bp13be40jsna35d4003b358",
            "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers)

        data = response.json()["body"][0]
        punchline = data["punchline"]

        response_text = f"{data['setup']}\n\n||{punchline}||"

        await message.channel.send(response_text)
    if message.content == 'кои сме ние' or message.content == 'koi sme nie' or message.content == 'KOI SME NIE' or \
            message.content == 'КОИ СМЕ НИЕ':

        await message.channel.send('''НИЕ СМЕ ЗЕЛЕНАТА АГИТКА
ПОБЪРКАНИ ПИЯНИ ФЕНОВЕ
ЗЕЛЕНО ЗНАМЕ ЩЕ СЕ ВЕЕ
ЩЕ ПЕЕМ НИЙ ЗА ЧЕРНОТО МОРЕ
КОГАТО ХВАНАХМЕ ПЛЕБЕЯ
ЗАВЪРЗАХМЕ ГО НИЕ СЪС ВЪЖЕ
ОСТАВИХМЕ ДА СТОИ НА ТЯСНО
И ПРАВИХМЕ СЪС НЕГО КВО ЛИ НЕ
ЕБАХМЕ ГО ВЪВ ДУПЕТО МУ МАЗНО
ОПРЪСКАХМЕ ЛИЦЕТО МУ СЪС КАЛ
ИЗПРАЗНИХМЕ МУ СЕ В УСТАТА
НА ВСИЧКИ ТОЙ НАПРАВИ НИ КАВАЛ
И НЕКА ВСЕКИ ПО СВЕТА ДА ЗНАЕ
ЧЕ ЧЕРНО МОРЕ ЩЕ Е ШАМПИОН
ЧЕ ДРУГИ НЯМА НИЙ ДА ТРАЕМ
ЩЕ ВЛАСТВА ВСЕ ЗЕЛЕНИЯ ТЕРОР''')

    if message.content == 'и ловец съм':
        await message.channel.send('и рибаp съм')
    if message.content == 'time':
        now = datetime.datetime.now()
        realtime = now.strftime('%H:%M')
        await message.channel.send(f"Часът е {realtime}.")
    if message.content == 'weather':
        api_url = f'https://api.open-meteo.com/v1/forecast?latitude=42.70&longitude=23.32&current_weather=true' \
                  f'&timezone=Europe%2FMoscow'
        response = requests.get(api_url)
        data = response.json()
        if 'current_weather' in data:
            temperature = data['current_weather']['temperature']
            await message.channel.send(f"В момента е {temperature}°C навън")
        else:
            await message.channel.send('Sorry, I could not retrieve the weather data.')
    for word in offensive_words:
        if word in message.content.lower():
            await message.delete()
            await message.channel.send(f"{message.author.mention}, не обиждай ")
            return
    await client.process_commands(message)


client.run(TOKEN)
