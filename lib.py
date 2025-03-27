from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.sessions import StringSession

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
session_string = os.getenv("SESSION_STRING")


async def get_all_user_ids(group_id):
    async with TelegramClient(
        StringSession(session_string), api_id, api_hash
    ) as client:
        # Fetch participants in batches
        all_users = []
        offset = 0

        while True:
            participants = await client(
                GetParticipantsRequest(
                    channel=group_id,
                    filter=ChannelParticipantsSearch(""),
                    offset=offset,
                    limit=100,  # Max per request
                    hash=0,
                )
            )

            if not participants.users:
                break

            all_users.extend([user.id for user in participants.users])
            offset += len(participants.users)

        print(f"Found {len(all_users)} users:")
        print(all_users)

        # Save to file
        # with open('user_ids.txt', 'w') as f:
        #     f.write('\n'.join(map(str, all_users)))

        return all_users


group_id = -1001768791701  # Your group ID (with -100 prefix)
if __name__ == "__main__":
    # Run the function
    # Must ensure the group ID is correct if you run standalone
    import asyncio
    asyncio.run(get_all_user_ids(group_id=group_id))
