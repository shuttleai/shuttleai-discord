# 🚀 ShuttleAI Discord multi-purpose Al

Welcome to the **#1 Free Discord AI Chatbot** powered by ShuttleAI. This bot brings advanced AI capabilities right into your Discord server.

> [!IMPORTANT]
> Join our Discord server for support: [discord.gg/shuttleai](https://discord.gg/shuttleai)

## 🎮 Connect with Us on Discord

[![Join us on Discord](https://invidget.switchblade.xyz/shuttleai)](https://discord.gg/shuttleai)


## 🌟 Features

- 🗣️ Advanced AI chat capabilities
- 🎨 Image generation
- ⚙️ Customizable settings
- 🎮 Easy integration with Discord
- 🚀 And much more!

## 📜 Commands

- `/setup`: 🛠️ Run /setup in the channel you want to use ShuttleAI in. Any message sent in that channel will be processed by ShuttleAI. Run /remove to remove the channel.
- `/remove`: 🗑️ Run /remove in the channel you want to remove ShuttleAI from processing messages in.
- `/reset`: 🔄 Run /reset to reset your conversation history with ShuttleAI.
- `/imagine`: 🎨 Run /imagine to generate an image. Choose between many models.
- `/settings`: ⚙️ Run /settings to configure the bot's personality, tts, and model.
- `/personality`: 🎭 Run /personality to set a custom personality. This command is only available for ShuttleAI Premium users.

## 🚀 Installation

> [!TIP]
> Follow these steps to quickly set up ShuttleAI.

### Step 1. 🎬 Git clone repository

Clone this repository using the following command:

```shell
git clone https://github.com/shuttleai/shuttleai-discord
```

Then, navigate into the cloned repository:

```shell
cd shuttleai-discord
```

### Step 2. 🗝️ Get your ShuttleAI API Key

After signing up, navigate to [shuttleai.app/keys](https://shuttleai.app/keys) to get your API key. You'll enter this key in the `.env` file:

```env
SHUTTLEAI_API_KEY='your-api-key-here'
```



### Step 3. 📚 Create a MongoDB database

You'll need a MongoDB database for the bot to store data. If you don't have one, you can create a free one at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).

### Step 4. 🤖 Get your Discord Bot Token

Go to the [Discord Developer Portal](https://discord.com/developers/applications), create a new application and get your bot token.

### Step 5. ⚙️ Configure your environment variables

Rename the `.env.example` file to `.env`. Fill out the environment variables in the `.env` file:

```env
SHUTTLEAI_API_KEY='' # Your ShuttleAI API Key
DISCORD_BOT_TOKEN='' # Your Discord Bot Token

STREAM_URL='' # Stream URL, e.g. https://www.twitch.tv/username
STREAM_NAME='' # Stream Name, e.g. /imagine

MONGO_URI='' # Your MongoDB URI, e.g. mongodb://localhost:27017
```

### Step 6. 📦 Install the requirements

Run the following command to install the necessary Python packages:

```shell
pip install -r requirements.txt
```

### Step 7. 🚀 Start the bot

Run the following command to start your bot:

```shell
python main.py
```

## 🆘 Support

If you encounter any issues or need further assistance, create an issue in this repository. We're here to help!

Enjoy your new AI-powered Discord bot!