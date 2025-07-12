import os
import uuid
import requests
from enum import Enum
from typing import List, Optional, Dict, Any
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
    PAGE = "PAGE"


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


# Fixed Video Series Enums - matching the original comprehensive options
class GeneratedFacelessVideoSeriesContentType(str, Enum):
    RANDOM_AI_STORY = "RANDOM_AI_STORY"
    SCARY_STORIES = "SCARY_STORIES"
    BEDTIME_STORIES = "BEDTIME_STORIES"
    INTERESTING_HISTORY = "INTERESTING_HISTORY"
    URBAN_LEGENDS = "URBAN_LEGENDS"
    MOTIVATIONAL = "MOTIVATIONAL"
    FUN_FACTS = "FUN_FACTS"
    LONG_FORM_JOKES = "LONG_FORM_JOKES"
    LIFE_PRO_TIPS = "LIFE_PRO_TIPS"
    ELI5 = "ELI5"
    DID_YOU_KNOW = "DID_YOU_KNOW"
    PHILOSOPHY = "PHILOSOPHY"
    RECIPES = "RECIPES"
    FITNESS = "FITNESS"
    BEAUTY = "BEAUTY"
    GROWTH_ADVICE = "GROWTH_ADVICE"
    # custom
    PRODUCT_MARKETING = "PRODUCT_MARKETING"
    CUSTOM = "CUSTOM"
    BLOG_ARTICLE = "BLOG_ARTICLE"


class GeneratedFacelessVideoStyle(str, Enum):
    DEFAULT = "DEFAULT"
    REALISM = "REALISM"
    IMPRESSIONISM = "IMPRESSIONISM"
    SURREALISM = "SURREALISM"
    ABSTRACT = "ABSTRACT"
    ART_NOUVEAU = "ART_NOUVEAU"
    CUBISM = "CUBISM"
    POP_ART = "POP_ART"
    FUTURISM = "FUTURISM"
    FANTASY_CONCEPT_ART = "FANTASY_CONCEPT_ART"
    MINIMALISM = "MINIMALISM"
    WATERCOLOR = "WATERCOLOR"
    GOTHIC_MEDIEVAL_ART = "GOTHIC_MEDIEVAL_ART"
    ANIME = "ANIME"
    COMIC = "COMIC"


class ImageStyle(Enum):
    DEFAULT = "DEFAULT"
    REALISM = "REALISM"
    IMPRESSIONISM = "IMPRESSIONISM"
    SURREALISM = "SURREALISM"
    ABSTRACT = "ABSTRACT"
    ART_NOUVEAU = "ART_NOUVEAU"
    CUBISM = "CUBISM"
    POP_ART = "POP_ART"
    FUTURISM = "FUTURISM"
    FANTASY_CONCEPT_ART = "FANTASY_CONCEPT_ART"
    MINIMALISM = "MINIMALISM"
    WATERCOLOR = "WATERCOLOR"
    GOTHIC_MEDIEVAL_ART = "GOTHIC_MEDIEVAL_ART"
    ANIME = "ANIME"
    COMIC = "COMIC"


class GeneratedVideoFormat(str, Enum):
    PORTRAIT = "PORTRAIT"
    WIDESCREEN = "WIDESCREEN"
    SQUARE = "SQUARE"


class AIVoice(str, Enum):
    CUSTOM = "CUSTOM"
    ALICE = "ALICE"
    BILL = "BILL"
    SARAH = "SARAH"
    BRIAN = "BRIAN"
    LAURA = "LAURA"
    ARIA = "ARIA"
    CALLUM = "CALLUM"
    CHARLIE = "CHARLIE"


class KokoroVoice(Enum):
    """Available voices for Kokoro TTS"""
    # Female voices (af_ prefix)
    AF_ALLOY = "af_alloy"
    AF_AOEDE = "af_aoede"
    AF_BELLA = "af_bella"
    AF_JESSICA = "af_jessica"
    AF_KORE = "af_kore"
    AF_NICOLE = "af_nicole"
    AF_NOVA = "af_nova"
    AF_RIVER = "af_river"
    AF_SARAH = "af_sarah"
    AF_SKY = "af_sky"

    # Male voices (am_ prefix)
    AM_ADAM = "am_adam"
    AM_ECHO = "am_echo"
    AM_ERIC = "am_eric"
    AM_FENRIR = "am_fenrir"
    AM_LIAM = "am_liam"
    AM_MICHAEL = "am_michael"
    AM_ONYX = "am_onyx"
    AM_PUCK = "am_puck"


