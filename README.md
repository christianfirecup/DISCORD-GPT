# Discord GPT Bot

This project implements a Discord bot leveraging OpenAI's GPT models to interact with users within Discord servers. The bot is capable of responding to commands, managing user-specific data, and utilizing AI models for natural language understanding and generation.

## Features

- Respond to specific commands (`$hello`, `$ask`, `$createdir`, `$CreateSave`, etc.)
- Create directories and save user data in JSON format.
- Dynamic model loading to change the AI behavior on the fly.
- Asynchronous design for efficient handling of Discord events.

## Setup

To set up the Discord GPT Bot, follow these steps:

### Prerequisites

- Python 3.8 or higher
- `discord.py` library
- `python-dotenv` library for environment variable management
- An OpenAI API key and a Discord Bot token.

### Installation

1. Clone the repository to your local machine.

   ```
   git clone [repository URL]
   cd [local repository]
   ```

2. Install the required Python packages.

   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory of the project and add your Discord Bot Token and OpenAI API key:

   ```
   DISCORD_TOKEN=DISCORD-BOT-TOKEN
   OPENAI=OPENAI-KEY
   Assistant_OpenAI=Defualt-Assistant
   ```

### Usage

To run the bot, use the following command:

```
python main.py
```

Once the bot is running, it will log into Discord and you can interact with it using the predefined commands.

## Commands

- `$hello` - The bot will greet the user.
- `$ask [query]` - The bot will respond to the query using the AI model.
- `$createdir` - The bot will create a directory for the user.
- `$CreateSave` - The bot will save user-specific data into a file.
- `$nme [bot_name]` - Assign a new name to the bot for the user.
- `$instruct [instructions]` - Provide instructions to the bot.
- `$LoadGPT [model]` - Change the AI model the bot is using.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your features or fixes.

## License

[MIT]
