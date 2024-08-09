# MemeBot

MemeBot is a versatile and interactive Discord bot designed to bring fun and utility to your server. It offers a range of features, including meme sharing, random fact generation, IP lookup, hobby suggestions, and more.

## Features

- **Meme Commands**
  - `!meme [category]`: Fetches a random meme. Optionally specify a category.
  - `!addmeme <meme-url>`: Adds a meme to the bot's collection.
  - `!submitmeme <meme-url>`: Submits a meme for voting.
  - `!my_memes`: Lists memes you have submitted.
  - `!memevote <user-id> <vote>`: Votes for a meme by a specific user.
  - `!topmeme`: Displays the top-voted meme.
  - `!CCMeme`: Fetches a random climate change meme.
  - `!searchmm <keyword>`: Searches for memes on Imgur using a keyword.

- **Informational Commands**
  - `!ip <ip-address>`: Provides information about an IP address.
  - `!fact [limit]`: Retrieves random facts (limit between 1-10).
  - `!hobby [category]`: Suggests a hobby based on the given category.
  - `!password <length>`: Generates a random password.
  - `!ClimateChange`: Shares a random climate change fact.
  - `!weather <location>`: Provides current weather information for a specified location.
  - `!trivia [category]`: Retrieves a random trivia question. Optionally specify a category.

- **Server Management**
  - `!welcome`: Sets the welcome channel (admin only).
  - `!goodbye`: Sets the goodbye channel (admin only).
  - `!feedback <message>`: Sends feedback to the bot's feedback channel.
  - `!setannouncementchannel`: Sets the channel for meme announcements (admin only).
  - `!resetvotes`: Resets all meme votes (admin only).
  - `!resetdata`: Resets all user data and votes (admin only).
  - `!leaderboard`: Displays the top 5 users with the most votes.

## Setup

### Prerequisites

- Python 3.8 or higher
- A Discord bot token
- API keys for [Imgur](https://api.imgur.com/), [API Ninjas](https://api-ninjas.com/), and [Weather API](https://www.weatherapi.com/)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/RawryLionzTvo/GreenMemes_Bot.git
   cd MemeBot

2. **Install the required packages:**
   ```bash
   pip install -r requirements.txt

3. **Create a `.env` file in the root directory and add your API keys:**
   ```env
   IMGUR_CLIENT_ID=your_imgur_client_id
    API_NINJAS_KEY=your_api_ninjas_key
    WEATHER_API_KEY=your_weather_api_key
    BOT_TOKEN=your_discord_bot_token

4. **Run the bot:**
   ```bash
   python bot.py

## Command Overview

| Command                | Description                                                                                      |
|------------------------|--------------------------------------------------------------------------------------------------|
| `!hi`                  | Say hello to the bot.                                                                           |
| `!meme [category]`     | Fetch a random meme. Optionally specify a category to filter.                                   |
| `!addmeme <meme-url>`  | Add a meme to the bot's collection.                                                              |
| `!submitmeme <meme-url>` | Submit a meme for voting.                                                                       |
| `!my_memes`            | View the memes you’ve submitted.                                                                 |
| `!memevote <user-id> <vote>` | Vote for a user's meme. The vote should be a positive or negative integer.                  |
| `!topmeme`             | View the most voted meme.                                                                        |
| `!CCMeme`              | Get a random climate change meme from Imgur.                                                     |
| `!searchmm <keyword>`  | Search for memes on Imgur using a keyword.                                                       |
| `!ip <ip-address>`     | Look up information about an IP address.                                                         |
| `!fact [limit]`        | Get random facts. Specify the number of facts (1-10).                                            |
| `!hobby [category]`    | Get a random hobby suggestion. Optionally specify a category.                                    |
| `!password <length>`   | Generate a random password with the specified length (1-128).                                    |
| `!ClimateChange`       | Get a random climate change fact.                                                                |
| `!weather <location>`  | Get the current weather for a specified location.                                                |
| `!trivia [category]`   | Get a random trivia question. Optionally specify a category.                                      |
| `!resetvotes`          | Reset all meme votes (admin only).                                                                |
| `!resetdata`           | Reset all user data and votes (admin only).                                                       |
| `!setannouncementchannel` | Set the channel for meme announcements (admin only).                                           |
| `!welcome`             | Set the welcome channel (admin only).                                                             |
| `!goodbye`             | Set the goodbye channel (admin only).                                                             |
| `!setfeedback`         | Set the feedback channel (admin only).                                                           |
| `!leaderboard`         | Show the top 5 users with the most votes.                                                        |
| `!bot_help`            | Show the help message for bot commands.                                                           |


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Instructions for Use:
- **Copy the text above** and paste it into a new file named `README.md` in your project's root directory.
- Ensure to replace placeholders like `yourusername` in the installation section with your actual GitHub username if applicable.

### Next Steps:
**a.** Create a `requirements.txt` file with all the dependencies listed.  
**b.** Add unit tests for key functions to ensure code reliability.
