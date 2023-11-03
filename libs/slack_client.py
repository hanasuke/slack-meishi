from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from .person import Person


class SlackClientError(Exception):
    pass


class SlackClient:
    def __init__(self, token: str):
        self.client = WebClient(token=token)

    def get_channel_users(self, channel_name: str):
        try:
            channel_id = self.get_channel_id(channel_name)
            # TODO: adapt to cursor
            return self.client.conversations_members(channel=channel_id, limit=1000)[
                "members"
            ]

        except SlackApiError as e:
            print(f"Got an error: {e.response['error']}")
            raise SlackClientError("SlackApiError message")

        except SlackClientError as e:
            raise e

    def get_user_info(self, user_id: str):
        user = self.client.users_info(user=user_id)["user"]
        return Person(
            username=user["profile"]["display_name"],
            realname=user["profile"]["real_name"],
            icon_url=user["profile"]["image_512"],
        )

    def get_channel_id(self, channel_name: str):
        try:
            ch_list = self.client.conversations_list(
                limit=1000, types="public_channel"
            )["channels"]
            # TODO: adapt to cursor
            return [ch["id"] for ch in ch_list if ch["name"] == channel_name][0]

        except SlackApiError as e:
            print(f"Got an error: {e.response['error']}")
            raise SlackClientError("SlackApiError message")

        except IndexError as e:
            print(f"not found channel name {ch_list}")
            raise SlackClientError("channel not found")
