import asyncio
import aiohttp
import discord
from discord.ext import commands, tasks
import random
import requests
import logging
import json
import os
from dotenv import load_dotenv
from typing import List, Dict, Optional

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

IMGUR_CLIENT_ID = os.getenv('IMGUR_CLIENT_ID')
API_NINJAS_KEY = os.getenv('API_NINJAS_KEY')
BOT_TOKEN = os.getenv('BOT_TOKEN')

WELCOME_CHANNEL_ID = None
GOODBYE_CHANNEL_ID = None
FEEDBACK_CHANNEL_ID = None

headers = {'Authorization': f'Client-ID {IMGUR_CLIENT_ID}'}

DATA_FILE = 'bot_data.json'

def load_data() -> Dict:
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'user_memes': {}, 'votes': {}}

def save_data(data: Dict) -> None:
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

data = load_data()
user_memes = data.get('user_memes', {})
votes = data.get('votes', {})
announcement_channel_id = None

facts = [
    "**Melting glaciers are causing sea levels to rise.**",
    "**The average global temperature has increased by 1.2°C over the past 100 years.**",
    "**The Amazon Rainforest produces 20% of the world's oxygen.**",
    "**The 20 hottest years on record have occurred in the last 22 years.**",
    "**Global warming could cause sea levels to rise by 1 meter by the year 2100.**",
    "**Carbon dioxide (CO2) levels are at their highest in the past 800,000 years.**",
    "**Arctic sea ice has decreased by 40% over the past 30 years.**",
    "**Climate change could lead to the loss of 70-90% of coral reefs.**",
    "**80% of global energy consumption is derived from fossil fuels.**",
    "**Food production accounts for 25% of global greenhouse gas emissions.**",
    "**Climate change is causing ocean acidification, threatening marine life.**",
    "**Water sources are depleting in many parts of the world, and droughts are becoming more common.**",
    "**Rising global temperatures are causing extreme weather events to become more frequent and intense.**",
    "**High temperatures negatively impact food production, increasing the risk of famine.**",
    "**Rapid urbanization and deforestation threaten biodiversity and disrupt ecosystems.**",
    "**Rising sea levels are threatening communities living in coastal areas.**",
    "**Global greenhouse gas emissions are leading to worldwide health problems and diseases.**",
    "**Melting glaciers in terrestrial areas are causing sea levels to rise and freshwater sources to dwindle.**",
    "**Deforestation is increasing carbon dioxide emissions and destroying natural habitats.**",
    "**Changes in ocean currents are affecting global climate patterns, altering weather conditions.**",
    "**Methane levels in the atmosphere have significantly increased in recent years.**",
    "**Climate change is leading to the loss of habitats for animals and plants.**",
    "**Rising sea levels pose an existential threat to small island nations.**",
    "**Desertification is leading to a decrease in agricultural land worldwide.**",
    "**Oceans continue to warm as they absorb heat from human activities.**",
    "**30% of the world's forests have been lost in the past 100 years.**",
    "**Global warming is altering the migration patterns of animal species.**",
    "**High temperatures are causing an increase in the number and severity of wildfires.**",
    "**Warming seas are leading to a decline in fish stocks and changes in marine life.**",
    "**Climate change is making life even harder in impoverished regions.**"
]

categories = {
    'funny': [],
    'political': [],
    'animal': [],
    'sports': [],
    'tech': [],
    'music': [],
    'movies': [],
    'gaming': [],
    'random': [],
    'science': [],
    'history': [],
    'food': [],
    'travel': [],
    'art': [],
    'fashion': [],
    'memes': [],
    'health': [],
    'education': [],
    'nature': [],
    'news': [],
    'literature': [],
    'automotive': [],
    'space': [],
    'business': [],
    'comics': [],
    'philosophy': [],
    'celebrity': [],
    'psychology': []
}

last_ccmeme_time = 0

