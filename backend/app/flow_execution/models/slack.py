from pydantic.fields import Field
from datetime import datetime, date
from typing import Optional, Union, Sequence, Any

# from slack_sdk.models.metadata import Metadata
from pydantic import StrictBool, StrictStr, StrictInt, root_validator

from app.flow_execution.models.base import BaseAPIModel, BaseIntegrationActionModel


class BaseSlackResponse(BaseAPIModel):
    """
    Base model for Slack API responses. All Slack API responses should inherit from this model.
    """

    ok: bool = Field(description="Indicates the success of the API call.")
    error: Optional[StrictStr] = Field(default=None, description="Error message if the API call was unsuccessful.")
    warning: Optional[StrictStr] = Field(
        default=None, description="Warning message if the API call was successful but with warnings."
    )
    response_metadata: Optional[dict] = Field(default=None, description="Metadata about the response.")


class SlackChatSendMessageResponse(BaseSlackResponse):
    """
    Response model for the chat.postMessage Slack API method.
    """

    channel: Optional[StrictStr] = Field(default=None, description="ID of the channel the message was posted in.")
    ts: Optional[StrictStr] = Field(default=None, description="Timestamp of the message.")
    message: Optional[dict] = Field(default=None, description="The message that was posted.")


class SlackChatUpdateMessageResponse(BaseSlackResponse):
    """
    Response model for the chat.update Slack API method.
    """

    channel: Optional[StrictStr] = Field(default=None, description="Channel containing the updated message.")
    ts: Optional[StrictStr] = Field(default=None, description="Timestamp of the updated message.")
    text: Optional[StrictStr] = Field(default=None, description="Content of the message.")
    message: Optional[dict] = Field(default=None, description="The updated message and corresponding user.")


class SlackChatDeleteMessageResponse(BaseSlackResponse):
    """
    Response model for the chat.delete Slack API method.
    """

    channel: Optional[StrictStr] = Field(default=None, description="Channel containing the deleted message.")
    ts: Optional[StrictStr] = Field(default=None, description="Timestamp of the deleted message.")


class SlackChatScheduleMessageResponse(BaseSlackResponse):
    """
    Response model for the chat.scheduleMessage Slack API method.
    """

    channel: Optional[StrictStr] = Field(
        default=None, description="Channel, private group, or DM channel the message was scheduled to be sent to."
    )
    scheduled_message_id: Optional[StrictStr] = Field(default=None, description="ID of the scheduled message.")
    post_at: Optional[StrictStr] = Field(
        default=None, description="Unix timestamp representing the future time the message should post to Slack."
    )
    message: Optional[dict] = Field(default=None, description="The scheduled message and its metadata.")


class SlackChatGetPermalinkResponse(BaseSlackResponse):
    """
    Response model for the chat.getPermalink Slack API method.
    """

    channel: Optional[StrictStr] = Field(
        default=None, description="ID of the conversation or channel containing the message."
    )
    permalink: Optional[StrictStr] = Field(default=None, description="Permalink URL.")


class SlackChatSendMeMessageResponse(BaseSlackResponse):
    """
    Response model for the chat.meMessage Slack API method.
    """

    channel: Optional[StrictStr] = Field(default=None, description="ID of the channel the Me message was posted in.")
    ts: Optional[StrictStr] = Field(default=None, description="Timestamp of the posted Me message.")


class SlackConversationsCreateResponse(BaseSlackResponse):
    """
    Response model for the conversations.create Slack API method.
    """

    channel: Optional[dict] = Field(default=None, description="Created channel ID and its metadata.")


class SlackConversationsHistoryResponse(BaseSlackResponse):
    """
    Response model for the conversations.history Slack API method.
    """

    latest: Optional[StrictStr] = Field(
        default=None, description="Unix timestamp of latest message in conversation history."
    )
    messages: Optional[dict] = Field(default=None, description="Conversation's messages.")
    has_more: Optional[bool] = Field(
        default=None, description="Boolean indicating whether conversation has more messages than those returned."
    )
    pin_count: Optional[int] = Field(
        default=None, description="The number of messages that have been pinned in the conversation"
    )
    response_metadata: Optional[dict] = Field(default=None, description="Metadata about the response.")


class SlackConversationsInfoResponse(BaseSlackResponse):
    """
    Response model for the conversations.info Slack API method.
    """

    channel: Optional[dict] = Field(default=None, description="Channel ID and its metadata.")


