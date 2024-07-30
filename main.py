import discord
import google.generativeai as genai
import os

# Replace with your actual token and API key
discord_token = "YOUR DISCORD BOT TOKEN"
GEMINI_KEY = "YOUR GEMINI API SECRET KEY"


# Configure the Google Generative AI API
genai.configure(api_key=GEMINI_KEY)


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        # Don't respond to messages from the bot itself
        if self.user == message.author:
            return

        # Only respond if the bot is mentioned
        if self.user in message.mentions:
            try:
                config = {
                    "temperature": 1,
                    "top_p": 0.95,
                    "top_k": 64,
                    "max_output_tokens": 50,
                    "response_mime_type": "text/plain",
                }

                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    generation_config=config
                )

                chat_session = model.start_chat(
                    history=[]
                )

                response = chat_session.send_message(message.content)

                # Print response for debugging
                print(response.text)

                # Send response to the Discord channel
                await message.channel.send(response.text)
            except Exception as e:
                await message.channel.send(f"An error occurred: {str(e)}")


# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Create and run the client
client = MyClient(intents=intents)
client.run(discord_token)
