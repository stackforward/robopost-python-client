# Robopost Python Client

**Robopost** is an AI-driven social media management platform that consolidates all your social channels into one place. It helps businesses, agencies, and freelancers automate and schedule posts, generate AI-based content, and streamline teamwork. For more information, visit [robopost.app](https://robopost.app/).

This **Robopost Client** library provides convenient Python methods to:
- **Manage Media:** Upload, list, get, and delete images or videos.
- **Schedule Posts:** Create simple, recurring, and AI-enhanced posts.
- **Generate AI Videos:** Create and manage automated faceless video series for platforms like TikTok, Reels, and Shorts.

> **Note:** All date/time fields must be provided in **UTC**.

---

## Installation

Install the library directly from GitHub:

```bash
pip install git+https://github.com/stackforward/robopost-python-client.git
```

---

## Getting Started

### 1. Initializing the Client

Instantiate the `RobopostClient` by providing your API key. You can find your API key in the Robopost dashboard.

```python
from robopost_client import RobopostClient

# Replace 'YOUR_API_KEY' with your actual API key.
client = RobopostClient(apikey="YOUR_API_KEY")
```

### 2. Finding Channel IDs

To specify which channels to post to, you’ll need their unique IDs. In the **Robopost dashboard**:

1.  Go to the **Channels** page.
2.  Click on a channel to view its details.
3.  Click **Copy ID** to get the channel’s identifier.

---

## Core Features

### 1. Media Management

You can manage your media assets by uploading, listing, retrieving, and deleting them.

#### A. Upload Media

Use `upload_media` to upload an image or video from a local file. The returned `storage_object_id` is used to attach the media to a post.

```python
media = client.upload_media("path/to/your/file.jpg")
print(f"Uploaded Media ID: {media.id}, Storage Object ID: {media.storage_object_id}")
```

#### B. List, Get, and Delete Media

Manage your existing media library with these methods.

```python
# List the first 10 media items
media_list = client.list_media(limit=10)
print(f"Found {len(media_list)} media items.")

if media_list:
    media_id_to_manage = media_list[0].id

    # Get a specific media item by its ID
    specific_media = client.get_media(media_id_to_manage)
    print("Retrieved media:", specific_media)

    # Delete a media item
    delete_response = client.delete_media(media_id_to_manage)
    print("Delete response:", delete_response)
```

---

### 2. Scheduled Posts

Create and schedule content for your social channels.

#### A. Create a Simple Post

To post immediately, simply provide the text and channel IDs.

```python
from robopost_client import PublicAPIScheduledPostCreateHTTPPayload

payload_now = PublicAPIScheduledPostCreateHTTPPayload(
    text="Posting now via the Robopost API!",
    channel_ids=["channel_123"],  # Replace with your channel ID
)
scheduled_post = client.create_scheduled_posts(payload_now)
print("Scheduled Immediately:", scheduled_post)
```

#### B. Schedule a Post for Later

Set `schedule_at` to a future UTC datetime string.

```python
from datetime import datetime, timedelta, timezone

future_time = datetime.now(timezone.utc) + timedelta(hours=2)
payload_later = PublicAPIScheduledPostCreateHTTPPayload(
    text="This post is scheduled for later!",
    channel_ids=["channel_123"],
    schedule_at=future_time,
)
scheduled_post_later = client.create_scheduled_posts(payload_later)
print("Scheduled for Later:", scheduled_post_later)
```

#### C. Create a Post with Media

Attach previously uploaded media using `image_object_ids` or `video_object_id`. Alternatively, provide direct `image_urls`, a `video_url`, or a `gif_url`, and Robopost will handle the download and processing.

```python
# Example using a direct image URL
payload_with_media = PublicAPIScheduledPostCreateHTTPPayload(
    text="Check out this image from a URL!",
    channel_ids=["channel_123"],
    image_urls=["https://example.com/images/scenery.jpg"],
)
scheduled_post_media = client.create_scheduled_posts(payload_with_media)
print("Scheduled Post with Media:", scheduled_post_media)
```

#### D. Create a Recurring Post

Set `is_recur=True` and specify an interval. The `schedule_at` field determines the time of the first post.

```python
from robopost_client import AutomationRecurInterval

first_post_time = datetime(2025, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
payload_recur = PublicAPIScheduledPostCreateHTTPPayload(
    text="This is a daily recurring post!",
    channel_ids=["channel_123"],
    schedule_at=first_post_time,
    is_recur=True,
    recur_interval=AutomationRecurInterval.DAILY,
)
scheduled_posts_recur = client.create_scheduled_posts(payload_recur)
print("Recurring Post Scheduled:", scheduled_posts_recur)
```

#### E. Advanced Recurring Posts (with AI)

Enhance recurring posts with AI-generated content. For each recurrence, Robopost can rephrase the text and/or generate a new image. You can also set an end date.

```python
from robopost_client import PostAIGenerateVoiceTone, AIImageModel

payload_advanced_recur = PublicAPIScheduledPostCreateHTTPPayload(
    text="This is a recurring post with AI enhancements! #AI #automation",
    channel_ids=["channel_123"],
    schedule_at=first_post_time,
    is_recur=True,
    recur_interval=AutomationRecurInterval.DAILY,
    
    # Re-phrase the text with a 'witty' tone for each new post
    recur_rephrase_text_with_ai=True,
    recur_rephrase_text_with_ai_tone=PostAIGenerateVoiceTone.WITTY,
    
    # Generate a new DALL-E image for each new post
    recur_generate_new_ai_image=True,
    recur_generate_new_ai_image_model=AIImageModel.DALLE,
    
    # Stop the recurrence after a specific date
    recur_until_dt_enabled=True,
    recur_until_dt=datetime(2025, 2, 1, 0, 0, 0, tzinfo=timezone.utc),
    
    # Optionally, add this post to a collection
    post_collection_id="collection_abc"
)
scheduled_advanced_recur = client.create_scheduled_posts(payload_advanced_recur)
print("Advanced Recurring Post Scheduled:", scheduled_advanced_recur)
```

#### F. Platform-Specific Settings

Customize posts for each social media platform by providing a settings object in the payload.

**Example: Schedule an Instagram Reel and a YouTube Short**

```python
from robopost_client import (
    InstagramSettings, InstagramPostType,
    YoutubeSettings, YoutubeVideoType, YoutubePrivacyStatus
)

# Assume you have a video's storage_object_id from uploading it
video_id = "your_video_storage_object_id"

payload_reels = PublicAPIScheduledPostCreateHTTPPayload(
    text="Check out my new short-form video! #reel #short",
    channel_ids=["instagram_channel_id", "youtube_channel_id"],
    video_object_id=video_id,
    
    instagram_settings=InstagramSettings(postType=InstagramPostType.REELS),
    
    youtube_settings=YoutubeSettings(
        videoTitle="My Awesome New Short",
        videoType=YoutubeVideoType.SHORT,
        videoDescription="A detailed description for my YouTube Short.",
        videoPrivacyStatus=YoutubePrivacyStatus.PUBLIC
    ),
)
scheduled_reels = client.create_scheduled_posts(payload_reels)
print("Scheduled Instagram Reel and YouTube Short:", scheduled_reels)
```

---

### 3. AI Faceless Video Generation

Automate the creation of short-form "faceless" videos. The process involves two steps:
1.  **Create a Video Series:** A template that defines the content, style, voice, captions, and other properties for your videos.
2.  **Generate a Video:** Trigger the creation of a new video based on your series template.

#### A. Create a Video Series

Define a template for your videos. You can even make the series recurring to automatically generate and post new videos on a schedule.

```python
from robopost_client import (
    PublicAPIGeneratedFacelessVideoSeriesCreate,
    GeneratedFacelessVideoSeriesContentType,
    GeneratedFacelessVideoStyle,
    AIVoice,
    GeneratedVideoFormat,
    AutomationRecurInterval
)

series_config = PublicAPIScheduledPostCreateHTTPPayload(
    name="Daily Fun Facts",
    content_type=GeneratedFacelessVideoSeriesContentType.FUN_FACTS,
    style=GeneratedFacelessVideoStyle.FANTASY_CONCEPT_ART,
    voice=AIVoice.ARIA.value,
    format=GeneratedVideoFormat.PORTRAIT,  # For TikTok/Reels/Shorts
    max_duration=59,
    
    # Automatically create and schedule a post when a video is ready
    create_scheduled_post=True,
    channel_ids=["tiktok_channel_123", "instagram_channel_456"],
    
    # Make this series generate a new video every day at a specific time
    is_recur=True,
    recur_interval=AutomationRecurInterval.DAILY_SPECIFIC_TIME_SLOTS,
    recur_interval_time_slots=[datetime(2025, 1, 1, 9, 30, 0, tzinfo=timezone.utc).isoformat()],
    timezone="America/New_York"
)

video_series = client.create_video_series(series_config)
print("Created Video Series:", video_series)
```

#### B. Manually Generate a Video from a Series

If your series is not recurring, or you want to generate an extra video, you can trigger it manually.

```python
# Manually trigger a video generation for the series we just created
task = client.generate_video(series_id=video_series.id)
print("Started video generation task:", task)
```

#### C. Check Generation Status & Wait for Completion

Video generation is an asynchronous process. You can poll the task status or use the convenient `wait_for_video_completion` helper method.

```python
try:
    # This method will poll the API until the task is complete, fails, or times out
    completed_task = client.wait_for_video_completion(
        task_id=task.task_id,
        poll_interval=15,  # Check every 15 seconds
        timeout=600        # Wait for a maximum of 10 minutes
    )
    print(f"Task {completed_task.task_id} finished with status: {completed_task.status}")

    if completed_task.status == "COMPLETE":
        # Get full details, including the final video URL and any generated text
        details = client.get_video_task_details(task.task_id)
        print("Video details:", details)

except TimeoutError as e:
    print(e)
```

#### D. Manage Video Series

You can also list, update, and delete your video series.

```python
# List all video series
all_series = client.list_video_series()
print(f"Found {len(all_series)} video series.")

# Update a series (e.g., change the voice)
from robopost_client import PublicAPIGeneratedFacelessVideoSeriesUpdate, AIVoice
update_payload = PublicAPIGeneratedFacelessVideoSeriesUpdate(voice=AIVoice.BILL.value)
updated_series = client.update_video_series(series_id=video_series.id, payload=update_payload)
print("Updated series voice to:", updated_series.voice)

# Delete a series
client.delete_video_series(series_id=video_series.id)
print(f"Series {video_series.id} has been deleted.")
```

---

## Error Handling

The client raises custom exceptions for API-related errors. It's best practice to wrap your API calls in a `try...except` block to handle potential issues gracefully.

- `RobopostPlanLimitError`: Raised when your request exceeds a limit of your current plan (e.g., creating too many posts).
- `RobopostAPIError`: A general exception for other API errors (e.g., invalid input, authentication failure).

```python
from robopost_client import RobopostAPIError, RobopostPlanLimitError

try:
    # An example API call that might fail
    client.create_scheduled_posts(some_invalid_payload)

except RobopostPlanLimitError as e:
    print(f"Plan limit reached: {e.message}")
    print(f"Limit: {e.limit}, Current Usage: {e.current_usage}")

except RobopostAPIError as e:
    print(f"An API error occurred (Status Code: {e.status_code}): {e.message}")
    print(f"Full response data: {e.response_data}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

---

## License

MIT