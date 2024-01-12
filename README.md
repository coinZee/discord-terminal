# Discord-terminal
basically ur system terminal in discord

# Purpose?

- 1. You can basically (kinda) have ssh access to ur system without terminal

- 2. That's basically it

# Discord Terminal Bot

This Discord bot allows you to control the system terminal directly from within Discord.

## Caution

Please exercise caution when using this bot as it provides direct access to the system terminal. Improper usage or executing malicious commands can lead to unintended consequences or compromise the security of your system.

## Installation

1. Clone the repository: `git clone https://github.com/coinZee/discord-terminal.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Configure the bot token in the `.env` file.
    - Replace the BOT_KEY, Run the bot and use /show_id command it'll show you your id
    - You dont need to put "" or '' around the token and id
    - Replace the OWNER_ID with your id
4. Start the bot: `python main.py`

## Usage

- Invite the bot to your server, type in any channel the bot has access to, the command will run.
- /ctrl_c to kill current process

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
