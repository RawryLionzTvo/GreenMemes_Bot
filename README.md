# Discord Meme and Utility Bot

This is a versatile Discord bot written in Python using the `discord.py` library. The bot provides various fun and utility commands, such as fetching random memes, generating passwords, retrieving IP information, and more. It also includes commands that fetch interesting facts and random hobbies using external APIs.

## Features

- **Meme Commands:**
  - `!meme [category]`: Fetches a random meme. If a category is specified, a meme from that category is shared.
  - `!addmeme <category> <meme-url>`: Adds a meme to a specified category.
  - `!submitmeme <meme-url>`: Submits a meme for voting.
  - `!my_memes`: Lists the memes submitted by the user.
  - `!vote <meme-id>`: Votes for a submitted meme.
  - `!topmeme`: Displays the most voted meme of the week.
  - `!CCMeme`: Shares a random meme about climate change.

- **Utility Commands:**
  - `!ip <ip-address>`: Retrieves geographic and network information for a given IP address.
  - `!password <length>`: Generates a random password of the specified length.
  - `!hobby [category]`: Fetches a random hobby suggestion.
  - `!fact [limit]`: Fetches random facts (default limit is 3).

- **Informational Commands:**
  - `!ClimateChange`: Shares a random fact about the environment and climate change.
  - `!helpbot`: Provides a list of all available commands.

- **Configuration Commands:**
  - `!setchannel <channel>`: Sets the channel where the most voted meme of the week will be announced.

## Installation

### Prerequisites

- Python 3.8 or higher.
- A Discord account and a bot token.
- API keys for Imgur and API Ninjas.

### Setup

1. Clone the repository or download the bot code.
2. Install the required Python packages using the following command:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a file named `.env` (optional) or edit the script to include your bot token and API keys:

    ```bash
    DISCORD_BOT_TOKEN=your_discord_bot_token
    IMGUR_CLIENT_ID=your_imgur_client_id
    API_NINJAS_KEY=your_api_ninjas_key
    ```

4. Run the bot using:

    ```bash
    python bot.py
    ```

## Configuration

- **Logging**: The bot is configured to log information using Python's built-in `logging` module.
- **Persistent Storage**: The bot stores user-submitted memes and votes in a JSON file (`bot_data.json`) for persistent storage.

## Usage

Invite the bot to your Discord server and use the following commands:

- **General Commands:**
  - `!hi`: Greet the bot.
  - `!helpbot`: Get a list of available commands.

- **Meme Commands:**
  - `!meme [category]`: Fetch a random meme. Specify a category to narrow the selection.
  - `!addmeme <category> <meme-url>`: Add a meme to a specified category.
  - `!submitmeme <meme-url>`: Submit a meme for community voting.
  - `!my_memes`: View the memes you've submitted.
  - `!vote <meme-id>`: Vote for a specific meme.
  - `!topmeme`: View the top-voted meme of the week.

- **Utility Commands:**
  - `!ip <ip-address>`: Look up information about an IP address.
  - `!password <length>`: Generate a random password.
  - `!hobby [category]`: Get a random hobby suggestion.
  - `!fact [limit]`: Retrieve random facts.

- **Informational Commands:**
  - `!ClimateChange`: Learn a random climate change fact.
  - `!CCMeme`: Get a random climate change meme.

- **Configuration Commands:**
  - `!setchannel <channel>`: Set the announcement channel for the top meme.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue on GitHub.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
