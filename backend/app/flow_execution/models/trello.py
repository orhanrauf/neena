from ctypes import Union
from dataclasses import Field
from datetime import datetime, date
import json
from typing import Annotated, Any, List, Optional

from pydantic import StrictBool, StrictFloat, StrictInt, StrictStr

from app.flow_execution.models.base import BaseAPIModel, BaseIntegrationActionModel


class TrelloCard(BaseAPIModel):
    """
    Trello API Card model.
    """ # noqa: E501
    id: Annotated[Optional[str], Field(strict=True, description="Unique identifier of the card")] = None
    address: Annotated[Optional[StrictStr], Field(description="Address of the card, if applicable")] = None
    closed: Annotated[Optional[StrictBool], Field(description="Whether the card is archived/closed")] = None
    coordinates: Annotated[Optional[StrictStr], Field(description="Coordinates of the card, if applicable")] = None
    creation_method: Annotated[Optional[StrictStr], Field(description="Method used for card creation", alias="creationMethod")] = None
    date_last_activity: Annotated[Optional[datetime], Field(description="Last activity date of the card", alias="dateLastActivity")] = None
    desc: Annotated[Optional[StrictStr], Field(description="Description of the card")] = None
    due: Annotated[Optional[date], Field(description="Due date of the card")] = None
    due_reminder: Annotated[Optional[StrictStr], Field(description="Reminder setting for the due date", alias="dueReminder")] = None
    email: Annotated[Optional[StrictStr], Field(description="Email associated with the card")] = None
    id_board: Annotated[Optional[str], Field(description="ID of the board the card belongs to", strict=True, alias="idBoard")] = None
    id_list: Annotated[Optional[str], Field(description="ID of the list the card belongs to", strict=True, alias="idList")] = None
    id_short: Annotated[Optional[StrictInt], Field(description="Short identifier for the card", alias="idShort")] = None
    id_attachment_cover: Annotated[Optional[str], Field(description="ID of the cover attachment", strict=True, alias="idAttachmentCover")] = None
    location_name: Annotated[Optional[StrictStr], Field(description="Name of the location associated with the card", alias="locationName")] = None
    manual_cover_attachment: Annotated[Optional[StrictBool], Field(description="Whether the cover attachment is set manually", alias="manualCoverAttachment")] = None
    name: Annotated[Optional[StrictStr], Field(description="Name of the card")] = None
    pos: Annotated[Optional[Union[StrictFloat, StrictInt]], Field(description="Position of the card in the list")] = None
    short_link: Annotated[Optional[StrictStr], Field(description="Short link for the card", alias="shortLink")] = None
    short_url: Annotated[Optional[StrictStr], Field(description="Short URL for the card", alias="shortUrl")] = None
    subscribed: Annotated[Optional[StrictBool], Field(description="Whether the user is subscribed to the card")] = None
    url: Annotated[Optional[StrictStr], Field(description="URL of the card")] = None

class TrelloCardCreate(BaseIntegrationActionModel):
    """
    Model for creating a new Card.
    """
    id_list: Annotated[str, Field(strict=True, description="The ID of the list the card should be created in")]
    name: Annotated[StrictStr, Field(description="The name for the card")] 
    desc: Annotated[Optional[StrictStr], Field(description="The description for the card")] = None
    pos: Annotated[Optional[Any], Field(description="The position of the new card. `top`, `bottom`, or a positive float")] = None
    due: Annotated[Optional[date], Field(description="A due date for the card")] = None,
    start: Annotated[Optional[date], Field(description="The start date of a card, or `null`")] = None
    id_labels: Annotated[Optional[List[str]], Field(description="Comma-separated list of label IDs to add to the card")] = None
    
class TrelloCardGet(BaseAPIModel):
    id: Annotated[str, Field(strict=True, description="The ID of the list the card should be created in")]

