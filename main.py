from dotenv import load_dotenv
import os
import asyncio
from pyrogram import Client,enums,utils as pyrogram_utils
from pyrogram.errors import FloodWait
import sys
#pyrogram_utils.MIN_CHAT_ID = -999999999999
#pyrogram_utils.MAX_CHANNEL_ID = -100999999999999

# Load environment variables from .env file
load_dotenv("config.env")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
SOURCE_CHANNEL = os.getenv("SOURCE_CHANNEL")
DESTINATION_CHANNEL = os.getenv("DESTINATION_CHANNEL")
WAIT_TIME = int(os.getenv("WAIT_TIME", 0))  # Set default to 0 if not provided
BATCH_MODE = os.getenv("BATCH_MODE", "TRUE").upper() == "TRUE"  # BATCH_MODE default to True
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 1000))
BATCH_INTERVAL = int(os.getenv("BATCH_INTERVAL", 10))

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
            message_start_destination = await app.send_message(chat_id=int(DESTINATION_CHANNEL), text="Bot started!")
            await app.delete_messages(chat_id=DESTINATION_CHANNEL, message_ids=message_start_destination.id)
            
            await asyncio.sleep(2)  # Short sleep before starting the process

            # Get the last message from the source channel
            iter_message = app.get_chat_history(chat_id=int(SOURCE_CHANNEL), limit=1)
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
    count = 0
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

            # Handle wait time
            await asyncio.sleep(WAIT_TIME)

            # Batch mode handling
            count += 1
            if BATCH_MODE and count >= BATCH_SIZE:
                print(f"Batch size reached. Sleeping for {BATCH_INTERVAL} seconds.")
                save_last_forwarded_message_id(i)
                await asyncio.sleep(BATCH_INTERVAL)
                count = 0  # Reset counter after a batch
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
