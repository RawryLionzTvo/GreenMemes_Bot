# Discord Meme Bot

A versatile Discord bot designed for meme sharing, trivia, climate change facts, and more. This bot provides various interactive commands to enhance server engagement and fun.

## Features

- **Meme Commands:**
  - `!meme [category]`: Get a random meme. Optionally specify a category.
  - `!addmeme [meme_url]`: Add a meme to the bot's collection.
  - `!submitmeme [meme_url]`: Submit a meme for voting.
  - `!my_memes`: View the memes you've submitted.
  - `!memevote [user_id] [vote]`: Vote for a user's meme.
  - `!topmeme`: View the most voted meme.
  - `!searchmm [keyword]`: Search for memes on Imgur by keyword.

- **Climate Change Commands:**
  - `!ClimateChange`: Get a random climate change fact.
  - `!CCMeme`: Get a random climate change meme from Imgur.

- **Utility Commands:**
  - `!password [length]`: Generate a random password with the specified length (1-128).
  - `!hobby [category]`: Get a random hobby suggestion. Optionally specify a category.
  - `!ip [ip_addr]`: Look up information about an IP address.
  - `!weather [city]`: Get the current weather for a specified location.
  - `!trivia [category]`: Get a random trivia question. Optionally specify a category.

- **Admin Commands:**
  - `!ban [member] [reason]`: Ban a user from the server.
  - `!kick [member] [reason]`: Kick a user from the server.
  - `!mute [member] [minutes] [reason]`: Mute a user for a specified number of minutes.
  - `!unmute [member]`: Unmute a user.
  - `!resetvotes`: Reset all meme votes (admin only).
  - `!resetdata`: Reset all user data and votes (admin only).
  - `!setannouncementchannel [channel_id]`: Set the channel for meme announcements (admin only).
  - `!welcome [channel_id]`: Set the welcome channel (admin only).
  - `!goodbye [channel_id]`: Set the goodbye channel (admin only).
  - `!setfeedback [channel_id]`: Set the feedback channel (admin only).
  - `!leaderboard`: Show the top 5 users with the most votes.

- **Miscellaneous Commands:**
  - `!hi`, `!hello`, `!hey`: Say hello to the bot.
  - `!fact [limit]`: Get random facts. Specify the number of facts (1-10).
  - `!bot_help`, `!helpbot`: Show the help message.

## Needed

### Prerequisites

- Python 3.8 or higher
- A Discord bot token
- API keys for [Imgur](https://api.imgur.com/), [API Ninjas](https://api-ninjas.com/), and [Weather API](https://www.weatherapi.com/)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/RawryLionzTvo/GreenMemes_Bot.git

2. **Install the required packages:**
   ```bash
   pip install -r requirements.txt

3. **Create a `.env` file in the root directory and add your API keys:**
   ```env
   IMGUR_CLIENT_ID=your_imgur_client_id
   API_NINJAS_KEY=your_api_ninjas_key
   BOT_TOKEN=your_discord_bot_token
   WEATHER_API_KEY=your_weather_api_key

4. **Run the bot:**
   ```bash
   python bot.py

## Command Overview

| Command                        | Description                                                                                      |
|--------------------------------|--------------------------------------------------------------------------------------------------|
| `!hi`, `!hello`, `!hey`        | Greets the user.                                                                               |
| `!meme [category]`             | Fetch a random meme. Optionally specify a category to filter.                                   |
| `!addmeme [meme-url]`          | Add a meme URL to the bot's database.                                                            |
| `!submitmeme [meme-url]`       | Submit a meme for voting.                                                                       |
| `!my_memes`                    | View the memes you’ve submitted.                                                                 |
| `!memevote [user-id] [vote]`   | Vote for a user's meme. The vote should be a positive or negative integer.                      |
| `!topmeme`                     | View the most voted meme.                                                                        |
| `!ClimateChange`               | Get a random climate change fact.                                                                |
| `!CCMeme`                      | Get a random climate change meme from Imgur.                                                     |
| `!password [length]`           | Generate a random password with the specified length (1-128).                                    |
| `!hobby [category]`            | Get a random hobby suggestion. Optionally specify a category.                                    |
| `!ip [ip_addr]`                | Look up information about an IP address.                                                         |
| `!weather [city]`              | Get the current weather for a specified city.                                                    |
| `!trivia [category]`           | Get a random trivia question. Optionally specify a category.                                      |
| `!resetvotes`                  | Reset all meme votes (admin only).                                                                |
| `!resetdata`                   | Reset all user data and votes (admin only).                                                       |
| `!setannouncementchannel [channel_id]` | Set the channel for announcements (admin only).                                               |
| `!welcome [channel_id]`        | Set the welcome channel (admin only).                                                             |
| `!goodbye [channel_id]`        | Set the goodbye channel (admin only).                                                             |
| `!setfeedback [channel_id]`    | Set the feedback channel (admin only).                                                           |
| `!leaderboard`                 | Show the top users with the most votes.                                                          |
| `!ban [member] [reason]`       | Ban a user from the server.                                                                      |
| `!kick [member] [reason]`      | Kick a user from the server.                                                                     |
| `!mute [member] [minutes] [reason]` | Mute a user for a specified number of minutes.                                               |
| `!unmute [member]`             | Unmute a user.                                                                                  |
| `!bot_help`, `!helpbot`        | Display the help message for bot commands.                                                       |


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
