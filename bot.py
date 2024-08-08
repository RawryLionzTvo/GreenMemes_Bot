import discord
from discord.ext import commands, tasks
import random
import aiohttp
import asyncio
import logging
import json
from typing import List, Dict
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

IMGUR_CLIENT_ID = ''
API_NINJAS_KEY = ''  # Replace with your actual API key
headers = {'Authorization': f'Client-ID {IMGUR_CLIENT_ID}'}

# Persistent storage
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

# Ensure each category has a default list of memes
for category in categories:
    if not categories[category]:
        categories[category] = []

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
        if memes:
            logger.info(f"Memes found at {url}: {memes}")
            all_memes.extend(memes)
        else:
            logger.info(f"No memes found at {url}")
    return all_memes if all_memes else []

memes = asyncio.run(get_climate_change_memes())

async def get_ip_info(ip_addr: str) -> str:
    """Fetch IP information using the Ninja API."""
    url = f'https://api.api-ninjas.com/v1/iplookup?address={ip_addr}'
    headers = {'X-Api-Key': API_NINJAS_KEY}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                # Format the response data nicely
                location_info = (
                    f"IP Address: {data.get('ip')}\n"
                    f"Country-Code: {data.get('country_code')}\n"
                    f"Country: {data.get('country')}\n"
                    f"Region-Code: {data.get('region_code')}\n"
                    f"Region: {data.get('region')}\n"
                    f"Timezone: {data.get('timezone')}\n"
                )
                return location_info
            else:
                return f"Error: {response.status} - {response.reason}"

@bot.command(name='ip')
async def ip_lookup(ctx: commands.Context, ip_addr: str):
    """Looks up geographic and network info for a given IP address."""
    result = await get_ip_info(ip_addr)
    await ctx.send(f"IP Lookup Result:\n{result}")

async def generate_password(length: int) -> str:
    """Generates a password of the specified length using the Ninja API."""
    url = f'https://api.api-ninjas.com/v1/passwordgenerator?length={length}'
    headers = {'X-Api-Key': API_NINJAS_KEY}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('random_password', 'No password generated.')
            else:
                return f"Error: {response.status} - {response.reason}"

@bot.command(name='password')
async def password_generator(ctx: commands.Context, length: int):
    """Generates a password of the specified length using the Ninja API."""
    if length < 1 or length > 128:  # Validate length
        await ctx.send("Please enter a length between 1 and 128.")
        return

    password = await generate_password(length)
    await ctx.send(f"Generated Password: `{password}`")

async def get_hobby(category: str = 'general') -> str:
    """Fetches a random hobby from the Ninja API."""
    url = f'https://api.api-ninjas.com/v1/hobbies?category={category}'
    headers = {'X-Api-Key': API_NINJAS_KEY}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                if data:
                    hobby = random.choice(data).get('hobby', 'No hobby found.')
                    return hobby
                else:
                    return "No hobbies found."
            else:
                return f"Error: {response.status} - {response.reason}"

@bot.command(name='hobby')
async def hobby(ctx: commands.Context, category: str = 'general'):
    """Fetches a random hobby from the Ninja API."""
    hobby = await get_hobby(category)
    await ctx.send(f"Here's a hobby you might enjoy: {hobby}")

async def get_random_facts(limit: int = 3) -> List[str]:
    """Fetch random facts using the Ninja API."""
    url = f'https://api.api-ninjas.com/v1/facts?limit={limit}'
    headers = {'X-Api-Key': API_NINJAS_KEY}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return [fact['fact'] for fact in data]
            else:
                logger.error(f"Error fetching facts: {response.status} - {response.reason}")
                return []
            
@bot.command(name='fact')
@commands.cooldown(1, 5, commands.BucketType.user)
async def fact(ctx: commands.Context, limit: int = 3):
    """Fetches random facts using the Ninja API and sends them to the channel."""
    if limit < 1 or limit > 10:  # Validate limit
        await ctx.send("Please enter a limit between 1 and 10.")
        return

    facts = await get_random_facts(limit)
    if facts:
        for fact in facts:
            await ctx.send(f"📚 **Fact**: {fact}")
    else:
        await ctx.send("Sorry, I couldn't retrieve any facts right now.")

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user}')
    announce_top_meme.start()

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def hi(ctx):
    await ctx.send(f'Hello!')

