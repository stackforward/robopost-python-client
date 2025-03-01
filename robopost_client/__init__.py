import os
import uuid
import requests
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


# ------------------------------------------------------------------------
# Enums (Updated with your provided values for AIImageModel & PostAIGenerateVoiceTone)
# ------------------------------------------------------------------------
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


# ------------------------------------------------------------------------
# Pydantic Models for /scheduled_posts
# ------------------------------------------------------------------------
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
    schedule_at: Optional[str] = None  # ISO datetime string

    recur_generate_new_ai_image: bool = False
    recur_generate_new_ai_image_model: Optional[AIImageModel] = None
    recur_until_dt: Optional[str] = None  # ISO datetime string
    recur_until_dt_enabled: bool = False
    recur_rephrase_text_with_ai: bool = False
    recur_rephrase_text_with_ai_tone: Optional[PostAIGenerateVoiceTone] = None


class PublicAPIScheduledPostRead(BaseModel):
    id: str
    text: str
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

    is_draft: bool = False
    post_collection_id: Optional[str] = None
    is_recur: bool = False
    recur_generate_new_ai_image: bool = False
    recur_generate_new_ai_image_model: Optional[AIImageModel] = None
    recur_until_dt: Optional[str] = None
    recur_until_dt_enabled: bool = False
    recur_rephrase_text_with_ai: bool = False
    recur_rephrase_text_with_ai_tone: Optional[PostAIGenerateVoiceTone] = None


# ------------------------------------------------------------------------
# Pydantic Model for /medias/upload
# ------------------------------------------------------------------------
class PublicAPIMediaRead(BaseModel):
    id: str
    name: str
    extension: str
    storage_object_id: str


# ------------------------------------------------------------------------
# The RobopostClient Class
# ------------------------------------------------------------------------
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
