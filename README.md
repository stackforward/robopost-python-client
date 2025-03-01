# Robopost Client

**Robopost** is an AI-driven social media management platform that consolidates all your social channels into one place. With over 20,000 users, it helps businesses, agencies, and freelancers automate and schedule posts, generate AI-based content, and streamline teamwork. For more information, visit [robopost.app](https://robopost.app/).

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

Below are a few common scenarios. For each, we’ll show how to upload media first (when needed) and then use the returned `storage_object_id`.

---

#### A. Create a Post to Be Scheduled **Now**

```python
from datetime import datetime, timezone
from robopost_client import PublicAPIScheduledPostCreateHTTPPayload

utc_now = datetime.now(timezone.utc).isoformat()

payload_now = PublicAPIScheduledPostCreateHTTPPayload(
    text="Posting now via Robopost!",
    channel_ids=["channel_123"],  # Replace with your channel ID
    schedule_at=utc_now,          # Schedules as soon as possible (UTC)
    is_draft=False
)

scheduled_post_now = client.create_scheduled_posts(payload_now)
print("Scheduled Immediately:", scheduled_post_now)
```

---

#### B. Create a **Recurring** Post That Repeats **DAILY**

```python
from datetime import datetime, timezone
from robopost_client import PublicAPIScheduledPostCreateHTTPPayload

first_post_time = datetime(2025, 3, 1, 10, 0, 0, tzinfo=timezone.utc).isoformat()
payload_recur = PublicAPIScheduledPostCreateHTTPPayload(
    text="Daily recurring post!",
    channel_ids=["channel_123"],   # Replace with your channel ID
    schedule_at=first_post_time,   # First run time in UTC
    is_recur=True,                 # Make this post recur
    # You could optionally set an end time:
    # recur_until_dt=datetime(2025, 12, 31, tzinfo=timezone.utc).isoformat(),
    # recur_until_dt_enabled=True,
)

scheduled_posts_recur = client.create_scheduled_posts(payload_recur)
print("Recurring Posts:", scheduled_posts_recur)
```

---

#### C. Create a Post With **3 Images**

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

#### D. Create a Post With **1 Video**

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

## License

MIT