@bot.command(name='meme')
@commands.cooldown(1, 5, commands.BucketType.user)
async def meme(ctx: commands.Context, category: str = None):
    if category and category in categories:
        meme_list = categories[category] + [meme for user_memes in user_memes.values() for meme in user_memes]
    else:
        meme_list = memes + [meme for user_memes in user_memes.values() for meme in user_memes]
    
    if meme_list:
        meme = random.choice(meme_list)
        await ctx.send(meme)
    else:
        await ctx.send("There are no memes in this category.")

@bot.command(name='addmeme')
@commands.cooldown(1, 10, commands.BucketType.user)
async def add_meme(ctx: commands.Context, category: str, *, meme_url: str):
    if category in categories:
        if meme_url.startswith('http'):
            categories[category].append(meme_url)
            await ctx.send(f"{category} Meme added to category!")
        else:
            await ctx.send("Please submit a valid URL.")
    else:
        await ctx.send("Invalid category.")

@bot.command(name='submitmeme')
@commands.cooldown(1, 10, commands.BucketType.user)
async def submit_meme(ctx: commands.Context, *, meme_url: str):
    user_id = ctx.author.id
    if meme_url.startswith('http'):
        if user_id not in user_memes:
            user_memes[user_id] = []
        user_memes[user_id].append(meme_url)
        votes[meme_url] = 0
        save_data({'user_memes': user_memes, 'votes': votes})
        await ctx.send("Meme submitted and put to vote!")
    else:
        await ctx.send("Please submit a valid URL.")

@bot.command(name='my_memes')
async def my_memes(ctx: commands.Context):
    user_id = ctx.author.id
    if user_id in user_memes and user_memes[user_id]:
        memes_list = '\n'.join(user_memes[user_id])
        await ctx.send(f"Memes you sent:\n{memes_list}")
    else:
        await ctx.send("There are no memes submitted yet.")

@bot.command(name='vote')
async def vote(ctx: commands.Context, meme: str):
    try:
        meme_id = int(meme)
        user_memes_list = [m for user_memes in user_memes.values() for m in user_memes]
        if 0 <= meme_id < len(user_memes_list):
            meme_url = user_memes_list[meme_id]
            votes[meme_url] += 1
            save_data({'user_memes': user_memes, 'votes': votes})
            await ctx.send(f"Meme {meme_id} You voted for!")
        else:
            await ctx.send("Invalid meme ID.")
    except ValueError:
        await ctx.send("Invalid format: Please enter a meme ID.")

@bot.command(name='topmeme')
async def top_meme(ctx: commands.Context):
    if votes:
        top_meme_url = max(votes, key=votes.get)
        await ctx.send(f"Top rated meme of the week: {top_meme_url}")
    else:
        await ctx.send("No memes have been voted yet.")

@bot.command(name='ClimateChange')
async def climate_change(ctx: commands.Context):
    fact = random.choice(facts)
    await ctx.send(f"Did you know that? {fact}")

