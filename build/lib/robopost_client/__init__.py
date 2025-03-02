import os
import uuid
import requests
from enum import Enum
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

# ---------------------------------------------------------
# Enums
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

# New Enums for Social Media Settings
class FacebookPostType(str, Enum):
    POST = "POST"
    REELS = "REELS"

class InstagramPostType(str, Enum):
    POST = "POST"
    REELS = "REELS"
    STORIES = "STORIES"

class WordpressPostType(str, Enum):
    POST = "POST"

class YoutubeVideoType(str, Enum):
    VIDEO = "video"
    SHORT = "short"

class YoutubePrivacyStatus(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    UNLISTED = "unlisted"

class TikTokPrivacyLevel(str, Enum):
    PUBLIC_TO_EVERYONE = "PUBLIC_TO_EVERYONE"

class GMBPostTopicType(str, Enum):
    STANDARD = "STANDARD"
    OFFER = "OFFER"
    EVENT = "EVENT"

class GMBCTAButtonActionType(str, Enum):
    ACTION_TYPE_UNSPECIFIED = "ACTION_TYPE_UNSPECIFIED"
    BOOK = "BOOK"
    ORDER = "ORDER"
    SHOP = "SHOP"
    LEARN_MORE = "LEARN_MORE"
    SIGN_UP = "SIGN_UP"
    CALL = "CALL"

# ---------------------------------------------------------
# Models for Social Media Settings
# ---------------------------------------------------------
class FacebookSettings(BaseModel):
    postType: FacebookPostType = Field(default=FacebookPostType.POST)

class InstagramSettings(BaseModel):
    postType: InstagramPostType = Field(default=InstagramPostType.POST)

class PinterestSettings(BaseModel):
    pinTitle: str = ""
    destinationLink: str = ""

class WordpressSettings(BaseModel):
    postTitle: str = ""
    postText: str = ""
    postSlug: str = ""
    postType: WordpressPostType = Field(default=WordpressPostType.POST)
    postCategories: List[str] = Field(default_factory=list)
    postTags: List[str] = Field(default_factory=list)
    postFeaturedImage: Optional[str] = None
    postParentPage: int = 0

class YoutubeSettings(BaseModel):
    videoObject: Optional[str] = None
    videoTitle: str = ""
    videoType: YoutubeVideoType = Field(default=YoutubeVideoType.VIDEO)
    videoDescription: str = ""
    videoPrivacyStatus: YoutubePrivacyStatus = Field(default=YoutubePrivacyStatus.PUBLIC)
    videoThumbnailImageObject: Optional[str] = None
    videoThumbnailGroupUuid: Optional[str] = None

class TikTokSettings(BaseModel):
    title: str = ""
    privacyLevel: TikTokPrivacyLevel = Field(default=TikTokPrivacyLevel.PUBLIC_TO_EVERYONE)
    disableDuet: bool = False
    disableComment: bool = False
    disableStitch: bool = False
    videoCoverTimestampMs: int = 0
    videoObject: Optional[str] = None
    videoThumbnailGroupUuid: Optional[str] = None
    autoAddMusic: bool = True

class GMBSettings(BaseModel):
    postTopicType: GMBPostTopicType = Field(default=GMBPostTopicType.STANDARD)
    offerTitle: str = ""
    offerCouponCode: str = ""
    offerRedeemOnlineUrl: str = ""
    offerTermsConditions: str = ""
    offerStartDt: Optional[datetime] = None
    offerEndDt: Optional[datetime] = None
    eventTitle: str = ""
    eventStartDt: Optional[datetime] = None
    eventEndDt: Optional[datetime] = None
    ctaButtonActionType: GMBCTAButtonActionType = Field(default=GMBCTAButtonActionType.ACTION_TYPE_UNSPECIFIED)
    ctaUrl: str = ""

# ---------------------------------------------------------
# Models for Scheduled Posts
# ---------------------------------------------------------
class PublicAPIScheduledPostCreateHTTPPayload(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    text: str = Field("")
    channel_ids: List[str] = Field(default_factory=list)
    image_object_ids: List[str] = Field(default_factory=list)
    video_object_id: Optional[str] = Field(None)
    gif_object_id: Optional[str] = Field(None)

    facebook_settings: FacebookSettings = Field(default_factory=FacebookSettings)
    instagram_settings: InstagramSettings = Field(default_factory=InstagramSettings)
    pinterest_settings: PinterestSettings = Field(default_factory=PinterestSettings)
    wordpress_settings: WordpressSettings = Field(default_factory=WordpressSettings)
    youtube_settings: YoutubeSettings = Field(default_factory=YoutubeSettings)
    tiktok_settings: TikTokSettings = Field(default_factory=TikTokSettings)
    gmb_settings: GMBSettings = Field(default_factory=GMBSettings)

    is_draft: bool = Field(False)
    post_collection_id: Optional[str] = Field(None)
    schedule_at: datetime = Field(default_factory=datetime.now)
    is_recur: bool = Field(False)
    recur_interval: Optional[AutomationRecurInterval] = Field(default=AutomationRecurInterval.DAILY)
    recur_generate_new_ai_image: bool = Field(False)
    recur_generate_new_ai_image_model: AIImageModel = Field(default=AIImageModel.DALLE)
    recur_until_dt: Optional[datetime] = Field(None)
    recur_until_dt_enabled: bool = Field(False)
    recur_rephrase_text_with_ai: bool = Field(False)
    recur_rephrase_text_with_ai_tone: PostAIGenerateVoiceTone = Field(default=PostAIGenerateVoiceTone.FRIENDLY)
    recur_interval_time_slots: List[str] = Field(default_factory=list)

class PublicAPIScheduledPostRead(BaseModel):
    id: str = Field(...)
    text: str = Field("")
    channel_ids: List[str] = Field(default_factory=list)
    image_object_ids: List[str] = Field(default_factory=list)
    video_object_id: Optional[str] = Field(None)
    gif_object_id: Optional[str] = Field(None)

    facebook_settings: FacebookSettings = Field(default_factory=FacebookSettings)
    instagram_settings: InstagramSettings = Field(default_factory=InstagramSettings)
    pinterest_settings: PinterestSettings = Field(default_factory=PinterestSettings)
    wordpress_settings: WordpressSettings = Field(default_factory=WordpressSettings)
    youtube_settings: YoutubeSettings = Field(default_factory=YoutubeSettings)
    tiktok_settings: TikTokSettings = Field(default_factory=TikTokSettings)
    gmb_settings: GMBSettings = Field(default_factory=GMBSettings)

    is_draft: bool = Field(False)
    post_collection_id: Optional[str] = Field(None)
    schedule_at: datetime = Field(...)
    is_recur: bool = Field(False)
    recur_interval: AutomationRecurInterval = Field(default=AutomationRecurInterval.DAILY)
    recur_generate_new_ai_image: bool = Field(False)
    recur_generate_new_ai_image_model: AIImageModel = Field(default=AIImageModel.DALLE)
    recur_until_dt: Optional[datetime] = Field(None)
    recur_until_dt_enabled: bool = Field(False)
    recur_rephrase_text_with_ai: bool = Field(False)
    recur_rephrase_text_with_ai_tone: PostAIGenerateVoiceTone = Field(default=PostAIGenerateVoiceTone.FRIENDLY)
    recur_interval_time_slots: List[str] = Field(default_factory=list)

# ---------------------------------------------------------
# Media Model
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

        json_data = payload.model_dump_json()
        print(f"sending payload: {json_data}")
        response = requests.post(url, params=params, data=json_data, headers={"Content-Type": "application/json"})
        print(f"response: {response.text}")
        response.raise_for_status()

        data = response.json()
        return [PublicAPIScheduledPostRead.model_validate(item) for item in data]