async def fetch_memes(url: str) -> List[str]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                logger.info(f"Fetching memes from {url}")
                response.raise_for_status()
                data = await response.json()
                if 'data' in data:
                    memes = [item['link'] for item in data['data'] if 'link' in item]
                    return memes if memes else []
                else:
                    logger.warning("Invalid response format, 'data' key not found.")
                    return []
        except aiohttp.ClientResponseError as e:
            logger.error(f'HTTP error occurred: {e.status} - {e.message}')
            return []
        except Exception as e:
            logger.error(f'An unexpected error occurred: {e}')
            return []

async def get_climate_change_memes() -> List[str]:
    urls = [
        'https://api.imgur.com/3/gallery/r/climatechange/hot',
        'https://api.imgur.com/3/gallery/r/climate/hot',
        'https://api.imgur.com/3/gallery/r/world/hot',
        'https://api.imgur.com/3/gallery/r/environment/hot',
        'https://api.imgur.com/3/gallery/r/sustainability/hot',
        'https://api.imgur.com/3/gallery/r/ClimateActionPlan/hot',
        'https://api.imgur.com/3/gallery/r/EcoFriendly/hot',
        'https://api.imgur.com/3/gallery/r/globalwarming/hot',
        'https://api.imgur.com/3/gallery/r/global/hot',
        'https://api.imgur.com/3/gallery/r/change/hot'
    ]
    
    all_memes = []
    for url in urls:
        memes = await fetch_memes(url)
        all_memes.extend(memes)

    return all_memes

async def get_ip_info(ip_addr: str) -> str:
    url = f'https://api.api-ninjas.com/v1/iplookup?address={ip_addr}'
    headers = {'X-Api-Key': API_NINJAS_KEY}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return (
                    f"🌍 **IP Address:** {data.get('ip')}\n"
                    f"🏳️ **Country-Code:** {data.get('country_code')}\n"
                    f"🇺🇸 **Country:** {data.get('country')}\n"
                    f"📍 **Region-Code:** {data.get('region_code')}\n"
                    f"📍 **Region:** {data.get('region')}\n"
                    f"🕒 **Timezone:** {data.get('timezone')}\n"
                )
            else:
                return f"❗ Error: {response.status} - {response.reason}"

@bot.command(name='ip')
async def ip_lookup(ctx: commands.Context, ip_addr: str):
    result = await get_ip_info(ip_addr)
    await ctx.send(f"🔍 **IP Lookup Result:**\n{result}")

async def generate_password(length: int) -> str:
    url = f'https://api.api-ninjas.com/v1/passwordgenerator?length={length}'
    headers = {'X-Api-Key': API_NINJAS_KEY}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('random_password', 'No password generated.')
            else:
                return f"❗ Error: {response.status} - {response.reason}"

@bot.command(name='password')
async def password_generator(ctx: commands.Context, length: int):
    if length < 1 or length > 128:
        await ctx.send("❗ Please enter a length between 1 and 128.")
        return

    password = await generate_password(length)
    await ctx.send(f"🔑 **Generated Password:** `{password}`")

# Function to fetch hobbies asynchronously
async def fetch_hobbies(url: str) -> Dict[str, Optional[str]]:
    headers = {'X-Api-Key': API_NINJAS_KEY}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                if isinstance(data, dict):  # Check if the response is a dictionary
                    return data
                else:
                    logger.warning("Unexpected response format.")
                    return {}
            else:
                logger.error(f"Failed to fetch data. Status code: {response.status}")
                return {}
            
async def get_hobby() -> Dict[str, str]:
    url = "https://api.api-ninjas.com/v1/hobbies?category=general"
    data = await fetch_hobbies(url)
    
    # Assuming the API response includes these fields
    hobby = data.get('hobby', 'No hobby found')
    category = data.get('category', 'No category found')
    link = data.get('link', 'No link available')
    
    return {
        'hobby': hobby,
        'category': category,
        'link': link
    }

