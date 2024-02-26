from pydantic.fields import Field
from datetime import datetime, date
from typing import Any, List, Optional, Union

from pydantic import StrictBool, StrictFloat, StrictInt, StrictStr

from app.flow_execution.models.base import BaseAPIModel, BaseIntegrationActionModel

class TrelloCard(BaseAPIModel):
    """
    Trello API Card model.
    """ # noqa: E501
    id: Optional[str] = Field(default=None, description="Unique identifier of the card")
    address: Optional[StrictStr] = Field(default=None, description="Address of the card, if applicable")
    closed: Optional[StrictBool] = Field(default=None, description="Whether the card is archived/closed")
    coordinates: Optional[StrictStr] = Field(default=None, description="Coordinates of the card, if applicable")
    creation_method: Optional[StrictStr] = Field(default=None, description="Method used for card creation", alias="creationMethod")
    date_last_activity: Optional[datetime] = Field(default=None, description="Last activity date of the card", alias="dateLastActivity")
    desc: Optional[StrictStr] = Field(default=None, description="Description of the card")
    due: Optional[date] = Field(default=None, description="Due date of the card")
    due_reminder: Optional[StrictStr] = Field(default=None, description="Reminder setting for the due date", alias="dueReminder")
    email: Optional[StrictStr] = Field(default=None, description="Email associated with the card")
    id_board: Optional[str] = Field(default=None, description="ID of the board the card belongs to", alias="idBoard")
    id_list: Optional[str] = Field(default=None, description="ID of the list the card belongs to", alias="idList")
    id_short: Optional[StrictInt] = Field(default=None, description="Short identifier for the card", alias="idShort")
    id_attachment_cover: Optional[str] = Field(default=None, description="ID of the cover attachment", alias="idAttachmentCover")
    location_name: Optional[StrictStr] = Field(default=None, description="Name of the location associated with the card", alias="locationName")
    manual_cover_attachment: Optional[StrictBool] = Field(default=None, description="Whether the cover attachment is set manually", alias="manualCoverAttachment")
    name: Optional[StrictStr] = Field(default=None, description="Name of the card")
    pos: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Position of the card in the list")
    short_link: Optional[StrictStr] = Field(default=None, description="Short link for the card", alias="shortLink")
    short_url: Optional[StrictStr] = Field(default=None, description="Short URL for the card", alias="shortUrl")
    subscribed: Optional[StrictBool] = Field(default=None, description="Whether the user is subscribed to the card")
    url: Optional[StrictStr] = Field(default=None, description="URL of the card")

class TrelloCardCreate(BaseIntegrationActionModel):
    """
    Model for creating a new Card.
    """
    name: str = Field(description="The name for the card")
    id_list: Optional[str] = Field(default=None, description="The ID of the list the card should be created in")
    desc: Optional[str] = Field(default=None, description="The description for the card")
    pos: Optional[Union[str, float]] = Field(default=None, description="The position of the new card. `top`, `bottom`, or a positive float")
    due: Optional[date] = Field(default=None, description="A due date for the card")
    start: Optional[date] = Field(default=None, description="The start date of a card, or `null`")
    id_labels: Optional[str] = Field(default=None, description="Comma-separated list of label IDs to add to the card")
    
class TrelloCardGet(BaseAPIModel):
    id: str = Field(None, description="The ID of the list the card should be created in")

class TrelloCardUpdate(BaseIntegrationActionModel):
    """
    Model for updating an existing Card.
    """
    id: str = Field(description="The ID of the Card")
    name: Optional[StrictStr] = Field(default=None, description="The new name for the card")
    desc: Optional[StrictStr] = Field(default=None, description="The new description for the card")
    closed: Optional[StrictBool] = Field(default=None, description="Whether the card should be archived (closed: true)")
    id_members: Optional[str] = Field(default=None, description="Comma-separated list of member IDs")
    id_attachment_cover: Optional[str] = Field(default=None, description="The ID of the image attachment the card should use as its cover, or null for none")
    id_list: Optional[str] = Field(default=None, description="The ID of the list the card should be in")
    id_labels: Optional[str] = Field(default=None, description="Comma-separated list of label IDs")
    pos: Optional[Any] = Field(default=None, description="The position of the card in its list. `top`, `bottom`, or a positive float")
    due: Optional[date] = Field(default=None, description="When the card is due, or `null`")
    start: Optional[date] = Field(default=None, description="The start date of a card, or `null`")
    due_complete: Optional[StrictBool] = Field(default=None, description="Whether the due date should be marked complete")
    subscribed: Optional[StrictBool] = Field(default=None, description="Whether the member is should be subscribed to the card")
    address: Optional[StrictStr] = Field(default=None, description="For use with/by the Map View")
    location_name: Optional[StrictStr] = Field(default=None, description="For use with/by the Map View")
    coordinates: Optional[StrictStr] = Field(default=None, description="For use with/by the Map View. Should be latitude,longitude")
    
class TrelloCardDelete(BaseIntegrationActionModel):
    """
    Model for deleting an existing Card.
    """
    id: str =  Field(None, description="The ID of the Card")
    