class TrelloCardUpdate(BaseIntegrationActionModel):
    """
    Model for updating an existing Card.
    """
    id: Annotated[str, Field(strict=True, description="The ID of the Card")],
    name: Annotated[Optional[StrictStr], Field(description="The new name for the card")] = None
    desc: Annotated[Optional[StrictStr], Field(description="The new description for the card")] = None
    closed: Annotated[Optional[StrictBool], Field(description="Whether the card should be archived (closed: true)")] = None
    id_members: Annotated[Optional[Annotated[str, Field(strict=True)]], Field(description="Comma-separated list of member IDs")] = None
    id_attachment_cover: Annotated[Optional[Annotated[str, Field(strict=True)]], Field(description="The ID of the image attachment the card should use as its cover, or null for none")] = None
    id_list: Annotated[Optional[Annotated[str, Field(strict=True)]], Field(description="The ID of the list the card should be in")] = None
    id_labels: Annotated[Optional[Annotated[str, Field(strict=True)]], Field(description="Comma-separated list of label IDs")] = None
    pos: Annotated[Optional[Any], Field(description="The position of the card in its list. `top`, `bottom`, or a positive float")] = None
    due: Annotated[Optional[date], Field(description="When the card is due, or `null`")] = None
    start: Annotated[Optional[date], Field(description="The start date of a card, or `null`")] = None,
    due_complete: Annotated[Optional[StrictBool], Field(description="Whether the due date should be marked complete")] = None
    subscribed: Annotated[Optional[StrictBool], Field(description="Whether the member is should be subscribed to the card")] = None
    address: Annotated[Optional[StrictStr], Field(description="For use with/by the Map View")] = None
    location_name: Annotated[Optional[StrictStr], Field(description="For use with/by the Map View")] = None
    coordinates: Annotated[Optional[StrictStr], Field(description="For use with/by the Map View. Should be latitude,longitude")] = None
    
class TrelloCardDelete(BaseIntegrationActionModel):
    """
    Model for deleting an existing Card.
    """
    id: Annotated[str, Field(strict=True, description="The ID of the Card")]
    
class TrelloList(BaseAPIModel):
    """
    Trello API List model.
    """
    id: Annotated[Optional[str], Field(strict=True)] = None
    name: Annotated[Optional[StrictStr], Field(default=None, description="The name of the list")] = None
    closed: Annotated[Optional[StrictBool], Field(strict=True)] = None
    pos: Annotated[Optional[Union[StrictFloat, StrictInt]], Field(strict=True)] = None
    soft_limit: Annotated[Optional[StrictStr], Field(default=None, alias="softLimit")] = None
    id_board: Annotated[Optional[StrictStr], Field(default=None, alias="idBoard")] = None
    subscribed: Annotated[Optional[StrictBool], Field(strict=True)] = None


    

class TrelloListCreate(BaseIntegrationActionModel):
    """
    Model for creating a new Trello List.
    """
    name: Annotated[StrictStr, Field(description="The name for the list")]
    id_board: Annotated[str, Field(strict=True, description="The ID of the board the list should be created in")]
    pos: Annotated[Optional[Union[StrictFloat, StrictInt]], Field(description="Position of the list in the board. `top`, `bottom`, or a positive float")] = None

class TrelloListGet(BaseIntegrationActionModel):
    """
    Model for retrieving details of a specific Trello List.
    """
    id: Annotated[str, Field(strict=True, description="The ID of the List to retrieve")]

class TrelloListUpdate(BaseIntegrationActionModel):
    
    id: Annotated[StrictStr, Field(description="The ID of the list")]
    name: Annotated[Optional[StrictStr], Field(description="New name for the list")] = None
    closed: Annotated[Optional[StrictBool], Field(description="Whether the list should be closed (archived)")] = None
    id_board: Annotated[Optional[Annotated[str, Field(strict=True)]], Field(description="ID of a board the list should be moved to")] = None
    pos: Annotated[Optional[Any], Field(description="New position for the list: `top`, `bottom`, or a positive floating point number")] = None