# Command to fetch and display a hobby
@bot.command(name='hobby')
async def hobby(ctx: commands.Context):
    hobby_info = await get_hobby()
    hobby = hobby_info.get('hobby', 'No hobby found')
    category = hobby_info.get('category', 'No category found')
    link = hobby_info.get('link', 'No link available')

    response = (
        f"🎨 **Here's a hobby you might enjoy:** {hobby}\n"
        f"📂 **Category:** {category}\n"
        f"🔗 **Learn more:** {link}"
    )
    await ctx.send(response)

async def get_random_facts() -> List[str]:
    url = 'https://api.api-ninjas.com/v1/facts'
    headers = {'X-Api-Key': API_NINJAS_KEY}
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                logger.info(f"Response Status Code: {response.status}")
                response_text = await response.text()
                logger.info(f"Response Text: {response_text}")

                if response.status == 200:
                    try:
                        data = await response.json()
                        if isinstance(data, list):
                            return [fact['fact'] for fact in data if 'fact' in fact][:3]  # Fixed number of facts
                        else:
                            logger.warning("Unexpected response format, data is not a list.")
                            return []
                    except json.JSONDecodeError as e:
                        logger.error(f"JSON Decode Error: {e}")
                        return []
                else:
                    logger.error(f"API Error: {response.status} - {response.reason}")
                    return []
        except aiohttp.ClientResponseError as e:
            logger.error(f'HTTP error occurred: {e.status} - {e.message}')
            return []
        except Exception as e:
            logger.error(f'An unexpected error occurred: {e}')
            return []

@bot.command(name='fact')
@commands.cooldown(1, 5, commands.BucketType.user)
async def fact(ctx: commands.Context, limit: int = 3):
    if limit < 1 or limit > 10:
        await ctx.send("❗ Please enter a limit between 1 and 10.")
        return

    facts = await get_random_facts()
    if facts:
        # Apply the limit here by slicing the facts list
        for fact in facts[:limit]:
            await ctx.send(f"📚 **Fact:** {fact}")
    else:
        await ctx.send("❗ Sorry, I couldn't retrieve any facts right now.")

@bot.event
async def on_ready():
    logger.info(f'✅ Logged in as {bot.user}')
    logger.info('Bot is ready and running!')
    announce_top_meme.start()

@bot.command(help="Say hello to the bot.")
async def hi(ctx):
    await ctx.send(f'👋 **Hello!**')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if any(bad_word in message.content.lower() for bad_word in ['stfu', 'fuck', 'shit', 'bitch', 'nigga', 'nigger', 'ass', 'mtf']):
        await message.delete()
        await message.channel.send(f"🚫 {message.author.mention}, that word is not allowed here.")

    await bot.process_commands(message)

@bot.command(name='feedback')
async def feedback(ctx: commands.Context, *, feedback_message: str):
    feedback_channel = bot.get_channel(int(FEEDBACK_CHANNEL_ID)) if FEEDBACK_CHANNEL_ID else None
    if feedback_channel:
        await feedback_channel.send(f"💬 **Feedback from {ctx.author}:** {feedback_message}")
        await ctx.send("✅ **Thank you for your feedback!**")
    else:
        await ctx.send("❗ **Feedback channel is not set. Please ask an admin to set it using `!feedback` command.**")

@bot.command(name='mystats')
async def my_stats(ctx: commands.Context):
    user_id = str(ctx.author.id)
    num_memes = len(user_memes.get(user_id, []))
    num_votes = votes.get(user_id, 0)
    await ctx.send(f"📊 **You have submitted {num_memes} memes and received {num_votes} votes.")

@bot.command(name='meme')
@commands.cooldown(1, 5, commands.BucketType.user)
async def meme(ctx: commands.Context, category: str = None):
    if category and category in categories:
        meme_list = categories[category] + [meme for user_memes in user_memes.values() for meme in user_memes]
    else:
        meme_list = [meme for category_list in categories.values() for meme in category_list] + [meme for user_memes in user_memes.values() for meme in user_memes]
    
    if meme_list:
        meme = random.choice(meme_list)
        await ctx.send(f"🤣 **Random Meme:** {meme}")
    else:
        await ctx.send("❗ There are no memes in this category.")

