# robopost_client.py

import os
import requests
from enum import Enum
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


# ---------------------------------------------------------
# Enums (Existing + New for AutomationRecurInterval)
# ---------------------------------------------------------
class AIImageModel(Enum):
    DALLE = "DALLE"
    FLUX_SCHNELL = "FLUX_SCHNELL"
    FLUX_DEV = "FLUX_DEV"
    FLUX_PRO = "FLUX_PRO"


class PostAIGenerateVoiceTone(Enum):
    POLITE = "POLITE"
    WITTY = "WITTY"
    ENTHUSIASTIC = "ENTHUSIASTIC"
    INFORMATIONAL = "INFORMATIONAL"
    FUNNY = "FUNNY"
    FORMAL = "FORMAL"
    INFORMAL = "INFORMAL"
    HUMOROUS = "HUMOROUS"
    SERIOUS = "SERIOUS"
    OPTIMISTIC = "OPTIMISTIC"
    MOTIVATING = "MOTIVATING"
    RESPECTFUL = "RESPECTFUL"
    ASSERTIVE = "ASSERTIVE"
    CONVERSATIONAL = "CONVERSATIONAL"
    CASUAL = "CASUAL"
    PROFESSIONAL = "PROFESSIONAL"
    SMART = "SMART"
    NOSTALGIC = "NOSTALGIC"
    FRIENDLY = "FRIENDLY"


class AutomationRecurInterval(Enum):
    DAILY_SPECIFIC_TIME_SLOTS = "DAILY_SPECIFIC_TIME_SLOTS"
    WEEKLY_SPECIFIC_TIME_SLOTS = "WEEKLY_SPECIFIC_TIME_SLOTS"
    EVERY_3_HOURS = "EVERY_3_HOURS"
    EVERY_6_HOURS = "EVERY_6_HOURS"
    BI_DAILY = "BI_DAILY"  # every 12 hours
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"


# ---------------------------------------------------------
# Scheduled Post Models
# ---------------------------------------------------------
class PublicAPIScheduledPostCreateHTTPPayload(BaseModel):
    text: str = ""
    channel_ids: List[str] = []
    image_object_ids: List[str] = []
    video_object_id: Optional[str] = None
    gif_object_id: Optional[str] = None

    facebook_settings: Optional[dict] = None
    instagram_settings: Optional[dict] = None
    pinterest_settings: Optional[dict] = None
    wordpress_settings: Optional[dict] = None
    youtube_settings: Optional[dict] = None
    tiktok_settings: Optional[dict] = None
    gmb_settings: Optional[dict] = None

    post_collection_id: Optional[str] = None
    is_draft: bool = False
    is_recur: bool = False
    schedule_at: Optional[str] = None  # ISO datetime string (UTC)
    recur_generate_new_ai_image: bool = False
    recur_generate_new_ai_image_model: Optional[AIImageModel] = None
    recur_until_dt: Optional[str] = None
    recur_until_dt_enabled: bool = False
    recur_rephrase_text_with_ai: bool = False
    recur_rephrase_text_with_ai_tone: Optional[PostAIGenerateVoiceTone] = None


class PublicAPIScheduledPostRead(BaseModel):
    id: str = Field(...)
    text: str = Field("")
    channel_ids: List[str] = Field(..., min_items=1)
    image_object_ids: List[dict] = Field([])
    video_object_id: dict = Field(None)
    gif_object_id: dict = Field(None)
    facebook_settings: dict = Field({})
    instagram_settings: dict = Field({})
    pinterest_settings: dict = Field({})
    wordpress_settings: dict = Field({})
    youtube_settings: dict = Field({})
    tiktok_settings: dict = Field({})
    gmb_settings: dict = Field({})
    is_draft: bool = Field(False)
    post_collection_id: Optional[str] = Field(None)
    is_recur: bool = Field(False)
    recur_interval: AutomationRecurInterval = Field(AutomationRecurInterval.DAILY)
    recur_generate_new_ai_image: bool = Field(False)
    recur_generate_new_ai_image_model: AIImageModel = Field(AIImageModel.DALLE)
    recur_until_dt: Optional[datetime] = Field(None)
    recur_until_dt_enabled: bool = Field(False)
    recur_rephrase_text_with_ai: bool = Field(False)
    recur_rephrase_text_with_ai_tone: PostAIGenerateVoiceTone = Field(PostAIGenerateVoiceTone.FRIENDLY)


# ---------------------------------------------------------
# Media Models
# ---------------------------------------------------------
class PublicAPIMediaRead(BaseModel):
    id: str
    name: str
    extension: str
    storage_object_id: str


# ---------------------------------------------------------
# Robopost Client
# ---------------------------------------------------------
class RobopostClient:
    """
    A client to interact with the Robopost public API.

    The API key is provided during initialization and passed as a query parameter
    with every request.
    """

    def __init__(self, apikey: str, base_url: str = "https://public-api.robopost.app"):
        self.apikey = apikey
        self.base_url = base_url

    def upload_media(self, file_path: str) -> PublicAPIMediaRead:
        """
        Calls the POST /medias/upload endpoint to upload an image or video.

        :param file_path: Path to the local file to be uploaded.
        :return: A PublicAPIMediaRead instance containing the uploaded media info.
        """
        url = f"{self.base_url}/medias/upload"
        params = {"apikey": self.apikey}

        with open(file_path, "rb") as file_data:
            files = {"file": (os.path.basename(file_path), file_data)}
            response = requests.post(url, params=params, files=files)

        response.raise_for_status()
        return PublicAPIMediaRead.model_validate(response.json())

    def create_scheduled_posts(
        self,
        payload: PublicAPIScheduledPostCreateHTTPPayload,
    ) -> List[PublicAPIScheduledPostRead]:
        """
        Calls the POST /scheduled_posts endpoint to create new scheduled posts or drafts.

        :param payload: A PublicAPIScheduledPostCreateHTTPPayload instance with post details.
        :return: A list of PublicAPIScheduledPostRead instances.
        """
        url = f"{self.base_url}/scheduled_posts/"
        params = {"apikey": self.apikey}

        body = payload.model_dump()
        response = requests.post(url, params=params, json=body)
        response.raise_for_status()

        data = response.json()
        return [PublicAPIScheduledPostRead.model_validate(item) for item in data]