class SlackConversationsInviteResponse(BaseSlackResponse):
    """
    Response model for the conversations.invite Slack API method.
    """

    channel: Optional[dict] = Field(default=None, description="Channel ID and its metadata.")


class SlackConversationsJoinResponse(BaseSlackResponse):
    """
    Response model the conversations.join Slack API method.
    """

    channel: Optional[dict] = Field(default=None, description="Channel ID and its metadata.")
    warning: Optional[str] = Field(
        default=None, description="Warning message indicating, e.g., whether already in channel."
    )
    response_metadata: Optional[dict] = Field(default=None, description="Metadata about the response.")


class SlackConversationsListResponse(BaseSlackResponse):
    """
    Response model for the conversations.list Slack API method.
    """

    channel: Optional[list[dict]] = Field(default=None, description="Channels and their metadata.")
    response_metadata: Optional[dict] = Field(default=None, description="Metadata about the response.")


class SlackConversationsMembersResponse(BaseSlackResponse):
    """
    Response model for the conversations.members Slack API method.
    """

    members: Optional[list[StrictStr]] = Field(default=None, description="List of member IDs in conversation.")
    response_metadata: Optional[dict] = Field(default=None, description="Metadata about the response.")


class SlackConversationsOpenResponse(BaseSlackResponse):
    """
    Response model for the conversations.open Slack API method.
    """

    channel: Optional[dict] = Field(default=None, description="Channel ID and its metadata.")
    no_op: Optional[bool] = Field(
        default=None,
        description="""
        No operation; boolean indicating that the conversations.open method was called, but no action was taken because 
        the requested operation was not needed. This is likely because the direct message or multi-person direct message 
        that was attempted to be opened or resumed was already open.
        """,
    )
    already_open: Optional[bool] = Field(
        default=None, description="Boolean indicating whether conversation was already open."
    )


class SlackConversationsRenameResponse(BaseSlackResponse):
    """
    Response model for the conversations.rename Slack API method.
    """

    channel: Optional[dict] = Field(default=None, description="Channel ID and its metadata.")