@bot.command(name='addmeme')
@commands.cooldown(1, 10, commands.BucketType.user)
async def add_meme(ctx: commands.Context, *, meme_url: str):
    user_id = str(ctx.author.id)
    if user_id not in user_memes:
        user_memes[user_id] = []
    user_memes[user_id].append(meme_url)
    save_data({'user_memes': user_memes, 'votes': votes})
    await ctx.send(f"✅ **Added your meme to the collection:** {meme_url}")

@bot.command(name='submitmeme')
@commands.cooldown(1, 10, commands.BucketType.user)
async def submit_meme(ctx: commands.Context, *, meme_url: str):
    user_id = ctx.author.id
    if meme_url.startswith('http'):
        if user_id not in user_memes:
            user_memes[user_id] = []
        user_memes[user_id].append(meme_url)
        save_data({'user_memes': user_memes, 'votes': votes})
        await ctx.send("✅ **Your meme has been submitted for voting!**")
    else:
        await ctx.send("❗ Please submit a valid URL.")

@bot.command(name='my_memes')
async def my_memes(ctx: commands.Context):
    user_id = ctx.author.id
    if user_id in user_memes and user_memes[user_id]:
        memes_list = '\n'.join(user_memes[user_id])
        await ctx.send(f"📸 **Memes you sent:**\n{memes_list}")
    else:
        await ctx.send("❗ There are no memes submitted yet.")

@bot.command(name='memevote')
@commands.cooldown(1, 10, commands.BucketType.user)
async def meme_vote(ctx: commands.Context, user_id: int, vote: int):
    user_id_str = str(user_id)
    if user_id_str in user_memes:
        if user_id_str not in votes:
            votes[user_id_str] = 0
        votes[user_id_str] += vote
        save_data({'user_memes': user_memes, 'votes': votes})
        await ctx.send(f"👍 **Your vote for user {user_id} has been counted.**")
    else:
        await ctx.send(f"❗ **User {user_id} has no memes.**")

@bot.command(name='topmeme')
async def top_meme(ctx: commands.Context):
    if votes:
        top_user = max(votes.items(), key=votes.get)[0]
        top_meme_url = random.choice(user_memes[top_user])
        await ctx.send(f"🏆 **Top Meme:** {top_meme_url} with {votes[top_user]} votes!")
    else:
        await ctx.send("❗ **No memes have been voted on yet.**")

@bot.command(name='ClimateChange')
async def climate_change(ctx: commands.Context):
    fact = random.choice(facts)
    await ctx.send(f"🌍 **Did you know that?** {fact}")

@bot.command(name='bot_help')
async def bot_help(ctx: commands.Context):
    help_text = """
    **Available Commands:**

    👋 **!hi** - Say hello to the bot.
    🤣 **!meme [category]** - Get a random meme. Optionally specify a category to filter.
    📝 **!addmeme <meme-url>** - Add a meme to the bot's collection.
    🗳️ **!submitmeme <meme-url>** - Submit a meme for voting.
    📸 **!my_memes** - View the memes you've submitted.
    👍 **!memevote <user-id> <vote>** - Vote for a user's meme. The vote should be a positive or negative integer.
    🏆 **!topmeme** - View the most voted meme.
    🌍 **!ClimateChange** - Get a random climate change fact.
    🔍 **!searchmm <keyword>** - Search for memes on Imgur by keyword.
    🔑 **!password <length>** - Generate a random password with the specified length (1-128).
    🎨 **!hobby [category]** - Get a random hobby suggestion. Optionally specify a category.
    🌍 **!ip <ip-address>** - Look up information about an IP address.
    🖼️ **!CCMeme** - Get a random climate change meme from Imgur.
    📚 **!fact [limit]** - Get random facts. Specify the number of facts (1-10).
    🌦️ **!weather <location>** - Get the current weather for a specified location.
    🧠 **!trivia [category]** - Get a random trivia question. Optionally specify a category.
    🔄 **!resetvotes** - Reset all meme votes (admin only).
    🔄 **!resetdata** - Reset all user data and votes (admin only).
    📢 **!setannouncementchannel** - Set the channel for meme announcements (admin only).
    👋 **!welcome** - Set the welcome channel (admin only).
    👋 **!goodbye** - Set the goodbye channel (admin only).
    💬 **!setfeedback** - Set the feedback channel (admin only).
    🏆 **!leaderboard** - Show the top 5 users with the most votes.
    ❓ **!bot_help** - Show this help message. 
    """
    await ctx.send(help_text)

