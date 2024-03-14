from pydantic.fields import Field
from datetime import datetime, date
from typing import Optional, Union, Dict, Sequence
from slack_sdk.models.metadata import Metadata
from pydantic import StrictBool, StrictStr

from app.flow_execution.models.base import BaseAPIModel, BaseIntegrationActionModel


class SlackChatMessage(BaseAPIModel):
    """
    Slack API Chat model.
    tl;dr: Chat is specifically about sending and managing messages.

    In the context of the Slack API, the term "chat" refers to the act of
    sending messages or posting content within Slack. When you're dealing with
    the Slack API, particularly with the chat.* methods
    (such as chat.postMessage), you're primarily focused on the action of
    sending messages to channels, direct messages (DMs),
    multi-party direct messages (MPDMs), or private groups.
    The chat API methods are specifically designed for creating or
    manipulating messages.
    """

    channel: StrictStr = Field(
        description="Channel, private group, or IM channel to send message to. Can be an encoded ID, or a name.",
    )
    as_user: Optional[StrictBool] = Field(
        default=None,
        description="(Legacy) Pass true to post the message as the authed user instead of as a bot. Defaults to false.",
    )
    attachments: Optional[StrictStr] = Field(
        default=None,
        description="""
        The message content in the form of a JSON-based array of structured attachments, 
        presented as a URL-encoded string.
        Example: [{"pretext": "pre-hello", "text": "text-world"}]
        """,
    )
    blocks: Optional[StrictStr] = Field(
        default=None,
        description="""
        The message content in the form of a JSON-based array of structured blocks, 
        presented as a URL-encoded string.
        Example: [{"type": "section", "text": {"type": "plain_text", "text": "Hello world"}}]
        """,
    )
    file_ids: Optional[Union[str, Sequence[str]]] = Field(
        default=None,
        description="""
        Array of new file ids that will be sent with this message. 
        
        Examples: F013GKY52QK,F013GL22D0T or ["F013GKY52QK","F013GL22D0T"]
        """,
    )
    link_names: Optional[StrictBool] = Field(default=None, description="Find and link user groups.")
    message_ts: Optional[str] = Field(
        default=None,
        description="""
        A message's ts (timestamp) value, uniquely identifying it within a channel
        
        Example: 1234567890.123456
        """,
    )
    metadata: Optional[Union[Dict, Metadata]] = Field(
        default=None,
        description="""
        JSON object with event_type and event_payload fields, presented as a URL-encoded string. 
        Metadata posted to Slack is accessible to any app or user who is a member of that workspace.
        
        Example: {"event_type": "task_created", "event_payload": { "id": "11223", "title": "Redesign Homepage"}}
        """,
    )
    mrkdwn: Optional[StrictBool] = Field(
        default=None, description="Disable Slack markup parsing by setting to false. Enabled by default."
    )
    parse: Optional[StrictStr] = Field(
        default=None,
        description="""
        Change formatting behavior based on value for parse: 'none' or 'full'
        Defaults to 'full'.
        By default, URLs will be hyperlinked. Set parse to none to remove the hyperlinks.
        """,
    )
    reply_broadcast: Optional[StrictBool] = Field(
        default=None,
        description="""
        Used in conjunction with thread_ts and indicates whether reply should be made visible 
        to everyone in the channel or conversation. Defaults to false.
        """,
    )
    text: Optional[StrictStr] = Field(
        default=None,
        description="""
        The content of the message. The usage of the text field changes depending on whether you're using blocks.
        If you're using blocks, this is used as a fallback string to display in notifications. 
        If you aren't, this is the main body text of the message. It can be formatted as plain text, 
        or with the optional boolean argument mrkdwn.
        The text field is not enforced as required when using blocks or attachments. 
        """,
    )
    thread_ts: Optional[str] = Field(
        default=None,
        description="""
        ts=timestamp
        Timestamp of another message. Provide another message's ts value to make this message a reply. 
        Avoid using a reply's ts value; use its parent instead.
        
        Example: 1234567890.123456
        """,
    )
    unfurl_links: Optional[StrictBool] = Field(
        default=None, description="Pass true to enable unfurling of primarily text-based content."
    )
    unfurl_media: Optional[StrictBool] = Field(
        default=None, description="Pass false to disable unfurling of media content."
    )
    username: Optional[StrictStr] = Field(
        default=None, description="Set bot's user name."
    )  # TODO: Consider defaulting this to 'Neena'.


