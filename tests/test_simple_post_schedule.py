import os
from datetime import datetime, timedelta, timezone
from robopost_client import (
    RobopostClient,
    PublicAPIScheduledPostCreateHTTPPayload,
    AutomationRecurInterval,
    InstagramSettings,
    InstagramPostType
)


def main():
    # Instantiate the client with your API key
    api_key = "3f60b32d-1d38-4ab3-bfc5-7e5f683870ab"  # Replace with your actual API key
    channel_ids = ["066617a4-1e4d-40ab-ac9d-0e4c6521814e"]
    api_url = "http://localhost:8093"
    client = RobopostClient(apikey=api_key, base_url=api_url)

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
        channel_ids=channel_ids,
        schedule_at=schedule_time,
        is_draft=False
    )

    scheduled_posts = client.create_scheduled_posts(payload)
    print("Scheduled posts:", scheduled_posts)

    # Add a second scheduled post:
    # - Same image, same channel
    # - Scheduled in 5 seconds
    # - Recurring every day
    # - Configured as Instagram Stories
    recurring_schedule_time = (datetime.now(timezone.utc) + timedelta(seconds=5)).isoformat()
    recurring_payload = PublicAPIScheduledPostCreateHTTPPayload(
        text="Recurring IG Stories post in 5 seconds!",
        image_object_ids=[media.storage_object_id],
        channel_ids=channel_ids,
        schedule_at=recurring_schedule_time,
        is_draft=False,
        is_recur=True,
        recur_interval=AutomationRecurInterval.DAILY,
        instagram_settings=InstagramSettings(postType=InstagramPostType.STORIES)
    )

    scheduled_posts_recurring = client.create_scheduled_posts(recurring_payload)
    print("Scheduled recurring IG Stories post:", scheduled_posts_recurring)


if __name__ == "__main__":
    main()