@bot.command(name='helpbot')
async def helpbot(ctx: commands.Context):
    help_text = """
    **Available Commands:**

    👋 **!hi** - Say hello to the bot.
    🤣 **!meme [category]** - Get a random meme. Optionally specify a category to filter.
    📝 **!addmeme <meme-url>** - Add a meme to the bot's collection.
    🗳️ **!submitmeme <meme-url>** - Submit a meme for voting.
    📸 **!my_memes** - View the memes you've submitted.
    👍 **!memevote <user-id> <vote>** - Vote for a user's meme. The vote should be a positive or negative integer.
    🏆 **!topmeme** - View the most voted meme.
    🌍 **!ClimateChange** - Get a random climate change fact.
    🔍 **!searchmm <keyword>** - Search for memes on Imgur by keyword.
    🔑 **!password <length>** - Generate a random password with the specified length (1-128).
    🎨 **!hobby [category]** - Get a random hobby suggestion. Optionally specify a category.
    🌍 **!ip <ip-address>** - Look up information about an IP address.
    🖼️ **!CCMeme** - Get a random climate change meme from Imgur.
    📚 **!fact [limit]** - Get random facts. Specify the number of facts (1-10).
    🌦️ **!weather <location>** - Get the current weather for a specified location.
    🧠 **!trivia [category]** - Get a random trivia question. Optionally specify a category.
    🔄 **!resetvotes** - Reset all meme votes (admin only).
    🔄 **!resetdata** - Reset all user data and votes (admin only).
    📢 **!setannouncementchannel** - Set the channel for meme announcements (admin only).
    👋 **!welcome** - Set the welcome channel (admin only).
    👋 **!goodbye** - Set the goodbye channel (admin only).
    💬 **!setfeedback** - Set the feedback channel (admin only).
    🏆 **!leaderboard** - Show the top 5 users with the most votes.
    ❓ **!bot_help** - Show this help message.
    """
    await ctx.send(help_text)

@bot.command(name='CCMeme')
@commands.cooldown(1, 5, commands.BucketType.user)
async def ccmeme(ctx: commands.Context):
    memes = await get_climate_change_memes()
    if memes:
        meme_url = random.choice(memes)
        await ctx.send(f"🌍 **A meme about climate change:** {meme_url}")
    else:
        await ctx.send("❗ There was an error retrieving climate change memes or no memes were found.")

def get_weather(city: str) -> str:
    api_key = os.getenv('WEATHER_API_KEY')
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return (f"🌡️ **Weather in {city}:**\n"
                f"Temperature: {data['current']['temp_c']}°C\n"
                f"Condition: {data['current']['condition']['text']}")
    except requests.RequestException as e:
        return f"❗ An error occurred while receiving weather data: {e}"

@bot.command(name='weather')
async def weather(ctx: commands.Context, *, city: str):
    weather_info = get_weather(city)
    await ctx.send(weather_info)