class SlackChatMessageSend(BaseIntegrationActionModel):
    """
    Action model for sending a message to a channel.
    """

    channel: StrictStr = Field(
        description="Channel, private group, or IM channel to send message to. Can be an encoded ID, or a name.",
    )
    text: Optional[StrictStr] = Field(
        default=None,
        description="""
        The content of the message. The usage of the text field changes depending on whether you're using blocks.
        If you're using blocks, this is used as a fallback string to display in notifications. 
        If you aren't, this is the main body text of the message. It can be formatted as plain text, 
        or with the optional boolean argument mrkdwn.
        The text field is not enforced as required when using blocks or attachments. 
        """,
    )
    as_user: Optional[StrictBool] = Field(
        default=None,
        description="(Legacy) Pass true to post the message as the authed user instead of as a bot. Defaults to false.",
    )
    attachments: Optional[StrictStr] = Field(
        default=None,
        description="""
        The message content in the form of a JSON-based array of structured attachments, 
        presented as a URL-encoded string.
        Example: [{"pretext": "pre-hello", "text": "text-world"}]
        """,
    )
    blocks: Optional[StrictStr] = Field(
        default=None,
        description="""
        The message content in the form of a JSON-based array of structured blocks, 
        presented as a URL-encoded string.
        Example: [{"type": "section", "text": {"type": "plain_text", "text": "Hello world"}}]
        """,
    )
    thread_ts: str = Field(
        default=None,
        description="""
        ts=timestamp
        Timestamp of another message. Provide another message's ts value to make this message a reply. 
        Avoid using a reply's ts value; use its parent instead.
        
        Example: 1234567890.123456
        """,
    )


class SlackChatMessageUpdate(BaseIntegrationActionModel):
    """
    Action model for updating a message.
    """

    channel: StrictStr = Field(
        description="""
        Channel, private group, or IM channel containing the message to be updated. Can be an encoded ID, or a name. 
        
        Example: C1234567890
        """,
    )
    message_ts: str = Field(
        description="""
        Timestamp of the message to be updated.
        
        Example: 1234567890.123456
        """,
    )
    text: StrictStr = Field(
        description="""
        The content of the message to be updated. The usage of the text field changes depending on whether you're using blocks.
        If you're using blocks, this is used as a fallback string to display in notifications. 
        If you aren't, this is the main body text of the message. It can be formatted as plain text, 
        or with the optional boolean argument mrkdwn.
        The text field is not enforced as required when using blocks or attachments. 
        """,
    )


class SlackChatMessageDelete(BaseIntegrationActionModel):
    """
    Action model for deleting a message.
    """

    channel: StrictStr = Field(
        description="""
        Channel, private group, or IM channel containing the message to be deleted. Can be an encoded ID, or a name. 
        
        Example: C1234567890
        """,
    )
    message_ts: str = Field(
        description="""
        Timestamp of the message to be deleted.
        
        Example: 1234567890.123456
        """,
    )


class SlackChatMessageGetPermalink(BaseIntegrationActionModel):
    """
    Action model for retrieving a permalink URL for a specific extant message.
    """


class SlackChatMessageSendMe(BaseIntegrationActionModel):
    """
    Action model for sending a me message into a channel.
    """


class SlackConversation(BaseAPIModel):
    """
    Slack API Conversation model.
    tl;dr: Conversations are about managing the broader contexts (channels,
    DMs, groups) where messages are sent.

    In the context of the Slack API, "conversation" refers to any channel,
    direct message, multi-party direct message, or private group.
    The conversations.* API methods are used to manage these conversation
    contexts themselves, not just the messages within them. For example, with
    conversations.* methods, you can create channels, archive channels,
    invite users to a conversation, or fetch a list of conversations a user is
    a part of. It's about managing the spaces where chats can happen rather
    than the chat messages themselves.
    """

    pass


class SlackAdmin(BaseAPIModel):
    """
    Slack API Admin model.
    """

    pass


class SlackTeam(BaseAPIModel):
    """
    Slack API Team model.
    """

    pass


class SlackUsers(BaseAPIModel):
    """
    Slack API Users model.
    """

    pass


class SlackUsergroups(BaseAPIModel):
    """
    Slack API Usergroups model.
    """

    pass


class SlackViews(BaseAPIModel):
    """
    Slack API Views model.
    """

    pass


class SlackReminders(BaseAPIModel):
    """
    Slack API Reminders model.
    """

    pass


class SlackApps(BaseAPIModel):
    """
    Slack API Apps model.
    """

    pass


class SlackFiles(BaseAPIModel):
    """
    Slack API Files model.
    """

    pass