class VideoColor(str, Enum):
    BLACK = "BLACK"
    WHITE = "WHITE"
    YELLOW = "YELLOW"
    RED = "RED"
    BLUE = "BLUE"
    GREEN = "GREEN"
    ORANGE = "ORANGE"
    PURPLE = "PURPLE"
    CYAN = "CYAN"
    MAGENTA = "MAGENTA"


class VideoCaptionPosition(str, Enum):
    CENTER_CENTER = "CENTER_CENTER"
    CENTER_TOP = "CENTER_TOP"
    CENTER_BOTTOM = "CENTER_BOTTOM"
    LEFT_CENTER = "LEFT_CENTER"
    LEFT_TOP = "LEFT_TOP"
    LEFT_BOTTOM = "LEFT_BOTTOM"
    RIGHT_CENTER = "RIGHT_CENTER"
    RIGHT_TOP = "RIGHT_TOP"
    RIGHT_BOTTOM = "RIGHT_BOTTOM"


class AutomationPostTo(str, Enum):
    DIRECT = "DIRECT"
    DRAFT = "DRAFT"
    POST_COLLECTION = "POST_COLLECTION"


class GeneratedFacelessVideoProcessState(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETE = "COMPLETE"
    ERROR = "ERROR"
    NO_CREDITS = "NO_CREDITS"


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
    """
    Represents the payload for creating a scheduled post via the Public API.
    Includes optional lists of URLs (image_urls, video_url, gif_url) which the
    server can handle (uploading to UploadCare, etc.) before assigning final
    object_ids.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    text: str = Field("")
    channel_ids: List[str] = Field(default_factory=list)
    image_object_ids: List[str] = Field(default_factory=list)
    video_object_id: Optional[str] = Field(None)
    gif_object_id: Optional[str] = Field(None)
    image_urls: List[str] = Field(default_factory=list)
    video_url: Optional[str] = Field(None)
    gif_url: Optional[str] = Field(None)
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
    daily_recur_interval_time_slots: List[str] = Field(default_factory=list)
    weekly_recur_interval_time_slots: List[str] = Field(default_factory=list)
    first_comment: str = Field("", description="First comment to add after posting to social media")


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
    first_comment: str = Field("", description="First comment to add after posting to social media")


# ---------------------------------------------------------
# Video Series Models
# ---------------------------------------------------------
class PublicAPIGeneratedFacelessVideoSeriesCreate(BaseModel):
    """Model for creating a new video series"""
    name: str = Field(..., description="Name of the video series", max_length=200)
    content_type: GeneratedFacelessVideoSeriesContentType = Field(
        default=GeneratedFacelessVideoSeriesContentType.ELI5,
        description="Type of content to generate"
    )
    style: GeneratedFacelessVideoStyle = Field(
        default=GeneratedFacelessVideoStyle.DEFAULT,
        description="Visual style of the videos"
    )
    voice: str = Field(
        default=AIVoice.ALICE.value,
        description="Voice to use for narration (AI voice name or ElevenLabs voice ID)"
    )
    text_prefix: str = Field(
        default="",
        description="Text to add before the main content",
        max_length=5000
    )
    text_suffix: str = Field(
        default="",
        description="Text to add after the main content",
        max_length=5000
    )
    lang: str = Field(
        default="en",
        description="Language code for the content",
        max_length=10
    )
    stick_to_script: bool = Field(
        default=False,
        description="Whether to strictly follow the script or allow AI improvisation"
    )
    content_custom: str = Field(
        default="",
        description="Custom content instructions",
        max_length=10000
    )
    format: GeneratedVideoFormat = Field(
        default=GeneratedVideoFormat.PORTRAIT,
        description="Video format/aspect ratio"
    )
    max_duration: int = Field(
        default=60,
        ge=5,
        le=600,
        description="Maximum video duration in seconds"
    )
    prevent_text_in_video: bool = Field(
        default=False,
        description="Whether to prevent text overlays in the video"
    )
    use_knowledge_base: bool = Field(
        default=False,
        description="Whether to use a knowledge base for content generation"
    )
    knowledge_base_id: Optional[str] = Field(
        default=None,
        description="ID of the knowledge base to use (if use_knowledge_base is True)"
    )
    bgm_bucket_id: Optional[str] = Field(
        default=None,
        description="ID of the background music bucket to use"
    )
    splash_screen_object: Optional[dict] = Field(
        default=None,
        description="Splash screen configuration object"
    )
    create_scheduled_post: bool = Field(
        default=False,
        description="Whether to create scheduled posts when videos are generated"
    )
    post_to: AutomationPostTo = Field(
        default=AutomationPostTo.DIRECT,
        description="Where to post generated videos"
    )
    post_collection_ids: List[str] = Field(
        default_factory=list,
        description="IDs of post collections to add videos to"
    )
    channel_ids: List[str] = Field(
        default_factory=list,
        description="IDs of channels to post videos to"
    )

    # Audio settings
    narration_volume: float = Field(
        default=1.2,
        ge=0.6,
        le=1.8,
        description="Narration audio volume multiplier"
    )
    bgm_volume: float = Field(
        default=0.2,
        ge=0.05,
        le=0.4,
        description="Background music volume multiplier"
    )

    # Caption settings
    font_size: int = Field(
        default=110,
        ge=10,
        le=300,
        description="Caption font size"
    )
    font_color: VideoColor = Field(
        default=VideoColor.YELLOW,
        description="Caption text color"
    )
    stroke_width: int = Field(
        default=3,
        ge=0,
        le=20,
        description="Caption text stroke width"
    )
    stroke_color: VideoColor = Field(
        default=VideoColor.BLACK,
        description="Caption text stroke color"
    )
    shadow_strength: float = Field(
        default=1.0,
        ge=0.0,
        le=5.0,
        description="Caption shadow strength"
    )
    shadow_blur: float = Field(
        default=0.1,
        ge=0.0,
        le=10.0,
        description="Caption shadow blur amount"
    )
    highlight_current_word: bool = Field(
        default=True,
        description="Whether to highlight the currently spoken word"
    )
    word_highlight_color: VideoColor = Field(
        default=VideoColor.RED,
        description="Color for highlighting current word"
    )
    line_count: int = Field(
        default=1,
        ge=1,
        le=10,
        description="Maximum lines of caption text on screen"
    )
    padding: int = Field(
        default=50,
        ge=0,
        le=500,
        description="Caption padding from screen edges in pixels"
    )
    position: VideoCaptionPosition = Field(
        default=VideoCaptionPosition.CENTER_CENTER,
        description="Caption position on screen"
    )

    # Recurrence settings
    is_recur: bool = Field(
        default=False,
        description="Whether this series should generate videos on a schedule"
    )
    timezone: Optional[str] = Field(
        default=None,
        description="Timezone for scheduled generation"
    )
    recur_dt: Optional[datetime] = Field(
        default=None,
        description="Next scheduled generation time"
    )
    recur_interval: Optional[AutomationRecurInterval] = Field(
        default=None,
        description="Interval for recurring generation"
    )
    recur_interval_time_slots: List[str] = Field(
        default_factory=list,
        description="Time slots for daily recurring generation"
    )
    recur_interval_weekly_time_slots: List[str] = Field(
        default_factory=list,
        description="Time slots for weekly recurring generation"
    )
    recur_until_dt: Optional[datetime] = Field(
        default=None,
        description="When to stop recurring generation"
    )
    recur_until_dt_enabled: bool = Field(
        default=False,
        description="Whether the recur_until_dt is enabled"
    )


class PublicAPIGeneratedFacelessVideoSeriesUpdate(BaseModel):
    """Model for updating an existing video series"""
    name: Optional[str] = Field(None, max_length=200)
    content_type: Optional[GeneratedFacelessVideoSeriesContentType] = None
    style: Optional[GeneratedFacelessVideoStyle] = None
    voice: Optional[str] = None
    text_prefix: Optional[str] = Field(None, max_length=5000)
    text_suffix: Optional[str] = Field(None, max_length=5000)
    lang: Optional[str] = Field(None, max_length=10)
    stick_to_script: Optional[bool] = None
    content_custom: Optional[str] = Field(None, max_length=10000)
    bgm_bucket_id: Optional[str] = None
    splash_screen_object: Optional[dict] = None
    format: Optional[GeneratedVideoFormat] = None
    max_duration: Optional[int] = Field(None, ge=5, le=600)
    prevent_text_in_video: Optional[bool] = None

    # Audio settings
    narration_volume: Optional[float] = Field(None, ge=0.6, le=1.8)
    bgm_volume: Optional[float] = Field(None, ge=0.05, le=0.4)

    # Caption settings
    font_size: Optional[int] = Field(None, ge=10, le=300)
    font_color: Optional[VideoColor] = None
    stroke_width: Optional[int] = Field(None, ge=0, le=20)
    stroke_color: Optional[VideoColor] = None
    shadow_strength: Optional[float] = Field(None, ge=0.0, le=5.0)
    shadow_blur: Optional[float] = Field(None, ge=0.0, le=10.0)
    highlight_current_word: Optional[bool] = None
    word_highlight_color: Optional[VideoColor] = None
    line_count: Optional[int] = Field(None, ge=1, le=10)
    padding: Optional[int] = Field(None, ge=0, le=500)
    position: Optional[VideoCaptionPosition] = None

    # Posting settings
    create_scheduled_post: Optional[bool] = None
    post_to: Optional[AutomationPostTo] = None
    post_collection_ids: Optional[List[str]] = None
    channel_ids: Optional[List[str]] = None

    # Recurrence settings
    is_recur: Optional[bool] = None
    timezone: Optional[str] = None
    recur_dt: Optional[datetime] = None
    recur_interval: Optional[AutomationRecurInterval] = None
    recur_interval_time_slots: Optional[List[str]] = None
    recur_interval_weekly_time_slots: Optional[List[str]] = None
    recur_until_dt: Optional[datetime] = None
    recur_until_dt_enabled: Optional[bool] = None


class PublicAPIGeneratedFacelessVideoSeriesRead(BaseModel):
    """Model for reading video series data"""
    id: str = Field(..., description="Unique identifier of the video series")
    name: str = Field(..., description="Name of the video series")
    content_type: GeneratedFacelessVideoSeriesContentType = Field(description="Content type")
    style: GeneratedFacelessVideoStyle = Field(description="Video style")
    voice: str = Field(description="Voice used for narration")
    text_prefix: str = Field(description="Text prefix")
    text_suffix: str = Field(description="Text suffix")
    lang: str = Field(description="Language code")
    stick_to_script: bool = Field(description="Whether to stick to script")
    content_custom: str = Field(description="Custom content instructions")
    format: GeneratedVideoFormat = Field(description="Video format")
    max_duration: int = Field(description="Maximum duration in seconds")
    prevent_text_in_video: bool = Field(description="Whether text overlays are prevented")
    use_knowledge_base: bool = Field(description="Whether knowledge base is used")
    knowledge_base_id: Optional[str] = Field(description="Knowledge base ID if used")
    bgm_bucket_id: Optional[str] = Field(description="Background music bucket ID")
    splash_screen_object: Optional[dict] = Field(description="Splash screen configuration")
    automation_id: Optional[str] = Field(description="Associated automation ID for recurring generation")
    create_scheduled_post: bool = Field(description="Whether scheduled posts are created")
    post_to: AutomationPostTo = Field(description="Where videos are posted")
    post_collection_ids: List[str] = Field(description="Post collection IDs")
    channel_ids: List[str] = Field(description="Channel IDs for posting")

    # Audio settings
    narration_volume: float = Field(description="Narration volume")
    bgm_volume: float = Field(description="Background music volume")

    # Caption settings
    font_size: int = Field(description="Caption font size")
    font_color: VideoColor = Field(description="Caption text color")
    stroke_width: int = Field(description="Caption stroke width")
    stroke_color: VideoColor = Field(description="Caption stroke color")
    shadow_strength: float = Field(description="Caption shadow strength")
    shadow_blur: float = Field(description="Caption shadow blur")
    highlight_current_word: bool = Field(description="Whether current word is highlighted")
    word_highlight_color: VideoColor = Field(description="Current word highlight color")
    line_count: int = Field(description="Maximum caption lines")
    padding: int = Field(description="Caption padding")
    position: VideoCaptionPosition = Field(description="Caption position")

    # Recurrence settings
    is_recur: bool = Field(description="Whether series has recurring generation")
    timezone: Optional[str] = Field(description="Timezone for scheduling")
    recur_dt: Optional[datetime] = Field(description="Next generation time")
    recur_interval: Optional[AutomationRecurInterval] = Field(description="Recurrence interval")
    recur_interval_time_slots: List[str] = Field(description="Daily time slots")
    recur_interval_weekly_time_slots: List[str] = Field(description="Weekly time slots")
    recur_until_dt: Optional[datetime] = Field(description="End date for recurrence")
    recur_until_dt_enabled: bool = Field(description="Whether end date is enabled")

    # Metadata
    is_deleted: bool = Field(description="Whether the series is deleted")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class PublicAPIVideoTaskResponse(BaseModel):
    """Response model for video generation task"""
    task_id: str = Field(..., description="Unique identifier for the video generation task")
    video_series_id: str = Field(..., description="ID of the video series this task belongs to")
    status: str = Field(..., description="Current status of the task")
    created_at: datetime = Field(..., description="Task creation timestamp")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


# ---------------------------------------------------------
# Media Model
# ---------------------------------------------------------
class PublicAPIMediaRead(BaseModel):
    id: str
    name: str
    extension: str
    storage_object_id: str


# ---------------------------------------------------------
# API Exception Classes
# ---------------------------------------------------------
class RobopostAPIError(Exception):
    """Base exception for Robopost API errors"""

    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


class RobopostPlanLimitError(RobopostAPIError):
    """Exception for plan limit errors"""

    def __init__(self, message: str, limit: int = None, current_usage: int = None):
        self.limit = limit
        self.current_usage = current_usage
        super().__init__(message, status_code=409)


# ---------------------------------------------------------
# Robopost Client
# ---------------------------------------------------------
class RobopostClient:
    """
    A client to interact with the Robopost public API.

    The API key is provided during initialization and passed as a query parameter
    with every request.
    """

    def __init__(self, apikey: str, base_url: str = "https://public-api.robopost.app/v1"):
        self.apikey = apikey
        self.base_url = base_url

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make an HTTP request with error handling"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        params = kwargs.get('params', {})
        params['apikey'] = self.apikey
        kwargs['params'] = params

        response = requests.request(method, url, **kwargs)

        # Handle API errors
        if not response.ok:
            try:
                error_data = response.json()
                if response.status_code == 409 and "plan limit" in str(error_data).lower():
                    raise RobopostPlanLimitError(
                        error_data.get('message', 'Plan limit reached'),
                        limit=error_data.get('limit'),
                        current_usage=error_data.get('current_usage')
                    )
                raise RobopostAPIError(
                    error_data.get('detail', error_data.get('message', 'API request failed')),
                    status_code=response.status_code,
                    response_data=error_data
                )
            except ValueError:
                # Response is not JSON
                response.raise_for_status()

        return response

    # ---------------------------------------------------------
    # Media Methods
    # ---------------------------------------------------------
    def upload_media(self, file_path: str) -> PublicAPIMediaRead:
        """
        Calls the POST /medias/upload endpoint to upload an image or video.

        :param file_path: Path to the local file to be uploaded.
        :return: A PublicAPIMediaRead instance containing the uploaded media info.
        """
        with open(file_path, "rb") as file_data:
            files = {"file": (os.path.basename(file_path), file_data)}
            response = self._make_request("POST", "/medias/upload", files=files)

        return PublicAPIMediaRead(**response.json())

    def list_media(self, skip: int = 0, limit: int = 50) -> List[PublicAPIMediaRead]:
        """
        Get a list of uploaded media files.

        :param skip: Number of items to skip (pagination)
        :param limit: Maximum number of items to return
        :return: List of PublicAPIMediaRead instances
        """
        params = {"skip": skip, "limit": limit}
        response = self._make_request("GET", "/medias/", params=params)

        return [PublicAPIMediaRead(**item) for item in response.json()]

    def get_media(self, media_id: str) -> PublicAPIMediaRead:
        """
        Get a specific media file by ID.

        :param media_id: ID of the media file
        :return: PublicAPIMediaRead instance
        """
        response = self._make_request("GET", f"/medias/{media_id}")
        return PublicAPIMediaRead(**response.json())

    def delete_media(self, media_id: str) -> dict:
        """
        Delete a media file.

        :param media_id: ID of the media file to delete
        :return: Success message
        """
        response = self._make_request("DELETE", f"/medias/{media_id}")
        return response.json()

    # ---------------------------------------------------------
    # Scheduled Posts Methods
    # ---------------------------------------------------------
    def create_scheduled_posts(
            self,
            payload: PublicAPIScheduledPostCreateHTTPPayload,
    ) -> List[PublicAPIScheduledPostRead]:
        """
        Calls the POST /scheduled_posts endpoint to create new scheduled posts or drafts.

        :param payload: A PublicAPIScheduledPostCreateHTTPPayload instance with post details.
        :return: A list of PublicAPIScheduledPostRead instances.
        """
        json_data = payload.model_dump_json()

        response = self._make_request(
            "POST",
            "/scheduled_posts/",
            data=json_data,
            headers={"Content-Type": "application/json"}
        )

        data = response.json()
        return [PublicAPIScheduledPostRead(**item) for item in data["scheduled_posts"]]

    # ---------------------------------------------------------
    # Video Series Methods
    # ---------------------------------------------------------
    def create_video_series(self,
                            payload: PublicAPIGeneratedFacelessVideoSeriesCreate) -> PublicAPIGeneratedFacelessVideoSeriesRead:
        """
        Create a new faceless video series.

        :param payload: Video series configuration
        :return: Created video series
        """
        json_data = payload.model_dump_json()

        response = self._make_request(
            "POST",
            "/video-series/",
            data=json_data,
            headers={"Content-Type": "application/json"}
        )

        return PublicAPIGeneratedFacelessVideoSeriesRead(**response.json())

    def list_video_series(
            self,
            search_text: Optional[str] = None,
            skip: int = 0,
            limit: int = 10,
            sort_by_field: str = "created_at",
            sort_order: str = "desc"
    ) -> List[PublicAPIGeneratedFacelessVideoSeriesRead]:
        """
        List video series with optional filtering and pagination.

        :param search_text: Search in series names
        :param skip: Number of items to skip
        :param limit: Maximum number of items to return
        :param sort_by_field: Field to sort by
        :param sort_order: Sort order ('asc' or 'desc')
        :return: List of video series
        """
        params = {
            "skip": skip,
            "limit": limit,
            "sort_by_field": sort_by_field,
            "sort_order": sort_order
        }

        if search_text:
            params["search_text"] = search_text

        response = self._make_request("GET", "/video-series/", params=params)
        return [PublicAPIGeneratedFacelessVideoSeriesRead(**item) for item in response.json()]

    def get_video_series(self, series_id: str) -> PublicAPIGeneratedFacelessVideoSeriesRead:
        """
        Get a specific video series by ID.

        :param series_id: ID of the video series
        :return: Video series details
        """
        response = self._make_request("GET", f"/video-series/{series_id}")
        return PublicAPIGeneratedFacelessVideoSeriesRead(**response.json())

    def update_video_series(
            self,
            series_id: str,
            payload: PublicAPIGeneratedFacelessVideoSeriesUpdate
    ) -> PublicAPIGeneratedFacelessVideoSeriesRead:
        """
        Update an existing video series.

        :param series_id: ID of the video series to update
        :param payload: Update data
        :return: Updated video series
        """
        json_data = payload.model_dump_json(exclude_unset=True)

        response = self._make_request(
            "PUT",
            f"/video-series/{series_id}",
            data=json_data,
            headers={"Content-Type": "application/json"}
        )

        return PublicAPIGeneratedFacelessVideoSeriesRead(**response.json())

    def delete_video_series(self, series_id: str) -> dict:
        """
        Delete a video series (soft delete).

        :param series_id: ID of the video series to delete
        :return: Success message
        """
        response = self._make_request("DELETE", f"/video-series/{series_id}")
        return response.json()

    # ---------------------------------------------------------
    # Video Tasks Methods
    # ---------------------------------------------------------
    def generate_video(self, series_id: str) -> PublicAPIVideoTaskResponse:
        """
        Generate a new video from the specified video series.

        :param series_id: ID of the video series to generate from
        :return: Video generation task details
        """
        response = self._make_request("POST", f"/video-tasks/{series_id}/generate")
        return PublicAPIVideoTaskResponse(**response.json())

    def get_video_task(self, task_id: str) -> PublicAPIVideoTaskResponse:
        """
        Get the status and details of a video generation task.

        :param task_id: ID of the video generation task
        :return: Task status and details
        """
        response = self._make_request("GET", f"/video-tasks/{task_id}")
        return PublicAPIVideoTaskResponse(**response.json())

    def list_video_tasks(
            self,
            series_id: Optional[str] = None,
            status: Optional[GeneratedFacelessVideoProcessState] = None,
            skip: int = 0,
            limit: int = 10,
            sort_order: str = "desc"
    ) -> List[PublicAPIVideoTaskResponse]:
        """
        List video generation tasks with optional filtering.

        :param series_id: Filter by video series ID
        :param status: Filter by task status
        :param skip: Number of items to skip
        :param limit: Maximum number of items to return
        :param sort_order: Sort order ('asc' or 'desc')
        :return: List of video tasks
        """
        params = {
            "skip": skip,
            "limit": limit,
            "sort_order": sort_order
        }

        if series_id:
            params["series_id"] = series_id

        if status:
            params["status"] = status.value

        response = self._make_request("GET", "/video-tasks/", params=params)
        return [PublicAPIVideoTaskResponse(**item) for item in response.json()]

    def get_video_task_details(self, task_id: str) -> dict:
        """
        Get detailed information about a video generation task.

        :param task_id: ID of the video generation task
        :return: Detailed task information including errors and results
        """
        response = self._make_request("GET", f"/video-tasks/{task_id}/details")
        return response.json()

    def cancel_video_task(self, task_id: str) -> dict:
        """
        Cancel a video generation task.

        :param task_id: ID of the video generation task to cancel
        :return: Success message
        """
        response = self._make_request("DELETE", f"/video-tasks/{task_id}")
        return response.json()

    # ---------------------------------------------------------
    # Convenience Methods
    # ---------------------------------------------------------
    def wait_for_video_completion(
            self,
            task_id: str,
            poll_interval: int = 10,
            timeout: int = 300
    ) -> PublicAPIVideoTaskResponse:
        """
        Wait for a video generation task to complete.

        :param task_id: ID of the video generation task
        :param poll_interval: Seconds to wait between status checks
        :param timeout: Maximum seconds to wait before timing out
        :return: Final task status
        :raises: TimeoutError if task doesn't complete within timeout
        """
        import time

        start_time = time.time()

        while time.time() - start_time < timeout:
            task = self.get_video_task(task_id)

            if task.status in ["COMPLETE", "ERROR", "NO_CREDITS"]:
                return task

            time.sleep(poll_interval)

        raise TimeoutError(f"Video generation task {task_id} did not complete within {timeout} seconds")

    def create_video_series_and_generate(
            self,
            series_config: PublicAPIGeneratedFacelessVideoSeriesCreate,
            wait_for_completion: bool = True,
            poll_interval: int = 10,
            timeout: int = 300
    ) -> tuple[PublicAPIGeneratedFacelessVideoSeriesRead, PublicAPIVideoTaskResponse]:
        """
        Create a video series and immediately generate a video from it.

        :param series_config: Video series configuration
        :param wait_for_completion: Whether to wait for video generation to complete
        :param poll_interval: Seconds between status checks if waiting
        :param timeout: Maximum seconds to wait for completion
        :return: Tuple of (created_series, task_result)
        """
        # Create the series
        series = self.create_video_series(series_config)

        # Generate a video
        task = self.generate_video(series.id)

        # Wait for completion if requested
        if wait_for_completion:
            task = self.wait_for_video_completion(task.task_id, poll_interval, timeout)

        return series, task