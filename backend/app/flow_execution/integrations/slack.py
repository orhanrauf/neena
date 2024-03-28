import os
import requests

from typing import Any

from app.flow_execution.decorators import integration, task
from app.flow_execution.integrations.base import BaseIntegration
from app.flow_execution.models.base import BaseIntegrationActionModel
from app import schemas
from slack_sdk import WebClient
from slack_sdk.web.base_client import SlackResponse
from app.core.secrets import secrets_service
from app.core.config import settings
from app.flow_execution.decorators import task
from app.flow_execution.models.slack import (
    BaseSlackResponse,
    SlackChatMessage,
    SlackChatSendMessageAction,
    SlackChatSendMessageResponse,
    SlackChatDeleteMessageAction,
    SlackChatDeleteMessageResponse,
    SlackChatDeleteScheduledMessageAction,
    SlackChatUpdateMessageAction,
    SlackChatUpdateMessageResponse,
    SlackChatScheduleMessageAction,
    SlackChatScheduleMessageResponse,
    SlackChatGetPermalinkAction,
    SlackChatGetPermalinkResponse,
    SlackChatSendMeMessageAction,
    SlackChatSendMeMessageResponse,
    SlackConversations,
    SlackConversationsArchiveAction,
    SlackConversationsCreateAction,
    SlackConversationsCreateResponse,
    SlackConversationsHistoryAction,
    SlackConversationsHistoryResponse,
    SlackConversationsInfoAction,
    SlackConversationsInfoResponse,
    SlackConversationsInviteAction,
    SlackConversationsInviteResponse,
    SlackConversationsJoinAction,
    SlackConversationsJoinResponse,
    SlackConversationsListAction,
    SlackConversationsListResponse,
    SlackConversationsMembersAction,
    SlackConversationsMembersResponse,
    SlackConversationsOpenAction,
    SlackConversationsOpenResponse,
    SlackConversationsRenameAction,
    SlackConversationsRenameResponse,
    SlackConversationsRepliesAction,
    SlackConversationsRepliesResponse,
)


