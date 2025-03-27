#!/usr/bin/env python
# This program is dedicated to the public domain under the CC0 license.

import asyncio
from dotenv import load_dotenv
import os
import logging

from main import gen_image, get_random_greeting

from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram.constants import ChatMemberStatus
from telegram.helpers import mention_html

from lib import get_all_user_ids


# Load .env file
load_dotenv()  # Looks for `.env` in the current directory

# Access variables
api_key = os.getenv("TELEGRAM_BOT_TOKEN")  # Returns None if not found

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"""
        🌟 Welcome, {user.mention_html()}! 🌟

        - I'm your Eid Card Generator Bot! 🎉✨
        - Use the <b>/gen</b> command in a group to generate personalized Eid Mubarak messages and cards for all group members. 🌙🎨

        - Type <b>/help</b> if you need assistance. Let's spread joy and blessings! 🌸
        - This is an open source project and is available on GitHub 🚀. Feel free to contribute ❤️.
        """,
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a detailed help message when the command /help is issued."""
    await update.message.reply_html(
        """
        🤔 <b>Need Help?</b> 
Here's what I can do:

        - Use <b>/start</b> to see the welcome message.
        - Use <b>/gen</b> in a group to generate beautiful Eid Mubarak messages and cards for all group members. 🌙✨
        - Make sure to add me to a group and give me the necessary permissions to mention users and send images. 📸

        - This is an open source project and is available on GitHub 🚀. Feel free to contribute ❤️.
Let's make this Eid special! 🎉
        """
    )


async def gen_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate Eid Mubarak messages for all group members."""
    chat = update.effective_chat

    # Ensure the command is used in a group
    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("This command can only be used in groups.")
        return

    # Fetch all chat member IDs
    chat_member_ids = await get_all_user_ids(chat.id)

    # Send "Eid Mubarak" message to all chat members with mentions
    for user_id in chat_member_ids:
        try:
            # Fetch user details using get_chat_member
            chat_member = await context.bot.get_chat_member(chat.id, user_id)
            user = chat_member.user

            if (
                chat_member.status
                not in [
                    ChatMemberStatus.ADMINISTRATOR,
                    ChatMemberStatus.MEMBER,
                    ChatMemberStatus.OWNER
                ]
                or user.is_bot
            ):
                print(
                    f"Skipping user {user_id}, name {user.first_name} because of being {chat_member.status}"
                )
                continue

            # Generate a mention hyperlink for the user
            mention = mention_html(user.id, user.full_name or user.username or "User")
            message = f"👋 Hi {mention},\n🌙Eid Mubarak!\n\n🎉{get_random_greeting()}"

            image_file_name: str = user.full_name or user.username or "User"
            gen_image(image_file_name)

            try:
                with open(f"output/{image_file_name}.png", 'rb') as photo:
                    await context.bot.send_photo(
                        chat_id=chat.id,
                        photo=photo,
                        caption=message,
                        parse_mode="HTML"
                    )
            except Exception as e:
                await context.bot.send_message(chat.id, message, parse_mode="HTML")
                print(f"Error sending image: {e}")

            # await context.bot.send_message(chat.id, message, parse_mode="HTML")
            try:
                os.remove(f"output/{image_file_name}.png")
            except Exception as e:
                print(f"Error deleting image: {e}")

            await asyncio.sleep(1)
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(api_key).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("gen", gen_command))  # Add the /gen command

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
