import os
from datetime import datetime, timedelta, timezone

# Import your client and model definitions:
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
    api_key = "9d2b38a5-9f90-47ea-8dd6-4117ca4f84e2"  # Replace with your actual API key
    # Define channel IDs for Instagram and YouTube
    instagram_channel_id = "89a1f4f8-2b27-4668-88c4-36c23e309ded"
    youtube_channel_id = "b9bf6705-3f70-4e64-98b3-6cbe0cb6f658"

    # Point to the local dev server or your staging/prod environment
    api_url = "http://localhost:8093/v1"
    client = RobopostClient(apikey=api_key, base_url=api_url)

    # -------------------------------------------------------------
    # Example 1: Post using an image (LOCAL UPLOAD)
    # -------------------------------------------------------------
    image_path = "images/sample1.jpg"
    print(f"Uploading image: {image_path}")
    media = client.upload_media(image_path)  # local file upload
    print("Uploaded media:", media)

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

    # -------------------------------------------------------------
    # Example 2: Recurring Post on Instagram (LOCAL UPLOAD)
    # -------------------------------------------------------------
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

    # -------------------------------------------------------------
    # Example 3: Post a Video to YouTube Immediately (LOCAL UPLOAD)
    # -------------------------------------------------------------
    video_path = "videos/sample1.mp4"
    print(f"Uploading video: {video_path}")
    video_media = client.upload_media(video_path)
    print("Uploaded video media:", video_media)

    now_time = datetime.now(timezone.utc).isoformat()
    youtube_payload = PublicAPIScheduledPostCreateHTTPPayload(
        text="Check out my new YouTube video!",
        video_object_id=video_media.storage_object_id,
        channel_ids=[youtube_channel_id],
        schedule_at=now_time,
        is_draft=False,
        youtube_settings=YoutubeSettings(
            videoTitle="My New Video",
            videoType=YoutubeVideoType.VIDEO,  # or YoutubeVideoType.SHORT
            videoDescription="A fun and engaging video posted immediately.",
            videoPrivacyStatus=YoutubePrivacyStatus.PUBLIC
        )
    )

    scheduled_youtube_post = client.create_scheduled_posts(youtube_payload)
    print("Scheduled YouTube post:", scheduled_youtube_post)

    # -------------------------------------------------------------
    # Example 4: Use image_urls (REMOTE IMAGE)
    # -------------------------------------------------------------
    # We specify a remote image URL (e.g., from Wikipedia)
    # The server will download it, upload to UploadCare, and then
    # fill in the final image_object_ids for us.
    # -------------------------------------------------------------
    remote_image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Grosser_Panda.JPG/640px-Grosser_Panda.JPG"
    schedule_time_remote_img = (datetime.now(timezone.utc) + timedelta(seconds=5)).isoformat()
    payload_remote_img = PublicAPIScheduledPostCreateHTTPPayload(
        text="Testing remote image URL!",
        image_urls=[remote_image_url],  # <--- new field
        channel_ids=[instagram_channel_id],
        schedule_at=schedule_time_remote_img,
        is_draft=False
    )

    scheduled_post_remote_img = client.create_scheduled_posts(payload_remote_img)
    print("Scheduled post (remote image):", scheduled_post_remote_img)

    # -------------------------------------------------------------
    # Example 5: Use video_url (REMOTE VIDEO)
    # -------------------------------------------------------------
    # We specify a remote video URL. The server will download and
    # upload it to UploadCare, converting if necessary.
    # -------------------------------------------------------------
    remote_video_url = "https://api.robopost.app/stored_objects/960a488d-3c40-4df5-9337-5bbcacafb1e8/download"
    schedule_time_remote_vid = (datetime.now(timezone.utc) + timedelta(seconds=5)).isoformat()
    payload_remote_vid = PublicAPIScheduledPostCreateHTTPPayload(
        text="Testing remote video URL!",
        video_url=remote_video_url,       # <--- new field
        channel_ids=[youtube_channel_id],
        schedule_at=schedule_time_remote_vid,
        is_draft=False,
        youtube_settings=YoutubeSettings(
            videoTitle="Remote Video Post",
            videoType=YoutubeVideoType.VIDEO,
            videoDescription="Uploaded via remote video URL test.",
            videoPrivacyStatus=YoutubePrivacyStatus.PUBLIC
        )
    )

    scheduled_post_remote_vid = client.create_scheduled_posts(payload_remote_vid)
    print("Scheduled post (remote video):", scheduled_post_remote_vid)

if __name__ == "__main__":
    main()