@bot.command(name='trivia')
async def trivia(ctx: commands.Context):
    trivia_data = {
        "What is the capital of France? 🇫🇷": "Paris",
        "What is the largest planet in our solar system? 🌌": "Jupiter",
        "Who wrote 'To Kill a Mockingbird'? 📚": "Harper Lee",
        "What is the chemical symbol for gold? 🏅": "Au",
        "In what year did the Titanic sink? 🚢": "1912",
        "What is the hardest natural substance on Earth? 💎": "Diamond",
        "Who painted the Mona Lisa? 🎨": "Leonardo da Vinci",
        "What is the smallest country in the world? 🌍": "Vatican City",
        "What element does 'O' represent on the periodic table? 🧪": "Oxygen",
        "What planet is known as the Red Planet? 🔴": "Mars",
        "Who is known as the father of modern physics? 👨‍🔬": "Albert Einstein",
        "Which ocean is the largest? 🌊": "Pacific Ocean",
        "What is the tallest mountain in the world? ⛰️": "Mount Everest",
        "In which city would you find the Colosseum? 🏛️": "Rome",
        "What year did World War II end? 🌍": "1945",
        "Which planet is closest to the Sun? ☀️": "Mercury",
        "Who wrote '1984'? 📖": "George Orwell",
        "What is the capital of Japan? 🇯🇵": "Tokyo",
        "How many continents are there on Earth? 🌎": "Seven",
        "What is the largest mammal in the world? 🐋": "Blue Whale",
        "Who was the first person to walk on the moon? 🌕": "Neil Armstrong",
        "What is the currency of the United Kingdom? 💷": "Pound Sterling",
        "What is the name of the longest river in the world? 🌊": "Nile",
        "Who developed the theory of relativity? 🧠": "Albert Einstein",
        "What is the chemical symbol for water? 💧": "H2O",
        "What is the main ingredient in guacamole? 🥑": "Avocado",
        "Which country is known as the Land of the Rising Sun? 🌅": "Japan",
        "Who painted 'Starry Night'? 🌟": "Vincent van Gogh",
        "What is the most abundant gas in Earth's atmosphere? 🌬️": "Nitrogen",
        "What is the smallest planet in our solar system? 🪐": "Mercury",
        "Who discovered penicillin? 💉": "Alexander Fleming",
        "What is the name of the galaxy that contains our solar system? 🌌": "Milky Way",
        "What is the capital city of Australia? 🐨": "Canberra",
        "What is the symbol for potassium on the periodic table? 🧪": "K",
        "What is the name of the phobia that involves an intense fear of spiders? 🕷️": "Arachnophobia",
        "Which element is represented by the symbol 'Fe'? 🧪": "Iron",
        "What fruit is known as the 'king of fruits' and has a strong odor? 🍍": "Durian",
        "What is the chemical formula for table salt? 🧂": "NaCl",
        "What is the name of the famous clock tower in London? ⏰": "Big Ben",
        "What is the hardest natural substance found in the human body? 💪": "Tooth enamel",
        "Who invented the light bulb? 💡": "Thomas Edison"
    }

    # Choose a random question
    question, correct_answer = random.choice(list(trivia_data.items()))
    
    # Ask the question
    await ctx.send(f"**📝 Question:** {question}\nReply with your answer!")

    # Wait for the user's response
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', timeout=30.0, check=check)
        user_answer = msg.content.strip()
        
        if user_answer.lower() == correct_answer.lower():
            await ctx.send(f"**✅ Correct!** The answer to \"{question}\" is indeed {correct_answer}.")
        else:
            await ctx.send(f"**❌ Wrong!** The correct answer to \"{question}\" is {correct_answer}.")
    
    except asyncio.TimeoutError:
        await ctx.send("**⏳ Time's up!** You took too long to answer.")

@bot.command(name='searchmm')
@commands.cooldown(1, 5, commands.BucketType.user)
async def searchmm(ctx: commands.Context, *, keyword: str):
    url = f'https://api.imgur.com/3/gallery/search?q={keyword}'
    memes = await fetch_memes(url)
    if memes:
        meme_url = random.choice(memes)
        await ctx.send(f"🔍 **Here's a random meme for you to search:** {meme_url}")
    else:
        await ctx.send(f"❗ No memes found for '{keyword}'.")

