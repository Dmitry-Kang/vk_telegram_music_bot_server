# Telegram & VK Music Bot

Welcome to the Telegram & VK Music Bot project! This Python-based project involves two bots—one for Telegram and another for VKontakte (VK). The VK bot allows users to send music or playlists, which the bot then downloads and forwards to the Telegram bot.

## Prerequisites

Before starting the bots, ensure you have the following prerequisites:

- Python installed on your system.
- Required Python packages (install using `pip install -r requirements.txt`).
- System dependencies (install using `sudo apt install build-essential libssl-dev libffi-dev python-dev ffmpeg`).

## Configuration

1. Create a `.env` file in the project root with the following fields:

```env
TELEGRAM_TOKEN=your_telegram_token
VK_LOGIN=your_vk_login
VK_PASSWORD=your_vk_password
VK_TOKEN=your_vk_token
VK_ADMIN_ID=your_vk_admin_id
TG_ADMIN_ID=your_telegram_admin_id
```

- `TELEGRAM_TOKEN`: Telegram bot token.
- `VK_LOGIN`: VKontakte login.
- `VK_PASSWORD`: VKontakte password.
- `VK_TOKEN`: VKontakte API token.
- `VK_ADMIN_ID`: VKontakte admin user ID.
- `TG_ADMIN_ID`: Telegram admin user ID.

## Running the Bots

1. Run the VK bot:

```bash
python3 vk.py
```

2. Run the Telegram bot:

```bash
python3 tg.py
```

## Usage

1. Send music or playlists to the VK bot in VKontakte.
2. The VK bot downloads the music and forwards it to the Telegram bot.
3. The Telegram bot receives the music and processes the request.

## Important Notes

- The VK bot requires VK login credentials and an API token.
- Make sure to handle sensitive information, such as login credentials and API tokens, securely.
- Admin IDs are used for admin-related functionalities.

## Contribution

Contributions are welcome! If you have suggestions or want to improve the bots, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Enjoy your music with the Telegram & VK Music Bot! 🎶🤖