@bot.command(name='helpbot')
async def helpbot(ctx: commands.Context):
    help_text = """
    **Available Commands:**

    **!hi**
    - **Want to say hi?**

    **!meme [category]**
    - **Description**: Shares a random meme. If a specific category is specified, memes from that category will be shared. If the category is not specified, it includes both the memes that the bot has predetermined and the memes submitted by users.
    - **Example Usage**: !meme or !meme funny

    **!addmeme <category> <meme-url>**
    - **Description**: Adds a new meme to a category. The category should be predefined, like funny, political, or animal. The URL must be valid and accessible.
    - **Usage**: The <category> parameter specifies the category to which the meme will be added. The <meme-url> parameter is the URL of the meme you want to add.
    - **Example Usage**: !addmeme funny https://example.com/my-funny-meme.jpg

    **!submitmeme <meme-url>**
    - **Description**: Allows users to submit their own memes. Submitted memes are included in the voting system.
    - **Usage**: The <meme-url> parameter is the URL of the meme you want to submit. The URL must be valid and accessible.
    - **Example Usage**: !submitmeme https://example.com/my-meme.jpg

    **!my_memes**
    - **Description**: Lists the memes submitted by the user. If no memes have been submitted by the user, it sends an appropriate message.
    - **Usage**: Shows the user the memes they have submitted.
    - **Example Usage**: !my_memes

    **!vote <meme-id>**
    - **Description**: Allows you to vote for a specific meme. The meme-id is the index number of the meme in the list of user-submitted memes.
    - **Usage**: The <meme-id> parameter specifies the number of the meme you want to vote for.
    - **Example Usage**: !vote 2 (This votes for the third meme on the list.)

    **!topmeme**
    - **Description**: Shows the most voted meme of the week. This information is updated weekly and sent to the designated announcement channel.
    - **Example Usage**: !topmeme

    **!ClimateChange**
    - **Description**: Shares a random fact about the environment and climate change. The fact is selected from a list of factors predetermined by the bot.
    - **Example Usage**: !ClimateChange (Provides a random environmental fact each time it's run.)

    **!searchmm <keyword>**
    - **Description**: Searches for memes on Imgur based on the specified keyword and shares a random one from the results.
    - **Usage**: The <keyword> parameter specifies the keyword you want to search for.
    - **Example Usage**: !searchmm cat (This searches for a meme related to the keyword 'cat' and shares a random one.)

    **!hobby [category]**
    - **Description**: Fetches a random hobby from the Ninja API. The category is optional and defaults to 'general'.
    - **Example Usage**: !hobby or !hobby outdoor

    **!helpbot**
    - **Description**: Provides a detailed list of all available commands and functions of the bot.
    - **Example Usage**: !helpbot

    **!setchannel <channel>**
    - **Description**: Sets the channel where the most voted meme of the week will be announced. The <channel> parameter specifies the name or ID of the announcement channel.
    - **Usage**: To set the announcement channel, specify an appropriate channel where the bot can share announcements.
    - **Example Usage**: !setchannel #announcements (This sets the #announcements channel as the announcement channel.)

    **!CCMeme**
    - **Description**: Shares a random meme about climate change. The command can be used once every 5 seconds. If the command is used again within 5 seconds, the bot informs the user how long they need to wait.
    - **Usage**: When you run the command, the bot shares a random meme about climate change from Imgur.
    - **Example Usage**: !CCMeme (You can run the command every 5 seconds.)

    **!password <length>**
    - **Description**: Generates a random password of the specified length using the Ninja API.
    - **Usage**: The <length> parameter specifies the length of the password.
    - **Example Usage**: !password 16 (This generates a 16-character password.)

    **Notes:**
    - For the !submitmeme command, make sure the submitted URL is in the correct format and accessible.
    - In the !vote command, the meme-id must correctly refer to the ID in the list of user-submitted memes.
    - Ensure that the announcement channel is correctly set using the !setchannel command.
    - The !CCMeme command can be run every 5 seconds; if used within that time frame again, the bot will notify you of how many seconds you need to wait.
    """

    def split_message(message, max_length=2000):
        return [message[i:i+max_length] for i in range(0, len(message), max_length)]

    for chunk in split_message(help_text):
        await ctx.send(chunk)

@bot.command(name='CCMeme')
@commands.cooldown(1, 5, commands.BucketType.user)
async def ccmeme(ctx: commands.Context):
    memes = await get_climate_change_memes()
    if memes:
        meme_url = random.choice(memes)
        await ctx.send(f"A meme about climate change: {meme_url}")
    else:
        await ctx.send("There was an error retrieving climate change memes or no memes were found.")

@bot.command(name='searchmm')
@commands.cooldown(1, 5, commands.BucketType.user)
async def searchmm(ctx: commands.Context, *, keyword: str):
    url = f'https://api.imgur.com/3/gallery/search?q={keyword}'
    memes = await fetch_memes(url)
    if memes:
        meme_url = random.choice(memes)
        await ctx.send(f"Here's a random meme for you to search: {meme_url}")
    else:
        await ctx.send(f"'{keyword}' No memes found for.")

@tasks.loop(hours=168)
async def announce_top_meme():
    if votes:
        top_meme_url = max(votes, key=votes.get)
        if announcement_channel_id:
            channel = bot.get_channel(announcement_channel_id)
            if channel:
                await channel.send(f"Most voted meme of the week: {top_meme_url}")
        votes.clear()
        save_data({'user_memes': user_memes, 'votes': votes})

@bot.command(name='setchannel')
async def set_channel(ctx: commands.Context, channel: discord.TextChannel):
    global announcement_channel_id
    announcement_channel_id = channel.id
    await ctx.send(f"As an announcement channel {channel.mention} is set.")

bot.run('')