@tasks.loop(hours=24)
async def announce_top_meme():
    if announcement_channel_id:
        channel = bot.get_channel(announcement_channel_id)
        if channel:
            top_user = max(votes.items(), key=lambda item: item[1], default=(None, 0))[0]
            if top_user and top_user in user_memes:
                top_meme = random.choice(user_memes[top_user])
                await channel.send(f"🏆 **Top meme of the hour by user {top_user}:** {top_meme}")
            else:
                await channel.send("❗ No memes to announce.")
        else:
            logger.warning("📢 Announcement channel not found.")

@bot.command(name='setannouncementchannel')
@commands.has_permissions(administrator=True)
async def set_announcement_channel(ctx: commands.Context):
    global announcement_channel_id
    announcement_channel_id = ctx.channel.id
    await ctx.send(f"📢 **Announcement channel set to {ctx.channel.name}**")

@bot.command(name='welcome')
@commands.has_permissions(administrator=True)
async def set_welcome_channel(ctx: commands.Context):
    global WELCOME_CHANNEL_ID
    WELCOME_CHANNEL_ID = ctx.channel.id
    await ctx.send(f"👋 **Welcome channel set to {ctx.channel.name}**")

@bot.command(name='goodbye')
@commands.has_permissions(administrator=True)
async def set_goodbye_channel(ctx: commands.Context):
    global GOODBYE_CHANNEL_ID
    GOODBYE_CHANNEL_ID = ctx.channel.id
    await ctx.send(f"👋 **Goodbye channel set to {ctx.channel.name}**")

@bot.command(name='setfeedback')
@commands.has_permissions(administrator=True)
async def set_feedback(ctx: commands.Context):
    global FEEDBACK_CHANNEL_ID
    FEEDBACK_CHANNEL_ID = ctx.channel.id
    await ctx.send(f"💬 **Feedback channel set to {ctx.channel.name}**")

@bot.command(name='resetvotes')
@commands.has_permissions(administrator=True)
async def reset_votes(ctx: commands.Context):
    global votes
    votes = {}
    save_data({'user_memes': user_memes, 'votes': votes})
    await ctx.send("🔄 **Votes have been reset.**")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ This command is on cooldown. Please try again in {error.retry_after:.2f} seconds.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❗ Missing required argument. Please check the command and try again.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❗ Invalid argument provided. Please check the command and try again.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("❗ Command not found. Use !bot_help to see a list of available commands.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("❗ You do not have permission to use this command.")
    else:
        await ctx.send(f"❗ An unexpected error occurred: {str(error)}")
        logger.error(f"Unhandled error: {error}")

@bot.command(name='leaderboard')
async def leaderboard(ctx: commands.Context):
    sorted_votes = sorted(votes.items(), key=lambda item: item[1], reverse=True)
    leaderboard = "\n".join([f"{user}: {vote} votes" for user, vote in sorted_votes[:5]])
    await ctx.send(f"🏆 **Meme Leaderboard** 🏆\n{leaderboard}")

@bot.event
async def on_member_join(member):
    welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if welcome_channel:
        await welcome_channel.send(f"👋 **Welcome {member.mention} to our server!**")
    else:
        logger.warning("👋 Welcome channel is not set.")

@bot.event
async def on_member_remove(member):
    goodbye_channel = bot.get_channel(GOODBYE_CHANNEL_ID)
    if goodbye_channel:
        await goodbye_channel.send(f"👋 **Goodbye {member.mention}, we'll miss you!**")
    else:
        logger.warning("👋 Goodbye channel is not set.")

@bot.command(name='resetdata')
@commands.has_permissions(administrator=True)
async def reset_data(ctx: commands.Context):
    global user_memes, votes
    user_memes = {}
    votes = {}
    save_data({'user_memes': user_memes, 'votes': votes})
    await ctx.send("🔄 **All user data has been reset.**")

if __name__ == '__main__':
    bot.run('')