class TrelloBoard(BaseAPIModel):
    """
    Trello API Card model.
    """
    
    id: Annotated[str, Field(strict=True, description="The ID of the board.")]
    name: Annotated[Optional[StrictStr], Field(description="The new name of the board")] = None
    desc: Annotated[Optional[StrictStr], Field(description="The new description of the board")] = None
    desc_data: Annotated[Optional[StrictStr], Field(description="The new descData of the board", alias="descData")] = None
    closed: Annotated[Optional[StrictBool], Field(description="Whether the board should be closed/archived")] = None
    id_member_creator: Annotated[Optional[Annotated[str, Field(strict=True)]], Field(description="The new idMemberCreator of the board", alias="idMemberCreator")] = None
    id_organization: Annotated[Optional[Annotated[str, Field(strict=True)]], Field(description="The new idOrganization of the board", alias="idOrganization")] = None
    pinned: Annotated[Optional[StrictBool], Field(description="Whether the board should be pinned")] = None
    url: Annotated[Optional[StrictStr], Field(description="The new url of the board")] = None
    short_url: Annotated[Optional[StrictStr], Field(description="The new shortUrl of the board", alias="shortUrl")] = None
    starred: Annotated[Optional[StrictBool], Field(description="Whether the board should be starred")] = None
    memberships: Annotated[Optional[StrictStr], Field(description="The new memberships of the board")] = None
    short_link: Annotated[Optional[StrictStr], Field(description="The new shortLink of the board", alias="shortLink")] = None
    subscribed: Annotated[Optional[StrictBool], Field(description="Whether the user is subscribed to the board")] = None
    power_ups: Annotated[Optional[StrictStr], Field(description="The new powerUps of the board", alias="powerUps")] = None
    date_last_activity: Annotated[Optional[date], Field(description="The new dateLastActivity of the board", alias="dateLastActivity")] = None
    date_last_view: Annotated[Optional[date], Field(description="The new dateLastView of the board", alias="dateLastView")] = None
    id_tags: Annotated[Optional[StrictStr], Field(description="The new idTags of the board", alias="idTags")] = None
    date_plugin_disable: Annotated[Optional[date], Field(description="The new datePluginDisable of the board", alias="datePluginDisable")] = None
    creation_method: Annotated[Optional[StrictStr], Field(description="The new creationMethod of the board", alias="creationMethod")] = None
    ix_update: Annotated[Optional[StrictInt], Field(description="The new ixUpdate of the board", alias="ixUpdate")] = None
    template_gallery: Annotated[Optional[StrictStr], Field(description="The new templateGallery of the board", alias="templateGallery")] = None
    enterprise_owned: Annotated[Optional[StrictBool], Field(description="Whether the board is enterprise owned", alias="enterpriseOwned")] = None

class TrelloBoardCreate(BaseIntegrationActionModel):
    """
    Model for creating a new Trello Board.
    """
    name: Annotated[str, Field(min_length=1, strict=True, max_length=16384, description="The new name for the board.")]
    default_labels: Annotated[Optional[StrictBool], Field(description="Determines whether to use the default set of labels.")] = None
    default_lists: Annotated[Optional[StrictBool], Field(description="Determines whether to add the default set of lists to a board (To Do, Doing, Done).")] = None
    desc: Annotated[Optional[Annotated[str, Field(min_length=0, strict=True, max_length=16384)]], Field(description="A new description for the board, 0 to 16384 characters long")] = None
    
class TrelloBoardGet(BaseIntegrationActionModel):
    """
    Model for retrieving details of a specific Trello Board.
    """
    id: Annotated[str, Field(strict=True, description="The ID of the board to retrieve")]

class TrelloBoardUpdate(BaseIntegrationActionModel):
    """
    Model for updating an existing Trello Board.
    """
    id: Annotated[str, Field(strict=True)]
    name: Annotated[Optional[StrictStr], Field(description="The new name for the board.")] = None
    desc: Annotated[Optional[StrictStr], Field(description="A new description for the board, 0 to 16384 characters long")] = None
    closed: Annotated[Optional[StrictBool], Field(description="Whether the board is closed")] = None

class TrelloBoardDelete(BaseIntegrationActionModel):
    """
    Model for archiving (or deleting) an existing Trello Board.
    """
    id: Annotated[str, Field(strict=True, description="The ID of the board to archive/delete")]