class SlackConversationsRepliesResponse(BaseSlackResponse):
    """
    Response model for the conversations.replies Slack API method.
    """

    messages: Optional[dict] = Field(default=None, description="Conversation's messages.")
    has_more: Optional[bool] = Field(
        default=None, description="Boolean indicating whether conversation has more messages than those returned."
    )
    response_metadata: Optional[dict] = Field(default=None, description="Metadata about the response.")


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

    TODO: This base API model for Slack Chat methods is currently unused. Find generalizable use for it, or remove it.
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
    metadata: Optional[Union[dict, Any]] = Field(
        # TODO: type hint Any should actually be slack_sdk.models.metadata.Metadata
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
    post_at: Optional[Union[StrictStr, StrictInt]] = Field(
        default=None,
        description="""
        Unix timestamp representing the future time the message should post to Slack.
        
        Example: 299876400
        """,
    )
    reply_broadcast: Optional[StrictBool] = Field(
        default=None,
        description="""
        Used in conjunction with thread_ts and indicates whether reply should be made visible 
        to everyone in the channel or conversation. Defaults to false.
        """,
    )
    scheduled_message_id: Optional[str] = Field(
        default=None,
        description="""
        scheduled_message_id returned from call to chat.scheduleMessage (Slack Web API method), i.e., SlackChatMessageSchedule (Neena action model)
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
    username: Optional[StrictStr] = Field(default=None, description="Set bot's user name.")


class SlackChatSendMessageAction(BaseIntegrationActionModel):
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
    thread_ts: Optional[str] = Field(
        default=None,
        description="""
        ts=timestamp
        Timestamp of another message. Provide another message's ts value to make this message a reply. 
        Avoid using a reply's ts value; use its parent instead.
        
        Example: 1234567890.123456
        """,
    )

    @root_validator(pre=True)
    def check_at_least_one_field(cls, values):
        if not any(values.get(field) for field in ("text", "attachments", "blocks")):
            raise ValueError("At least one of text, attachments, or blocks must be provided.")
        return values


class SlackChatUpdateMessageAction(BaseIntegrationActionModel):
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
    text: Optional[StrictStr] = Field(
        description="""
        The content of the message to be updated. The usage of the text field changes depending on whether you're using blocks.
        If you're using blocks, this is used as a fallback string to display in notifications. 
        If you aren't, this is the main body text of the message. It can be formatted as plain text, 
        or with the optional boolean argument mrkdwn.
        The text field is not enforced as required when using blocks or attachments. 
        """,
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

    @root_validator(pre=True)
    def check_at_least_one_field(cls, values):
        if not any(values.get(field) for field in ("text", "attachments", "blocks")):
            raise ValueError("At least one of text, attachments, or blocks must be provided.")
        return values


class SlackChatDeleteMessageAction(BaseIntegrationActionModel):
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


class SlackChatDeleteScheduledMessageAction(BaseIntegrationActionModel):
    """
    Action model for deleting a pending scheduled message from the queue.
    """

    channel: StrictStr = Field(
        description="""
        The channel the scheduled_message is posting to. Can be an encoded ID, or a name. 
        
        Example: C1234567890
        """,
    )
    scheduled_message_id: str = Field(
        description="""
        scheduled_message_id returned from call to chat.scheduleMessage (Slack Web API method), i.e., SlackChatMessageSchedule (Neena action model)

        Example: Q1234ABCD
        """,
    )
    as_user: Optional[StrictBool] = Field(
        default=None,
        description="""
        Pass true to delete the message as the authed user with chat:write:user scope. Bot users in this context are considered authed users. If unused or false, the message will be deleted with chat:write:bot scope
        """,
    )


class SlackChatScheduleMessageAction(BaseIntegrationActionModel):
    """
    Action model for scheduling a message to be sent.
    """

    channel: StrictStr = Field(
        description="""
        Channel, private group, or IM channel containing the message to be scheduled for sending. 
        Can be an encoded ID, or a name. 
        
        Example: C1234567890
        """,
    )
    post_at: Union[StrictStr, StrictInt] = Field(
        description="""
        Unix timestamp representing the future time the message should post to Slack.
        
        Example: 299876400
        """,
    )
    text: Optional[StrictStr] = Field(
        default=None,
        description="""
        The content of the message to be sent. The usage of the text field changes depending on whether you're using blocks.
        If you're using blocks, this is used as a fallback string to display in notifications. 
        If you aren't, this is the main body text of the message. It can be formatted as plain text, 
        or with the optional boolean argument mrkdwn.
        The text field is not enforced as required when using blocks or attachments. 
        """,
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

    @root_validator(pre=True)
    def check_at_least_one_field(cls, values):
        if not any(values.get(field) for field in ("text", "attachments", "blocks")):
            raise ValueError("At least one of text, attachments, or blocks must be provided.")
        return values


class SlackChatGetPermalinkAction(BaseIntegrationActionModel):
    """
    Action model for retrieving a permalink URL for a specific extant message.
    """

    channel: StrictStr = Field(
        description="""
        Channel, private group, or IM channel containing the message. 
        Can be an encoded ID, or a name. 
        
        Example: C1234567890
        """,
    )
    message_ts: str = Field(
        description="""
        Timestamp of the message, uniquely identifying it within a channel.
        
        Example: 1234567890.123456
        """,
    )


class SlackChatSendMeMessageAction(BaseIntegrationActionModel):
    """
    Action model for sharing a me message into a channel.
    """

    channel: StrictStr = Field(
        description="""
        Channel to send message to. Can be a public channel, private group or IM channel. Can be an encoded ID, or a name.
        
        Example: C1234567890
        """,
    )
    text: StrictStr = Field(
        default=None,
        description="""
        The content of the message to be sent.

        Example: Hello world
        """,
    )


class SlackConversations(BaseAPIModel):
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

    TODO: This base API model for Slack Conversation methods is currently unused. Find generalizable use for it, or remove it.
    """

    channel: Optional[StrictStr] = Field(default=None, description="ID of a channel.")
    cursor: Optional[StrictStr] = Field(
        default=None,
        description="""
        Paginate through collections of data by setting the cursor parameter to 
        a next_cursor attribute returned by a previous request's response_metadata. 
        Default value fetches the first "page" of the collection

        Example: dXNlcjpVMDYxTkZUVDI=
        """,
    )
    exclude_archived: Optional[StrictBool] = Field(
        default=None,
        description="""
        When listing conversations, set to True to exclude archived channels from the list. Default: False
        """,
    )
    force: Optional[StrictBool] = Field(
        default=None,
        description="""
        When inviting users to a channel, force set to True, and multiple user IDs are provided, 
        continue inviting the valid user IDs while disregarding invalid IDs. 
        Defaults to False.
        """,
    )
    include_all_metadata: Optional[StrictStr] = Field(
        default=None, description="Boolean indicating whether to return all metadata associated with a message or not."
    )
    include_locale: Optional[StrictBool] = Field(
        default=None,
        description="""
        When fetching conversation information, set this to True to receive the locale for this conversation. 
        Defaults to False.
        """,
    )
    include_num_members: Optional[StrictBool] = Field(
        default=None,
        description="""
        When fetching conversation information, set to True to include the member count for the specified conversation. 
        Defaults to False.
        """,
    )
    inclusive: Optional[StrictBool] = Field(
        default=None,
        description="""
        Boolean indicating whether to include messages with oldest or latest timestamps in results when fetching conversation history. 
        Ignored unless either timestamp (latest or oldest) is specified.
        """,
    )
    is_private: Optional[StrictBool] = Field(
        default=None, description="Boolean indicating whether a channel private (True) or public (False)"
    )
    latest: Optional[StrictStr] = Field(
        default=None,
        description="""
        When fetching conversation history, only messages before this Unix timestamp will be included in results. 
        Default is the current time.
        """,
    )
    limit: Optional[StrictInt] = Field(
        default=None,
        description="""
        The maximum number of items to return when fetching conversations history. 
        Fewer than the requested number of items may be returned, 
        even if the end of the conversation history hasn't been reached. Maximum of 999.

        Default: 100
        """,
    )
    name: Optional[StrictStr] = Field(default=None, description="Name of the public or private channel.")
    oldest: Optional[StrictStr] = Field(
        default=None,
        description="""
        When fetching conversation history, only messages after this Unix timestamp will be included in results.

        Default: 0

        Example: 1234567890.123456
        """,
    )
    prevent_creation: Optional[StrictBool] = Field(
        default=None,
        description="""
        When resuming a direct message (dm) or multi-person direct message (mpdm), 
        do not create a dm or mpdm. 
        This is used to see if there is an existing dm or mpdm.
        """,
    )
    return_im: Optional[StrictBool] = Field(
        default=None,
        description="""
        When opening or resuming a direct message or multi-person direct message, 
        this boolean indicates you want the full IM channel definition in the response.
        """,
    )
    team_id: Optional[StrictStr] = Field(
        default=None, description="encoded team id to create the channel in, required if org token is used"
    )
    types: Optional[Union[StrictStr, Sequence[StrictStr]]] = Field(
        default=None,
        description="""
        Mix and match channel types by providing a comma-separated list of any combination of public_channel, 
        private_channel, mpim, im.

        Default: public_channel

        Example: public_channel,private_channel
        """,
    )
    users: Optional[Union[StrictStr, Sequence[StrictStr]]] = Field(
        default=None,
        description="""
        A comma separated list of user IDs. Up to 1000 users may be listed.

        Example: W1234567890,U2345678901,U3456789012
        """,
    )


class SlackConversationsAcceptSharedInviteAction(BaseIntegrationActionModel):
    """
    Action model for accepting an invitation to a Slack Connect channel.
    """


class SlackConversationsApproveSharedInviteAction(BaseIntegrationActionModel):
    """
    Action model for approving an invitation to a Slack Connect channel.
    """


class SlackConversationsArchiveAction(BaseIntegrationActionModel):
    """
    Action model for archiving a conversation.
    """

    channel: StrictStr = Field(description="ID of conversation to archive. Example: C1234567890")


class SlackConversationsCloseAction(BaseIntegrationActionModel):
    """
    Action model for closing a direct message or multi-person direct message.
    """

    channel: StrictStr = Field(description="Conversation to close.")


class SlackConversationsCreateAction(BaseIntegrationActionModel):
    """
    Action model for initiating a public or private channel-based conversation/
    """

    name: StrictStr = Field(description="Name of the public or private channel to create. Example: mychannel")
    is_private: Optional[StrictBool] = Field(
        default=None, description="Create a private channel instead of a public one"
    )
    team_id: Optional[StrictStr] = Field(
        default=None, description="""encoded team id to create the channel in, required if org token is used"""
    )


class SlackConversationsDeclineSharedInviteAction(BaseIntegrationActionModel):
    """
    Action model for declining a Slack Connect channel invite.
    """


class SlackConversationsHistoryAction(BaseIntegrationActionModel):
    """
    Action model for fetching a conversation's history of messages and events.
    """

    channel: StrictStr = Field(description="Conversation ID to fetch history for.")
    include_all_metadata: Optional[StrictBool] = Field(
        default=None, description="Return all metadata associated with this message."
    )
    inclusive: Optional[StrictBool] = Field(
        default=None,
        description="Include messages with oldest or latest timestamps in results. Ignored unless either timestamp is specified.",
    )
    latest: Optional[StrictStr] = Field(
        default=None,
        description="""Only messages before this Unix timestamp will be included in results. Default is the current time.""",
    )
    limit: Optional[StrictInt] = Field(
        default=None,
        description="""
        The maximum number of items to return. Fewer than the requested number of items may be returned, 
        even if the end of the conversation history hasn't been reached. Maximum of 999.

        Default: 100
        """,
    )
    oldest: Optional[StrictStr] = Field(
        default=None,
        description="""
        Only messages after this Unix timestamp will be included in results.

        Default: 0

        Example: 1234567890.123456
        """,
    )


class SlackConversationsInfoAction(BaseIntegrationActionModel):
    """
    Retrieve information about a conversation.
    """

    channel: StrictStr = Field(description="Conversation ID to fetch information about.")
    include_locale: Optional[StrictBool] = Field(
        default=None, description="Set this to True to receive the locale for this conversation. Defaults to False"
    )
    include_num_members: Optional[StrictBool] = Field(
        default=None,
        description="Set to true to include the member count for the specified conversation. Defaults to false",
    )


class SlackConversationsInviteAction(BaseIntegrationActionModel):
    """
    Invites users to a channel.
    """

    channel: StrictStr = Field(description="ID of the public or private to invite(s) user to.")
    users: Union[StrictStr, Sequence[StrictStr]] = Field(
        description="""
        A comma separated list of user IDs. Up to 1000 users may be listed.

        Example: W1234567890,U2345678901,U3456789012
        """
    )
    force: Optional[StrictBool] = Field(
        default=None,
        description="""
        When set to True and multiple user IDs are provided, 
        continue inviting the valid ones while disregarding invalid IDs. 
        Defaults to False.
        """,
    )


class SlackConversationsInviteSharedAction(BaseIntegrationActionModel):
    """
    Action model for sending an invitation to a Slack Connect channel.
    """


class SlackConversationsJoinAction(BaseIntegrationActionModel):
    """
    Action model for joining an existing conversation.
    """

    channel: StrictStr = Field(description="ID of the public or private to join.")


class SlackConversationsKickAction(BaseIntegrationActionModel):
    """
    ...
    """


class SlackConversationsLeaveAction(BaseIntegrationActionModel):
    """
    ...
    """


class SlackConversationsListAction(BaseIntegrationActionModel):
    """
    Action model for listing all channels in a Slack team.
    """

    cursor: Optional[StrictStr] = Field(
        default=None,
        description="""
        Paginate through collections of data by setting the cursor parameter to 
        a next_cursor attribute returned by a previous request's response_metadata. 
        Default value fetches the first "page" of the collection

        Example: dXNlcjpVMDYxTkZUVDI=
        """,
    )
    exclude_archived: Optional[StrictBool] = Field(
        default=None, description="Set to True to exclude archived channels from the list. Default: False"
    )
    limit: Optional[StrictInt] = Field(
        default=None,
        description="""
        The maximum number of items to return. Fewer than the requested number of items may be returned, 
        even if the end of the list hasn't been reached. Must be an integer under 1000.

        Default: 100
        """,
    )
    team_id: Optional[StrictStr] = Field(
        default=None,
        description="""
        Encoded team id to list channels in, required if token belongs to org-wide app.

        Example: T1234567890
        """,
    )
    types: Optional[Union[StrictStr, Sequence[StrictStr]]] = Field(
        default=None,
        description="""
        Mix and match channel types by providing a comma-separated list of any combination of public_channel, 
        private_channel, mpim, im.

        Default: public_channel

        Example: public_channel,private_channel
        """,
    )


class SlackConversationsListConnectInvitesAction(BaseIntegrationActionModel):
    """
    Action model for listing shared channel invites that have been generated
    or received but have not yet been approved by all parties.
    """


class SlackConversationsMarkAction(BaseIntegrationActionModel):
    """
    Action model for setting the read cursor in a channel.
    """


class SlackConversationsMembersAction(BaseIntegrationActionModel):
    """
    Action model for retrieving members of a conversation.
    """

    channel: StrictStr = Field(description="ID of the conversation to retrieve members for.")
    cursor: Optional[StrictStr] = Field(
        default=None,
        description="""
        Paginate through collections of data by setting the cursor parameter to 
        a next_cursor attribute returned by a previous request's response_metadata. 
        Default value fetches the first "page" of the collection

        Example: dXNlcjpVMDYxTkZUVDI=
        """,
    )
    limit: Optional[StrictInt] = Field(
        default=None,
        description="""
        The maximum number of items to return. Fewer than the requested number of items may be returned, 
        even if the end of the list hasn't been reached. Must be an integer under 1000.

        Default: 100
        """,
    )


class SlackConversationsOpenAction(BaseIntegrationActionModel):
    """
    Action model for opening or resuming a direct message or multi-person direct message.
    """

    channel: Optional[StrictStr] = Field(
        description="""Resume a conversation by supplying an im or mpim's ID. Or provide the users field instead."""
    )
    prevent_creation: Optional[StrictBool] = Field(
        default=None,
        description="""
        Do not create a direct message or multi-person direct message. 
        This is used to see if there is an existing dm or mpdm.
        """,
    )
    return_im: Optional[StrictBool] = Field(
        default=None, description="""Boolean, indicates you want the full IM channel definition in the response."""
    )
    users: Optional[Union[StrictStr, Sequence[StrictStr]]] = Field(
        default=None,
        description="""
        Comma separated lists of users. If only one user is included, 
        this creates a 1:1 DM. The ordering of the users is preserved whenever a multi-person direct message is returned. 
        Supply a channel when not supplying users.

        Example: W1234567890,U2345678901,U3456789012
        """,
    )


class SlackConversationsRenameAction(BaseIntegrationActionModel):
    """
    Action model for renaming a conversation.
    """

    channel: StrictStr = Field(description="ID of conversation to rename.")
    name: StrictStr = Field(description="New name for conversation.")


class SlackConversationsRepliesAction(BaseIntegrationActionModel):
    """
    Action model for retrieving a thread of messages posted to a conversation.
    """

    channel: StrictStr = Field(description="Conversation ID to fetch thread from.")
    ts: StrictStr = Field(
        description="""
        Unique identifier of either a thread's parent message or a message in the thread. 
        ts must be the timestamp of an existing message with 0 or more replies. 
        If there are no replies then just the single message referenced by ts will return - it is just an ordinary, 
        unthreaded message.

        Example: 1234567890.123456
        """
    )
    cursor: Optional[StrictStr] = Field(
        default=None,
        description="""
        Paginate through collections of data by setting the cursor parameter to 
        a next_cursor attribute returned by a previous request's response_metadata. 
        Default value fetches the first "page" of the collection

        Example: dXNlcjpVMDYxTkZUVDI=
        """,
    )
    include_all_metadata: Optional[StrictBool] = Field(
        default=None, description="Return all metadata associated with this message."
    )
    inclusive: Optional[StrictBool] = Field(
        default=None,
        description="Include messages with oldest or latest timestamps in results. Ignored unless either timestamp is specified.",
    )
    latest: Optional[StrictStr] = Field(
        default=None,
        description="""Only messages before this Unix timestamp will be included in results. Default: now""",
    )
    limit: Optional[StrictInt] = Field(
        default=None,
        description="""
        The maximum number of items to return. Fewer than the requested number of items may be returned, 
        even if the end of the conversation history hasn't been reached. Maximum of 999.

        Default: 100
        """,
    )
    oldest: Optional[StrictStr] = Field(
        default=None,
        description="""
        Only messages after this Unix timestamp will be included in results.

        Default: 0

        Example: 1234567890.123456
        """,
    )


class SlackConversationsSetPurposeAction(BaseIntegrationActionModel):
    """
    Action model for setting the purpose for a conversation.
    """


class SlackConversationsSetTopicAction(BaseIntegrationActionModel):
    """
    Action model for setting the topic for a conversation.
    """


class SlackConversationsUnarchiveAction(BaseIntegrationActionModel):
    """
    Action model for reversing conversation archival.
    """


class SlackAdmin(BaseAPIModel):
    """
    Slack API Admin model.
    """


class SlackTeam(BaseAPIModel):
    """
    Slack API Team model.
    """


class SlackUsers(BaseAPIModel):
    """
    Slack API Users model.
    """


class SlackUsergroups(BaseAPIModel):
    """
    Slack API Usergroups model.
    """


class SlackViews(BaseAPIModel):
    """
    Slack API Views model.
    """


class SlackReminders(BaseAPIModel):
    """
    Slack API Reminders model.
    """


class SlackApps(BaseAPIModel):
    """
    Slack API Apps model.
    """


class SlackFiles(BaseAPIModel):
    """
    Slack API Files model.
    """
