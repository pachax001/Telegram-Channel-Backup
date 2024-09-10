from dotenv import load_dotenv
import os
import asyncio
from pyrogram import Client
from time import sleep
from pyrogram.errors import FloodWait


import sys

# Load environment variables from .env file
load_dotenv("config.env")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL")
DESTINATION_CHANNEL = os.getenv("DESTINATION_CHANNEL")
WAIT_TIME = int(os.getenv("WAIT_TIME", 0))  # Set default to 0 if not provided

# Check if required env variables are set
if not API_ID or not API_HASH or not SOURCE_CHANNEL or not DESTINATION_CHANNEL:
    print("Please fill all the required fields in config.env file!")
    sys.exit()

# Initialize Pyrogram Client
app = Client("User", api_id=API_ID, api_hash=API_HASH)

def get_caption(message):
    """Extracts caption from the message."""
    return message.caption.html if message.caption else None

def save_last_forwarded_message_id(last_forwarded_message_id):
    """Saves the ID of the last forwarded message to a text file."""
    with open("last_forwarded_message_id.txt", "w") as f:
        f.write(str(last_forwarded_message_id))

async def main():
    try:
        async with app:
            # Notify both source and destination channels that the bot has started
            message_start_source = await app.send_message(chat_id=SOURCE_CHANNEL, text="Bot started!")
            await app.delete_messages(chat_id=SOURCE_CHANNEL, message_ids=message_start_source.id)

            message_start_destination = await app.send_message(chat_id=DESTINATION_CHANNEL, text="Bot started!")
            await app.delete_messages(chat_id=DESTINATION_CHANNEL, message_ids=message_start_destination.id)
            
            sleep(2)  # Short sleep before starting the process

            # Get the last message from the source channel
            iter_message = app.get_chat_history(chat_id=SOURCE_CHANNEL, limit=1)
            async for message in iter_message:
                last_message_id = message.id
                print(f"Last message id: {last_message_id}")
                break

            # Check if we have a last forwarded message ID stored
            if os.path.exists("last_forwarded_message_id.txt"):
                with open("last_forwarded_message_id.txt", "r") as f:
                    last_forwarded_message_id = int(f.read())
                    print(f"Last forwarded message id: {last_forwarded_message_id}")
                    await forward(last_forwarded_message_id + 1, last_message_id)
            else:
                await forward(1, last_message_id)
    except KeyboardInterrupt:
        print("Bot stopped!")
        await app.stop()
        sys.exit()
    except FloodWait as e:
        print(f"FloodWait: Sleeping for {e.value} seconds due to rate limits.")
        await asyncio.sleep(e.value)
        await main()
    except Exception as e:
        print(f"Error: {e}")
        await app.stop()
        sys.exit()


async def forward(start_message_id, end_message_id):
    """Forwards messages from source channel to destination channel."""
    for i in range(start_message_id, end_message_id + 1):
        try:
            message = await app.get_messages(chat_id=SOURCE_CHANNEL, message_ids=i)

            if message.service:
                print("Service message found!")
                continue
            if message.empty:
                print(f"Message {i} not found! Probably deleted.")
                continue
            caption = get_caption(message)
            await app.copy_message(
                chat_id=DESTINATION_CHANNEL,
                from_chat_id=SOURCE_CHANNEL,
                message_id=i,
                caption=caption
            )
            # Save last forwarded message ID
            save_last_forwarded_message_id(i)
            print(f"Message {i} forwarded!")
            await asyncio.sleep(WAIT_TIME)
        except KeyboardInterrupt:
            print("Bot stopped!")
            save_last_forwarded_message_id(i)
            await app.stop()
            sys.exit()
        except FloodWait as e:
            print(f"FloodWait: Sleeping for {e.value} seconds due to rate limits.")
            await asyncio.sleep(e.value)
        except Exception as e:
            print(f"Error: {e}")
            save_last_forwarded_message_id(i)
            await app.stop()
            sys.exit()

if __name__ == "__main__":
    try:
        app.run(main())
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt caught at the main level. Shutting down...")
        sys.exit(0)