class TrelloList(BaseAPIModel):
    """
    Trello API List model.
    """
    id: Optional[str] = Field(default=None)
    name: Optional[StrictStr] =  Field(default=None, description="The name of the list")
    closed: Optional[StrictBool] = Field(None)
    pos: Optional[Union[StrictFloat, StrictInt]] = Field(None)
    soft_limit: Optional[StrictStr] = Field(default=None, alias="softLimit")
    id_board: Optional[StrictStr] = Field(default=None, alias="idBoard")
    subscribed: Optional[StrictBool] =  Field(None)

class TrelloListCreate(BaseIntegrationActionModel):
    """
    Model for creating a new Trello List.
    """
    name: StrictStr = Field(description="The name for the list")
    id_board: str = Field(default=None, description="The ID of the board the list should be created in")
    pos: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Position of the list in the board. `top`, `bottom`, or a positive float")

class TrelloListGet(BaseIntegrationActionModel):
    """
    Model for retrieving details of a specific Trello List.
    """
    id: str =  Field(None, description="The ID of the List to retrieve")

class TrelloListUpdate(BaseIntegrationActionModel):
    
    id: str = Field(description="The ID of the list")
    name: Optional[str] = Field(default=None, description="New name for the list")
    closed: Optional[StrictBool] = Field(default=None, description="Whether the list should be closed (archived)")
    id_board: Optional[str] = Field(default=None, description="ID of a board the list should be moved to")
    pos: Optional[Any] = Field(default=None, description="New position for the list: `top`, `bottom`, or a positive floating point number")

class TrelloBoard(BaseAPIModel):
    """
    Trello API Card model.
    """
    
    id: str = Field(description="The ID of the board.")
    name: Optional[StrictStr] = Field(default=None, description="The new name of the board")
    desc: Optional[StrictStr] = Field(default=None, description="The new description of the board")
    desc_data: Optional[StrictStr] = Field(default=None, description="The new descData of the board", alias="descData")
    closed: Optional[StrictBool] = Field(default=None, description="Whether the board should be closed/archived")
    id_member_creator: Optional[str] = Field(None, description="The new idMemberCreator of the board", alias="idMemberCreator")
    id_organization: Optional[str] = Field(None, description="The new idOrganization of the board", alias="idOrganization")
    pinned: Optional[StrictBool] = Field(default=None, description="Whether the board should be pinned")
    url: Optional[StrictStr] = Field(default=None, description="The new url of the board")
    short_url: Optional[StrictStr] = Field(default=None, description="The new shortUrl of the board", alias="shortUrl")
    starred: Optional[StrictBool] = Field(default=None, description="Whether the board should be starred")
    memberships: Optional[StrictStr] = Field(default=None, description="The new memberships of the board")
    short_link: Optional[StrictStr] = Field(default=None, description="The new shortLink of the board", alias="shortLink")
    subscribed: Optional[StrictBool] = Field(default=None, description="Whether the user is subscribed to the board")
    power_ups: Optional[StrictStr] = Field(default=None, description="The new powerUps of the board", alias="powerUps")
    date_last_activity: Optional[date] = Field(default=None, description="The new dateLastActivity of the board", alias="dateLastActivity")
    date_last_view: Optional[date] = Field(default=None, description="The new dateLastView of the board", alias="dateLastView")
    id_tags: Optional[StrictStr] = Field(default=None, description="The new idTags of the board", alias="idTags")
    date_plugin_disable: Optional[date] = Field(default=None, description="The new datePluginDisable of the board", alias="datePluginDisable")
    creation_method: Optional[StrictStr] = Field(default=None, description="The new creationMethod of the board", alias="creationMethod")
    ix_update: Optional[StrictInt] = Field(default=None, description="The new ixUpdate of the board", alias="ixUpdate")
    template_gallery: Optional[StrictStr] = Field(default=None, description="The new templateGallery of the board", alias="templateGallery")
    enterprise_owned: Optional[StrictBool] = Field(default=None, description="Whether the board is enterprise owned", alias="enterpriseOwned")

class TrelloBoardCreate(BaseIntegrationActionModel):
    """
    Model for creating a new Trello Board.
    """
    name: str = Field(min_length=1, max_length=16384, description="The new name for the board.")
    default_labels: Optional[StrictBool] = Field(default=None, description="Determines whether to use the default set of labels.", alias="defaultLabels")
    default_lists: Optional[StrictBool] = Field(default=None, description="Determines whether to add the default set of lists to a board (To Do, Doing, Done).", alias="defaultLists")
    desc: Optional[str] = Field(default=None, min_length=0, max_length=16384, description="A new description for the board, 0 to 16384 characters long")
    
class TrelloBoardGet(BaseIntegrationActionModel):
    """
    Model for retrieving details of a specific Trello Board.
    """
    id: str = Field(None, description="The ID of the board to retrieve")

class TrelloBoardUpdate(BaseIntegrationActionModel):
    """
    Model for updating an existing Trello Board.
    """
    id: str = Field(None)
    name: Optional[StrictStr] = Field(default=None, description="The new name for the board.")
    desc: Optional[StrictStr] = Field(default=None, description="A new description for the board, 0 to 16384 characters long")
    closed: Optional[StrictBool] = Field(default=None, description="Whether the board is closed")

class TrelloBoardDelete(BaseIntegrationActionModel):
    """
    Model for archiving (or deleting) an existing Trello Board.
    """
    id: str = Field(None, description="The ID of the board to archive/delete")
