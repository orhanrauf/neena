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
    SlackChatMessageSend,
    SlackChatMessageSendResponse,
    SlackChatMessageDelete,
    SlackChatMessageDeleteResponse,
    SlackChatMessageDeleteScheduled,
    SlackChatMessageUpdate,
    SlackChatMessageUpdateResponse,
    SlackChatMessageSchedule,
    SlackChatMessageScheduleResponse,
    SlackChatMessageGetPermalink,
    SlackChatMessageGetPermalinkResponse,
    SlackChatMessageSendMe,
    SlackChatMessageSendMeResponse,
    SlackConversations,
    SlackConversationsArchive,
    SlackConversationsCreate,
    SlackConversationsCreateResponse,
    SlackConversationsHistory,
    SlackConversationsHistoryResponse,
    SlackConversationsInfo,
    SlackConversationsInfoResponse,
    SlackConversationsInvite,
    SlackConversationsInviteResponse,
    SlackConversationsJoin,
    SlackConversationsJoinResponse,
    SlackConversationsList,
    SlackConversationsListResponse,
    SlackConversationsMembers,
    SlackConversationsMembersResponse,
    SlackConversationsOpen,
    SlackConversationsOpenResponse,
    SlackConversationsRename,
    SlackConversationsRenameResponse,
    SlackConversationsReplies,
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
        max_no_conversations = 5
        response = self.client.conversations_list(limit=max_no_conversations)
        return response.status_code == 200

    @task(task_name="Send Message")
    def send_message(self, message_to_send: SlackChatMessageSend) -> SlackChatMessageSendResponse:
        """
        Sends a message to a Slack channel.
        """
        params = self._model_to_query_params(message_to_send)
        response = self.client.chat_postMessage(**params)
        return SlackChatMessageSendResponse(**response.data)

    @task(task_name="Update Message")
    def update_message(self, message_to_update: SlackChatMessageUpdate) -> SlackChatMessageUpdateResponse:
        """
        Updates a message in a Slack channel.
        """
        params = self._model_to_query_params(message_to_update)
        response = self.client.chat_update(**params)
        return SlackChatMessageUpdateResponse(**response.data)

    @task(task_name="Delete Message")
    def delete_message(self, message_to_delete: SlackChatMessageDelete) -> SlackChatMessageDeleteResponse:
        """
        Deletes a message in a Slack channel.
        """
        params = self._model_to_query_params(message_to_delete)
        response = self.client.chat_delete(**params)
        return SlackChatMessageDeleteResponse(**response.data)

    @task(task_name="Delete Scheduled Message")
    def delete_scheduled_message(
        self, scheduled_message_to_delete: SlackChatMessageDeleteScheduled
    ) -> BaseSlackResponse:
        """
        Deletes a pending scheduled message from the queue.
        """
        params = self._model_to_query_params(scheduled_message_to_delete)
        response = self.client.chat_deleteScheduledMessage(**params)
        return BaseSlackResponse(**response.data)

    @task(task_name="Schedule Message")
    def schedule_message(self, message_to_schedule: SlackChatMessageSchedule) -> SlackChatMessageScheduleResponse:
        """
        Schedules a message to be sent to a channel.
        """
        params = self._model_to_query_params(message_to_schedule)
        response = self.client.chat_scheduleMessage(**params)
        return SlackChatMessageScheduleResponse(**response.data)

    @task(task_name="Get Message Permalink")
    def get_message_permalink(self, message: SlackChatMessageGetPermalink) -> SlackChatMessageGetPermalinkResponse:
        """
        Retrieves a permalink URL for a specific extant message
        """
        params = self._model_to_query_params(message)
        response = self.client.chat_getPermalink(**params)
        return SlackChatMessageGetPermalinkResponse(**response.data)

    @task(task_name="Send Me Message")
    def send_me_message(self, message_to_send: SlackChatMessageSendMe) -> SlackChatMessageSendMeResponse:
        """
        Shares a Me message into a channel.
        """
        params = self._model_to_query_params(message_to_send)
        response = self.client.chat_meMessage(**params)
        return SlackChatMessageSendMeResponse(**response.data)

    @task(task_name="Archive Conversation")
    def archive_conversation(self, conversation_to_archive: SlackConversationsArchive) -> BaseSlackResponse:
        """
        Archives a conversation.
        """
        params = self._model_to_query_params(conversation_to_archive)
        response = self.client.conversations_archive(**params)
        return BaseSlackResponse(**response.data)

    @task(task_name="Create Conversation")
    def create_conversation(self, conversation_to_create: SlackConversationsCreate) -> SlackConversationsCreateResponse:
        """
        Initiates a public or private channel-based conversation
        """
        params = self._model_to_query_params(conversation_to_create)
        response = self.client.conversations_create(**params)
        return SlackConversationsCreateResponse(**response.data)

    @task(task_name="Get Conversation History")
    def get_conversation_history(
        self, conversation_history: SlackConversationsHistory
    ) -> SlackConversationsHistoryResponse:
        """
        Fetches a conversation's history of messages and events.
        """
        params = self._model_to_query_params(conversation_history)
        response = self.client.conversations_history(**params)
        return SlackConversationsHistoryResponse(**response.data)

    @task(task_name="Get Conversation Info")
    def get_conversation_info(self, conversation_info: SlackConversationsInfo) -> SlackConversationsInfoResponse:
        """
        Retrieve information about a conversation.
        """
        params = self._model_to_query_params(conversation_info)
        response = self.client.conversations_info(**params)
        return SlackConversationsInfoResponse(**response.data)

    @task(task_name="Invite Users To Channel")
    def invite_users_to_channel(
        self, conversations_invite: SlackConversationsInvite
    ) -> SlackConversationsInviteResponse:
        """
        Invites users to a channel.
        """
        params = self._model_to_query_params(conversations_invite)
        response = self.client.conversations_invite(**params)
        return SlackConversationsInviteResponse(**response.data)

    @task(task_name="Join Conversation")
    def join_conversation(self, join_conversation: SlackConversationsJoin) -> SlackConversationsJoinResponse:
        """
        Joins an existing conversation.
        """
        params = self._model_to_query_params(join_conversation)
        response = self.client.conversations_join(**params)
        return SlackConversationsJoinResponse(**response.data)

    @task(task_name="List All Channels in Team")
    def list_all_channels_in_team(self, conversations_list: SlackConversationsList) -> SlackConversationsListResponse:
        """
        Lists all channels in a Slack team.
        """
        params = self._model_to_query_params(conversations_list)
        response = self.client.conversations_list(**params)
        return SlackConversationsListResponse(**response.data)

    @task(task_name="Get Members")
    def get_members(self, conversation_members: SlackConversationsMembers) -> BaseSlackResponse:
        """
        Retrieve members of a conversation.
        """
        params = self._model_to_query_params(conversation_members)
        response = self.client.conversations_members(**params)
        return BaseSlackResponse(**response.data)

    @task(task_name="Open Conversation")
    def open_conversation(self, conversation_open_model: SlackConversationsOpen) -> SlackConversationsOpenResponse:
        """
        Opens or resumes a direct message or multi-person direct message.
        """
        params = self._model_to_query_params(conversation_open_model)
        response = self.client.conversations_open(**params)
        return SlackConversationsOpenResponse(**response.data)

    @task(task_name="Rename Conversation")
    def rename_conversation(
        self, conversation_rename_model: SlackConversationsRename
    ) -> SlackConversationsRenameResponse:
        """
        Renames a conversation.
        """
        params = self._model_to_query_params(conversation_rename_model)
        response = self.client.conversations_rename(**params)
        return SlackConversationsRenameResponse(**response.data)

    @task(task_name="Get Replies")
    def get_replies(self, conversation_replies_model: SlackConversationsReplies) -> SlackConversationsRepliesResponse:
        """
        Retrieve a thread of messages posted to a conversation.
        """
        params = self._model_to_query_params(conversation_replies_model)
        response = self.client.conversations_replies(**params)
        return SlackConversationsRepliesResponse(**response.data)
