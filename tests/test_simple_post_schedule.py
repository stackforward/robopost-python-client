import os
from datetime import datetime, timedelta, timezone
from robopost_client import (
    RobopostClient,
    PublicAPIScheduledPostCreateHTTPPayload,
    AutomationRecurInterval,
    InstagramSettings,
    InstagramPostType,
    YoutubeSettings,
    YoutubeVideoType,
    YoutubePrivacyStatus
)


def main():
    # Instantiate the client with your API key
    api_key = "3f60b32d-1d38-4ab3-bfc5-7e5f683870ab"  # Replace with your actual API key
    # Define channel IDs for Instagram and YouTube
    instagram_channel_id = "066617a4-1e4d-40ab-ac9d-0e4c6521814e"
    youtube_channel_id = "c0d7fb13-fc02-4db8-b439-e046e9bd52c8"

    api_url = "http://localhost:8093/v1"
    client = RobopostClient(apikey=api_key, base_url=api_url)

    # --------------------------------------
    # Example 1: Post using an image
    # --------------------------------------
    # Upload a JPG image
    image_path = "images/sample1.jpg"
    print(f"Uploading image: {image_path}")
    media = client.upload_media(image_path)
    print("Uploaded media:", media)

    # Schedule a post to be published in 5 seconds from now
    schedule_time = (datetime.now(timezone.utc) + timedelta(seconds=5)).isoformat()
    payload = PublicAPIScheduledPostCreateHTTPPayload(
        text="Test scheduled post in 5 seconds!",
        image_object_ids=[media.storage_object_id],
        channel_ids=[instagram_channel_id],
        schedule_at=schedule_time,
        is_draft=False
    )

    scheduled_posts = client.create_scheduled_posts(payload)
    print("Scheduled posts:", scheduled_posts)

    # Add a second scheduled post:
    # - Same image, same channel (Instagram)
    # - Scheduled in 5 seconds
    # - Recurring every day
    # - Configured as Instagram Stories
    recurring_schedule_time = (datetime.now(timezone.utc) + timedelta(seconds=5)).isoformat()
    recurring_payload = PublicAPIScheduledPostCreateHTTPPayload(
        text="Recurring IG Stories post in 5 seconds!",
        image_object_ids=[media.storage_object_id],
        channel_ids=[instagram_channel_id],
        schedule_at=recurring_schedule_time,
        is_draft=False,
        is_recur=True,
        recur_interval=AutomationRecurInterval.DAILY,
        instagram_settings=InstagramSettings(postType=InstagramPostType.STORIES)
    )

    scheduled_posts_recurring = client.create_scheduled_posts(recurring_payload)
    print("Scheduled recurring IG Stories post:", scheduled_posts_recurring)

    # --------------------------------------
    # Example 2: Post a Video to YouTube Immediately
    # --------------------------------------
    # Upload a video file (e.g., MP4)
    video_path = "videos/sample1.mp4"
    print(f"Uploading video: {video_path}")
    video_media = client.upload_media(video_path)
    print("Uploaded video media:", video_media)

    # Schedule a YouTube post immediately with the new YouTube settings
    now_time = datetime.now(timezone.utc).isoformat()
    youtube_payload = PublicAPIScheduledPostCreateHTTPPayload(
        text="Check out my new YouTube video!",
        video_object_id=video_media.storage_object_id,
        channel_ids=[youtube_channel_id],
        schedule_at=now_time,
        is_draft=False,
        youtube_settings=YoutubeSettings(
            videoTitle="My New Video",
            videoType=YoutubeVideoType.VIDEO,  # Use YoutubeVideoType.SHORT for shorts
            videoDescription="A fun and engaging video posted immediately.",
            videoPrivacyStatus=YoutubePrivacyStatus.PUBLIC
        )
    )

    scheduled_youtube_post = client.create_scheduled_posts(youtube_payload)
    print("Scheduled YouTube post:", scheduled_youtube_post)


if __name__ == "__main__":
    main()
