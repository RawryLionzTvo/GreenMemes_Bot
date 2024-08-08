# Meme Bot

Meme Bot is a Discord bot designed to share memes, allow users to submit and vote on memes, and provide random climate change facts. It also fetches memes from Imgur based on specified categories and keywords.

## Features

- Fetch and share random memes from Imgur.
- Allow users to submit their own memes.
- Voting system for user-submitted memes.
- Announcement of the most voted meme every week.
- Share random facts about climate change.
- Fetch memes based on specific keywords.
- Commands to interact with the bot easily.

## Commands

### General Commands

- `!hi`: The bot will greet you.
- `!helpbot`: Provides a detailed list of all available commands and how to use them.

### Meme Commands

- `!meme [category]`: Shares a random meme. If a category is specified, it fetches memes from that category.
- `!addmeme <category> <meme-url>`: Adds a meme to a specified category.
- `!submitmeme <meme-url>`: Allows users to submit their own meme. The meme is then added to the voting system.
- `!my_memes`: Lists all memes submitted by the user.
- `!vote <meme-id>`: Vote for a specific meme by its ID.
- `!topmeme`: Shows the most voted meme of the week.
- `!searchmm <keyword>`: Searches for memes on Imgur based on the specified keyword.

### Climate Change Commands

- `!ClimateChange`: Shares a random fact about climate change.
- `!CCMeme`: Shares a random meme related to climate change.

### Admin Commands

- `!setchannel <channel>`: Sets the channel where the most voted meme of the week will be announced.

## Installation

### Prerequisites

- Python 3.8+
- Discord.py
- A Discord bot token
- Imgur Client ID

### Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/memebot.git
    cd memebot
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Add your Discord bot token and Imgur Client ID:

    - Open the bot script and replace `YOUR_DISCORD_BOT_TOKEN` with your actual Discord bot token.
    - Replace `IMGUR_CLIENT_ID` with your Imgur Client ID.

4. Run the bot:

    ```bash
    python bot.py
    ```

### Running the Bot

- Make sure you have the bot's token and other configurations set up correctly.
- Run the bot using the command:

    ```bash
    python bot.py
    ```

## Persistent Storage

- The bot uses a JSON file (`bot_data.json`) for persistent storage to save user-submitted memes and votes.
- Ensure that this file is available and writable in the bot's working directory.

## Logging

- The bot is configured with basic logging to help track its activities and troubleshoot issues.
- Logs are displayed in the console.

## Contributing

Contributions are welcome! If you have suggestions or improvements, feel free to create an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