@integration(name="Slack", short_name="slack")
class SlackIntegration(BaseIntegration):
    """
    Integration class for Slack.
    Models implemented: message.
    """

    token: str

    def __init__(self, user: schemas.User) -> None:
        self.user = user
        self.token = self._fetch_credentials()
        self.base_params = self._construct_base_params()
        self.client = WebClient(token=self.token)

    def _fetch_credentials(self) -> str:
        """
        Fetches the user-specific Slack token from the key vault.
        """
        return secrets_service.get_secret(self.user, self._short_name)

    def _construct_base_params(self) -> dict:
        """
        Constructs the base query parameters for requests to the Slack API.
        """
        return {"token": self.token}

    def _model_to_query_params(self, model: BaseIntegrationActionModel) -> dict[str, Any]:
        """
        Converts a Pydantic model instance into a dictionary suitable for query parameters,
        respecting field aliases.
        """
        model_dict = model.model_dump(by_alias=True, exclude_none=True)
        return {**self.base_params, **model_dict}

    def check_connectivity(self) -> bool:
        """
        Checks if the Slack API is accessible by our application and the SDK is working.
        """
        max_no_conversations_to_list = 5
        response = self.client.conversations_list(limit=max_no_conversations_to_list)
        return response.status_code == 200

    @task(task_name="Send Message")
    def send_message(self, send_message_action: SlackChatSendMessageAction) -> SlackChatSendMessageResponse:
        """
        Sends a message to a Slack channel.
        """
        params = self._model_to_query_params(send_message_action)
        response = self.client.chat_postMessage(**params)
        return SlackChatSendMessageResponse(**response.data)

    @task(task_name="Update Message")
    def update_message(self, update_message_action: SlackChatUpdateMessageAction) -> SlackChatUpdateMessageResponse:
        """
        Updates a message in a Slack channel.
        """
        params = self._model_to_query_params(update_message_action)
        response = self.client.chat_update(**params)
        return SlackChatUpdateMessageResponse(**response.data)

    @task(task_name="Delete Message")
    def delete_message(self, delete_message_action: SlackChatDeleteMessageAction) -> SlackChatDeleteMessageResponse:
        """
        Deletes a message in a Slack channel.
        """
        params = self._model_to_query_params(delete_message_action)
        response = self.client.chat_delete(**params)
        return SlackChatDeleteMessageResponse(**response.data)

    @task(task_name="Delete Scheduled Message")
    def delete_scheduled_message(
        self, delete_scheduled_message_action: SlackChatDeleteScheduledMessageAction
    ) -> BaseSlackResponse:
        """
        Deletes a pending scheduled message from the queue.
        """
        params = self._model_to_query_params(delete_scheduled_message_action)
        response = self.client.chat_deleteScheduledMessage(**params)
        return BaseSlackResponse(**response.data)

    @task(task_name="Schedule Message")
    def schedule_message(self, schedule_message: SlackChatScheduleMessageAction) -> SlackChatScheduleMessageResponse:
        """
        Schedules a message to be sent to a channel.
        """
        params = self._model_to_query_params(schedule_message)
        response = self.client.chat_scheduleMessage(**params)
        return SlackChatScheduleMessageResponse(**response.data)

    @task(task_name="Get Message Permalink")
    def get_message_permalink(
        self, get_permalink_message: SlackChatGetPermalinkAction
    ) -> SlackChatGetPermalinkResponse:
        """
        Retrieves a permalink URL for a specific extant message
        """
        params = self._model_to_query_params(get_permalink_message)
        response = self.client.chat_getPermalink(**params)
        return SlackChatGetPermalinkResponse(**response.data)

    @task(task_name="Send Me Message")
    def send_me_message(self, send_me_message_action: SlackChatSendMeMessageAction) -> SlackChatSendMeMessageResponse:
        """
        Shares a Me message into a channel.
        """
        params = self._model_to_query_params(send_me_message_action)
        response = self.client.chat_meMessage(**params)
        return SlackChatSendMeMessageResponse(**response.data)

    @task(task_name="Archive Conversation")
    def archive_conversation(self, archive_conversation_action: SlackConversationsArchiveAction) -> BaseSlackResponse:
        """
        Archives a conversation.
        """
        params = self._model_to_query_params(archive_conversation_action)
        response = self.client.conversations_archive(**params)
        return BaseSlackResponse(**response.data)

    @task(task_name="Create Conversation")
    def create_conversation(
        self, create_conversation_action: SlackConversationsCreateAction
    ) -> SlackConversationsCreateResponse:
        """
        Initiates a public or private channel-based conversation
        """
        params = self._model_to_query_params(create_conversation_action)
        response = self.client.conversations_create(**params)
        return SlackConversationsCreateResponse(**response.data)

    @task(task_name="Get Conversation History")
    def get_conversation_history(
        self, get_conversation_history_action: SlackConversationsHistoryAction
    ) -> SlackConversationsHistoryResponse:
        """
        Fetches a conversation's history of messages and events.
        """
        params = self._model_to_query_params(get_conversation_history_action)
        response = self.client.conversations_history(**params)
        return SlackConversationsHistoryResponse(**response.data)

    @task(task_name="Get Conversation Info")
    def get_conversation_info(
        self, get_conversation_info_action: SlackConversationsInfoAction
    ) -> SlackConversationsInfoResponse:
        """
        Retrieve information about a conversation.
        """
        params = self._model_to_query_params(get_conversation_info_action)
        response = self.client.conversations_info(**params)
        return SlackConversationsInfoResponse(**response.data)

    @task(task_name="Invite Users To Channel")
    def invite_users_to_channel(
        self, invite_conversation_action: SlackConversationsInviteAction
    ) -> SlackConversationsInviteResponse:
        """
        Invites users to a channel.
        """
        params = self._model_to_query_params(invite_conversation_action)
        response = self.client.conversations_invite(**params)
        return SlackConversationsInviteResponse(**response.data)

    @task(task_name="Join Conversation")
    def join_conversation(
        self, join_conversation_action: SlackConversationsJoinAction
    ) -> SlackConversationsJoinResponse:
        """
        Joins an existing conversation.
        """
        params = self._model_to_query_params(join_conversation_action)
        response = self.client.conversations_join(**params)
        return SlackConversationsJoinResponse(**response.data)

    @task(task_name="List All Channels in Team")
    def list_all_channels_in_team(
        self, list_conversations_action: SlackConversationsListAction
    ) -> SlackConversationsListResponse:
        """
        Lists all channels in a Slack team.
        """
        params = self._model_to_query_params(list_conversations_action)
        response = self.client.conversations_list(**params)
        return SlackConversationsListResponse(**response.data)

    @task(task_name="Get Members")
    def get_members(
        self, get_conversation_members_action: SlackConversationsMembersAction
    ) -> SlackConversationsMembersResponse:
        """
        Retrieve members of a conversation.
        """
        params = self._model_to_query_params(get_conversation_members_action)
        response = self.client.conversations_members(**params)
        return SlackConversationsMembersResponse(**response.data)

    @task(task_name="Open Conversation")
    def open_conversation(
        self, open_conversation_action: SlackConversationsOpenAction
    ) -> SlackConversationsOpenResponse:
        """
        Opens or resumes a direct message or multi-person direct message.
        """
        params = self._model_to_query_params(open_conversation_action)
        response = self.client.conversations_open(**params)
        return SlackConversationsOpenResponse(**response.data)

    @task(task_name="Rename Conversation")
    def rename_conversation(
        self, rename_conversation_action: SlackConversationsRenameAction
    ) -> SlackConversationsRenameResponse:
        """
        Renames a conversation.
        """
        params = self._model_to_query_params(rename_conversation_action)
        response = self.client.conversations_rename(**params)
        return SlackConversationsRenameResponse(**response.data)

    @task(task_name="Get Replies")
    def get_replies(
        self, get_conversation_replies_action: SlackConversationsRepliesAction
    ) -> SlackConversationsRepliesResponse:
        """
        Retrieve a thread of messages posted to a conversation.
        """
        params = self._model_to_query_params(get_conversation_replies_action)
        response = self.client.conversations_replies(**params)
        return SlackConversationsRepliesResponse(**response.data)
