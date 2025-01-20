# Discord Key Distribution Bot

A Discord bot that manages and distributes keys to users through ephemeral messages (messages only visible to the command sender).

## Features

- Distribute keys through ephemeral messages (only visible to the command sender)
- Store keys and claims in a MySQL database
- Track which users claimed which keys
- Admin command to add new keys
- Users can claim multiple keys

## Prerequisites

- Python 3.10 or higher
- MySQL/MariaDB server
- Discord Bot Token
- LAMP stack environment

## Installation

1. Clone this repository or download the files

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your MySQL database:
   - Make sure MySQL server is running
   - Default configuration uses:
     - Host: localhost
     - User: root
     - Password: (empty)
     - Database: discord_keys (will be created automatically)

4. Configure your Discord bot:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Go to the Bot section
   - Create a bot and copy the token
   - Enable MESSAGE CONTENT INTENT in the Bot section
   - Add the token to `.env` file:
     ```
     DISCORD_TOKEN=your_bot_token_here
     ```

5. Invite the bot to your server:
   - Go to OAuth2 > URL Generator
   - Select 'bot' scope
   - Select required permissions:
     - Send Messages
     - View Channels
   - Use the generated URL to invite the bot

## Usage

### Start the Bot
```bash
python bot.py
```

### Commands

- `!key` - Get a key (sent via ephemeral message)
- `!addkey <key>` - Add a new key to the database (admin only)

### Examples

```
User: !key
Bot: Here is your key: `YOUR-KEY-HERE`

Admin: !addkey ABC123
Bot: Key added successfully!
```

## Database Structure

The bot uses two tables:

1. `license_keys`:
   - `key_id` (VARCHAR): The actual key
   - `claimed` (BOOLEAN): Whether the key has been claimed

2. `claims`:
   - `user_id` (BIGINT): Discord user ID of claimer
   - `key_id` (VARCHAR): The claimed key
   - `claim_date` (TIMESTAMP): When the key was claimed

## Security Features

- Database credentials can be configured in the code
- Admin-only commands are protected by Discord's permission system

## Contributing

Feel free to fork this repository and submit pull requests for any improvements.
