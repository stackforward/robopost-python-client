# Robopost Client

**Robopost** is an AI-driven social media management platform that consolidates all your social channels into one place. It helps businesses, agencies, and freelancers automate and schedule posts, generate AI-based content, and streamline teamwork. For more information, visit [robopost.app](https://robopost.app/).

This **Robopost Client** library provides convenient Python methods to:
- **Upload Media** (images or videos)
- **Create Scheduled Posts** (including drafts and recurring posts)

> **Note:** All date/time fields must be provided in **UTC**.

---

## Installation

Install the required dependencies using pip:

```bash
pip install robopost-client
```

---

## Usage

### 1. Initializing the Client

Instantiate the `RobopostClient` by providing your API key. You can also optionally override the default base URL.

```python
from robopost_client import RobopostClient

# Replace 'YOUR_API_KEY' with your actual API key.
client = RobopostClient(apikey="YOUR_API_KEY")
```

### 2. Uploading Media

Use the `upload_media` method to upload an image or video. Simply pass the local file path to the file you want to upload; the API key is included automatically as a query parameter.

```python
media = client.upload_media("path/to/your/file.jpg")
print("Uploaded Media:", media)
```

> After uploading a file, **note the `storage_object_id`** in the returned `PublicAPIMediaRead` object. You will use this value as either the **`video_object_id`** or one of the **`image_object_ids`** in your scheduled posts.

### 3. Finding Channel IDs

To specify the `channel_ids` for your posts, you’ll need the IDs of each channel. In the **Robopost dashboard**:

1. Go to **Channels**  
2. Click on a specific channel to view its details  
3. Click **Copy ID** to get the channel’s unique identifier  

Use these channel IDs in the `channel_ids` list when creating scheduled posts.

### 4. Creating Scheduled Posts

All scheduled times must be in UTC. Build a payload using the `PublicAPIScheduledPostCreateHTTPPayload` Pydantic model, then pass that payload to `create_scheduled_posts`.

**Important:**  
- The `schedule_at` field is required (with a default of the current UTC time).  
- When scheduling a recurring post (i.e. `is_recur=True`), you **must** also pass a valid `recur_interval` along with the recurrence fields.  
- For recurrence using either `DAILY_SPECIFIC_TIME_SLOTS` or `WEEKLY_SPECIFIC_TIME_SLOTS`, you must fill the `recur_interval_time_slots` field with full ISO 8601 datetime strings.  
  - When using `DAILY_SPECIFIC_TIME_SLOTS`, only the time portion will be used by the API.
  - When using `WEEKLY_SPECIFIC_TIME_SLOTS`, both the day of the week and time are taken into account.

Below are a few common scenarios:

---

#### A. Create a Post to Be Scheduled **Now**

*(This example uses the default value for `schedule_at`, which is the current UTC datetime.)*

```python
from robopost_client import PublicAPIScheduledPostCreateHTTPPayload
# No need to explicitly set schedule_at if posting now since it defaults to datetime.now()
payload_now = PublicAPIScheduledPostCreateHTTPPayload(
    text="Posting now via Robopost!",
    channel_ids=["channel_123"],  # Replace with your channel ID
    is_draft=False
)

scheduled_post_now = client.create_scheduled_posts(payload_now)
print("Scheduled Immediately:", scheduled_post_now)
```

---

#### B. Create a Post to Be Scheduled **Later**

*(Explicitly set `schedule_at` to a future UTC datetime.)*

```python
from datetime import datetime, timedelta, timezone
from robopost_client import PublicAPIScheduledPostCreateHTTPPayload

# Schedule for 2 hours later in UTC
future_time = (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat()
payload_later = PublicAPIScheduledPostCreateHTTPPayload(
    text="Scheduled for later via Robopost!",
    channel_ids=["channel_123"],  # Replace with your channel ID
    schedule_at=future_time,
    is_draft=False
)

scheduled_post_later = client.create_scheduled_posts(payload_later)
print("Scheduled for Later:", scheduled_post_later)
```

---

#### C. Create a **Recurring** Post (Standard)

When using recurring posts, set `is_recur=True` and provide a valid `recur_interval`. In this example, we use a standard DAILY interval.

```python
from datetime import datetime, timezone
from robopost_client import PublicAPIScheduledPostCreateHTTPPayload, AutomationRecurInterval

first_post_time = datetime(2025, 3, 1, 10, 0, 0, tzinfo=timezone.utc).isoformat()
payload_recur = PublicAPIScheduledPostCreateHTTPPayload(
    text="Recurring post via Robopost!",
    channel_ids=["channel_123"],  # Replace with your channel ID
    schedule_at=first_post_time,   # First run time in UTC
    is_recur=True,                 # Enable recurrence
    recur_interval=AutomationRecurInterval.DAILY,  # Standard daily recurrence
)

scheduled_posts_recur = client.create_scheduled_posts(payload_recur)
print("Recurring Posts (Standard):", scheduled_posts_recur)
```

---

#### D. Create a **Recurring** Post Using DAILY_SPECIFIC_TIME_SLOTS

When using `DAILY_SPECIFIC_TIME_SLOTS`, set `is_recur=True`, use `AutomationRecurInterval.DAILY_SPECIFIC_TIME_SLOTS`, and provide a list of ISO 8601 datetime strings in `recur_interval_time_slots`. Note that the API will only use the time portion.

```python
from datetime import datetime, timezone
from robopost_client import PublicAPIScheduledPostCreateHTTPPayload, AutomationRecurInterval

first_post_time = datetime(2025, 3, 1, 8, 0, 0, tzinfo=timezone.utc).isoformat()
payload_daily_slots = PublicAPIScheduledPostCreateHTTPPayload(
    text="Recurring post with daily specific time slots!",
    channel_ids=["channel_123"],  # Replace with your channel ID
    schedule_at=first_post_time,   # First run time in UTC
    is_recur=True,                 # Enable recurrence
    recur_interval=AutomationRecurInterval.DAILY_SPECIFIC_TIME_SLOTS,
    recur_interval_time_slots=[
        datetime(2025, 3, 1, 9, 0, 0, tzinfo=timezone.utc).isoformat(),
        datetime(2025, 3, 1, 15, 0, 0, tzinfo=timezone.utc).isoformat()
    ]
)

scheduled_posts_daily = client.create_scheduled_posts(payload_daily_slots)
print("Recurring Posts (Daily Specific Slots):", scheduled_posts_daily)
```

---

#### E. Create a **Recurring** Post Using WEEKLY_SPECIFIC_TIME_SLOTS

For `WEEKLY_SPECIFIC_TIME_SLOTS`, set `is_recur=True`, use `AutomationRecurInterval.WEEKLY_SPECIFIC_TIME_SLOTS`, and provide a list of ISO 8601 datetime strings in `recur_interval_time_slots`. In this case, the API considers both the day of the week and time.

```python
from datetime import datetime, timezone
from robopost_client import PublicAPIScheduledPostCreateHTTPPayload, AutomationRecurInterval

first_post_time = datetime(2025, 3, 1, 10, 0, 0, tzinfo=timezone.utc).isoformat()
payload_weekly_slots = PublicAPIScheduledPostCreateHTTPPayload(
    text="Recurring post with weekly specific time slots!",
    channel_ids=["channel_123"],  # Replace with your channel ID
    schedule_at=first_post_time,   # First run time in UTC
    is_recur=True,                 # Enable recurrence
    recur_interval=AutomationRecurInterval.WEEKLY_SPECIFIC_TIME_SLOTS,
    recur_interval_time_slots=[
        datetime(2025, 3, 3, 10, 0, 0, tzinfo=timezone.utc).isoformat(),  # Example: Monday or Tuesday at 10:00 UTC
        datetime(2025, 3, 5, 14, 0, 0, tzinfo=timezone.utc).isoformat()   # Example: Wednesday or Thursday at 14:00 UTC
    ]
)

scheduled_posts_weekly = client.create_scheduled_posts(payload_weekly_slots)
print("Recurring Posts (Weekly Specific Slots):", scheduled_posts_weekly)
```

---

#### F. Create a Post With **3 Images**

**Step 1: Upload the images (one by one) and collect their `storage_object_id`.**

```python
media_1 = client.upload_media("path/to/image1.jpg")
media_2 = client.upload_media("path/to/image2.jpg")
media_3 = client.upload_media("path/to/image3.jpg")

print("Image #1 ID:", media_1.storage_object_id)
print("Image #2 ID:", media_2.storage_object_id)
print("Image #3 ID:", media_3.storage_object_id)
```

**Step 2: Create the scheduled post referencing these IDs.**

```python
from robopost_client import PublicAPIScheduledPostCreateHTTPPayload

payload_with_images = PublicAPIScheduledPostCreateHTTPPayload(
    text="Check out these 3 images!",
    channel_ids=["channel_123"],  # Replace with your channel ID
    image_object_ids=[
        media_1.storage_object_id,
        media_2.storage_object_id,
        media_3.storage_object_id,
    ],
    is_draft=False
)

scheduled_posts_images = client.create_scheduled_posts(payload_with_images)
print("Post with Images:", scheduled_posts_images)
```

---

#### G. Create a Post With **1 Video**

**Step 1: Upload a video and retrieve its `storage_object_id`.**

```python
video_media = client.upload_media("path/to/video.mp4")
print("Video ID:", video_media.storage_object_id)
```

**Step 2: Create the scheduled post referencing that video ID.**

```python
from robopost_client import PublicAPIScheduledPostCreateHTTPPayload

payload_with_video = PublicAPIScheduledPostCreateHTTPPayload(
    text="Here's a demo video!",
    channel_ids=["channel_123"],       # Replace with your channel ID
    video_object_id=video_media.storage_object_id,
    is_draft=False
)

scheduled_posts_video = client.create_scheduled_posts(payload_with_video)
print("Post with Video:", scheduled_posts_video)
```

---

### 5. Specifying Social Media–Specific Settings

Robopost supports additional fields that allow you to customize posts for each social media platform. These fields can be found in the following Pydantic models:

- **`FacebookSettings`**  
  - `postType` → `FacebookPostType.POST` or `FacebookPostType.REELS`  
- **`InstagramSettings`**  
  - `postType` → `InstagramPostType.POST`, `InstagramPostType.REELS`, or `InstagramPostType.STORIES`  
- **`PinterestSettings`**  
  - `pinTitle`, `destinationLink`  
- **`WordpressSettings`**  
  - `postTitle`, `postText`, `postSlug`, `postType`, `postCategories`, `postTags`, etc.  
- **`YoutubeSettings`**  
  - `videoObject`, `videoTitle`, `videoType`, `videoDescription`, `videoPrivacyStatus`, etc.  
- **`TikTokSettings`**  
  - `title`, `privacyLevel`, `disableDuet`, `disableComment`, etc.  
- **`GMBSettings`**  
  - `postTopicType` (STANDARD, OFFER, EVENT), `offerTitle`, `eventTitle`, `ctaButtonActionType`, etc.

Each of these settings objects is optional. If you do not provide them, the fields default to safe values (e.g., `POST` type for Facebook and Instagram). However, if you want to post Facebook Reels or Instagram Stories, or if you need to specify additional fields for WordPress or GMB, you can do so by providing the respective settings object in your payload.

#### Example: Using **Facebook Reels** and **Instagram Reels**

```python
from robopost_client import (
    PublicAPIScheduledPostCreateHTTPPayload,
    FacebookSettings,
    FacebookPostType,
    InstagramSettings,
    InstagramPostType
)

payload_social_settings = PublicAPIScheduledPostCreateHTTPPayload(
    text="Testing Reels on Facebook and Instagram!",
    channel_ids=["facebook_channel_id", "instagram_channel_id"],
    facebook_settings=FacebookSettings(postType=FacebookPostType.REELS),
    instagram_settings=InstagramSettings(postType=InstagramPostType.REELS),
)

scheduled_reels = client.create_scheduled_posts(payload_social_settings)
print("Scheduled Facebook & Instagram Reels:", scheduled_reels)
```

#### Example: Adding Additional **Wordpress** Fields

```python
from robopost_client import (
    PublicAPIScheduledPostCreateHTTPPayload,
    WordpressSettings,
    WordpressPostType
)

payload_wordpress = PublicAPIScheduledPostCreateHTTPPayload(
    text="Check out my WordPress post!",
    channel_ids=["wordpress_channel_id"],
    wordpress_settings=WordpressSettings(
        postTitle="My Awesome Post",
        postText="Detailed blog content goes here...",
        postSlug="my-awesome-post",
        postType=WordpressPostType.POST,
        postCategories=["Tech", "Python"],
        postTags=["robopost", "automation"]
    ),
)

scheduled_wordpress = client.create_scheduled_posts(payload_wordpress)
print("WordPress Post Scheduled:", scheduled_wordpress)
```

#### Example: Setting **YouTube** Privacy and Video Type

```python
from robopost_client import (
    PublicAPIScheduledPostCreateHTTPPayload,
    YoutubeSettings,
    YoutubeVideoType,
    YoutubePrivacyStatus
)

payload_youtube = PublicAPIScheduledPostCreateHTTPPayload(
    text="My new YouTube short!",
    channel_ids=["youtube_channel_id"],
    youtube_settings=YoutubeSettings(
        videoObject="SOME_VIDEO_OBJECT_ID",
        videoTitle="Behind the Scenes",
        videoType=YoutubeVideoType.SHORT,  # or VIDEO
        videoDescription="A fun behind-the-scenes short video.",
        videoPrivacyStatus=YoutubePrivacyStatus.UNLISTED
    ),
)

scheduled_youtube = client.create_scheduled_posts(payload_youtube)
print("YouTube Short Scheduled:", scheduled_youtube)
```


### Example: Standard GMB Post

Use the `GMBPostTopicType.STANDARD` and provide any additional CTA button fields as needed.

```python
from datetime import datetime, timezone
from robopost_client import (
    PublicAPIScheduledPostCreateHTTPPayload,
    GMBSettings,
    GMBPostTopicType,
    GMBCTAButtonActionType
)

payload_gmb_standard = PublicAPIScheduledPostCreateHTTPPayload(
    text="Come visit our new store location!",
    channel_ids=["gmb_channel_id"],  # Replace with your GMB channel ID
    gmb_settings=GMBSettings(
        postTopicType=GMBPostTopicType.STANDARD,
        ctaButtonActionType=GMBCTAButtonActionType.CALL,
        ctaUrl="tel:+1234567890"
    ),
    schedule_at=datetime.now(timezone.utc).isoformat(),
    is_draft=False
)

scheduled_gmb_standard = client.create_scheduled_posts(payload_gmb_standard)
print("Scheduled Standard GMB Post:", scheduled_gmb_standard)
```

This creates a **standard** GMB post with a “Call” button that dials the specified phone number.

---

### Example: GMB Offer Post

Use the `GMBPostTopicType.OFFER` and specify fields for offers (like `offerTitle`, `offerCouponCode`, etc.). You can also add optional CTA buttons (e.g., `BOOK`, `ORDER`, `SHOP`, etc.).

```python
from datetime import datetime, timezone
from robopost_client import (
    PublicAPIScheduledPostCreateHTTPPayload,
    GMBSettings,
    GMBPostTopicType,
    GMBCTAButtonActionType
)

offer_start = datetime(2025, 3, 10, 0, 0, 0, tzinfo=timezone.utc)
offer_end = datetime(2025, 3, 12, 23, 59, 59, tzinfo=timezone.utc)

payload_gmb_offer = PublicAPIScheduledPostCreateHTTPPayload(
    text="Get 50% off your purchase this weekend!",
    channel_ids=["gmb_channel_id"],  # Replace with your GMB channel ID
    gmb_settings=GMBSettings(
        postTopicType=GMBPostTopicType.OFFER,
        offerTitle="50% OFF Weekend Special",
        offerCouponCode="WEEKEND50",
        offerRedeemOnlineUrl="https://example.com/discount",
        offerTermsConditions="Limited time offer. One per customer.",
        offerStartDt=offer_start,
        offerEndDt=offer_end,
        ctaButtonActionType=GMBCTAButtonActionType.SHOP,
        ctaUrl="https://example.com/shop"
    ),
    schedule_at=datetime.now(timezone.utc).isoformat(),
    is_draft=False
)

scheduled_gmb_offer = client.create_scheduled_posts(payload_gmb_offer)
print("Scheduled GMB Offer Post:", scheduled_gmb_offer)
```

This creates an **offer**-type GMB post, displays the coupon code and offer details, and includes a “Shop” CTA button that links to your e-commerce or landing page.

---

### Example: GMB Event Post

Use the `GMBPostTopicType.EVENT` and provide event details (like `eventTitle`, `eventStartDt`, `eventEndDt`). You can also attach a CTA button.

```python
from datetime import datetime, timezone
from robopost_client import (
    PublicAPIScheduledPostCreateHTTPPayload,
    GMBSettings,
    GMBPostTopicType,
    GMBCTAButtonActionType
)

event_start = datetime(2025, 4, 15, 9, 0, 0, tzinfo=timezone.utc)
event_end = datetime(2025, 4, 15, 17, 0, 0, tzinfo=timezone.utc)

payload_gmb_event = PublicAPIScheduledPostCreateHTTPPayload(
    text="Join our grand opening event!",
    channel_ids=["gmb_channel_id"],  # Replace with your GMB channel ID
    gmb_settings=GMBSettings(
        postTopicType=GMBPostTopicType.EVENT,
        eventTitle="Grand Opening",
        eventStartDt=event_start,
        eventEndDt=event_end,
        ctaButtonActionType=GMBCTAButtonActionType.LEARN_MORE,
        ctaUrl="https://example.com/events/grand-opening"
    ),
    schedule_at=datetime.now(timezone.utc).isoformat(),
    is_draft=False
)

scheduled_gmb_event = client.create_scheduled_posts(payload_gmb_event)
print("Scheduled GMB Event Post:", scheduled_gmb_event)
```

This creates an **event**-type GMB post, including start/end times and a link to “Learn More.”

---

## GMB Fields Overview

Below are the main fields in `GMBSettings`. You can customize them based on the type of GMB post you’re creating:

- **`postTopicType`**  
  - `STANDARD`, `OFFER`, `EVENT`

- **Offer Fields**  
  - `offerTitle`, `offerCouponCode`, `offerRedeemOnlineUrl`, `offerTermsConditions`, `offerStartDt`, `offerEndDt`

- **Event Fields**  
  - `eventTitle`, `eventStartDt`, `eventEndDt`

- **CTA Fields**  
  - `ctaButtonActionType`: Options include `ACTION_TYPE_UNSPECIFIED`, `BOOK`, `ORDER`, `SHOP`, `LEARN_MORE`, `SIGN_UP`, `CALL`.  
  - `ctaUrl`: Link for your CTA button (e.g., phone number, booking page, website).

> **Note:** The Google Business Profile (formerly Google My Business) API imposes specific rules on how offers, events, and standard posts are displayed. Make sure to follow Google’s [Business Profile Posting Guidelines](https://support.google.com/business/answer/10394711) for compliance and best practices.

---

## License

MIT
