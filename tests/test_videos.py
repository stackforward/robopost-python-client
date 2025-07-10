#!/usr/bin/env python3
"""
Comprehensive test file for Robopost Video Series and Video Task functionality.
This script tests all video-related features including series creation,
video generation, task monitoring, and error handling.
"""

import os
import time
from datetime import datetime, timedelta, timezone

# Import your client and model definitions:
from robopost_client import (
    RobopostClient,
    PublicAPIScheduledPostCreateHTTPPayload,
    PublicAPIGeneratedFacelessVideoSeriesCreate,
    PublicAPIGeneratedFacelessVideoSeriesUpdate,
    GeneratedFacelessVideoSeriesContentType,
    GeneratedFacelessVideoStyle,
    GeneratedVideoFormat,
    AIVoice,
    VideoColor,
    VideoCaptionPosition,
    AutomationRecurInterval,
    AutomationPostTo,
    GeneratedFacelessVideoProcessState,
    InstagramSettings,
    InstagramPostType,
    YoutubeSettings,
    YoutubeVideoType,
    YoutubePrivacyStatus,
    RobopostAPIError,
    RobopostPlanLimitError
)


class VideoSeriesTestSuite:
    """Test suite for video series functionality"""

    def __init__(self, api_key: str, base_url: str = "http://localhost:8093/v1"):
        self.client = RobopostClient(apikey=api_key, base_url=base_url)
        self.created_series_ids = []
        self.created_task_ids = []

        # Test channel IDs - replace with your actual channel IDs
        self.instagram_channel_id = "89a1f4f8-2b27-4668-88c4-36c23e309ded"
        self.youtube_channel_id = "b9bf6705-3f70-4e64-98b3-6cbe0cb6f658"

    def log(self, message: str, level: str = "INFO"):
        """Simple logging function"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")

    def test_basic_series_creation(self):
        """Test 1: Basic video series creation"""
        self.log("=" * 60)
        self.log("TEST 1: Basic Video Series Creation")
        self.log("=" * 60)

        try:
            series_config = PublicAPIGeneratedFacelessVideoSeriesCreate(
                name="Test Tech Explained Series",
                content_type=GeneratedFacelessVideoSeriesContentType.ELI5,
                style=GeneratedFacelessVideoStyle.DEFAULT,
                voice=AIVoice.ALICE.value,
                lang="en",
                max_duration=30,  # Short test videos
                format=GeneratedVideoFormat.PORTRAIT,
                text_prefix="Welcome to our test! ",
                text_suffix=" Thanks for watching our test video!",

                # Caption styling
                font_size=120,
                font_color=VideoColor.YELLOW,
                stroke_width=3,
                stroke_color=VideoColor.BLACK,
                highlight_current_word=True,
                word_highlight_color=VideoColor.RED,
                position=VideoCaptionPosition.CENTER_CENTER,

                # Audio settings
                narration_volume=1.2,
                bgm_volume=0.3
            )

            series = self.client.create_video_series(series_config)
            self.created_series_ids.append(series.id)

            self.log(f"✅ Successfully created series: {series.name}")
            self.log(f"   ID: {series.id}")
            self.log(f"   Content Type: {series.content_type}")
            self.log(f"   Style: {series.style}")
            self.log(f"   Max Duration: {series.max_duration}s")

            return series

        except Exception as e:
            self.log(f"❌ Failed to create basic series: {e}", "ERROR")
            return None

    def test_custom_content_series(self):
        """Test 2: Custom content series creation"""
        self.log("\n" + "=" * 60)
        self.log("TEST 2: Custom Content Video Series")
        self.log("=" * 60)

        try:
            custom_series_config = PublicAPIGeneratedFacelessVideoSeriesCreate(
                name="Custom AI Education Series",
                content_type=GeneratedFacelessVideoSeriesContentType.CUSTOM,
                style=GeneratedFacelessVideoStyle.REALISM,
                voice=AIVoice.ALICE.value,
                max_duration=45,
                content_custom="Create educational content about machine learning basics, focusing on practical applications and real-world examples. Keep it simple and engaging.",

                # Different styling
                font_size=110,
                font_color=VideoColor.WHITE,
                stroke_width=2,
                stroke_color=VideoColor.BLACK,
                position=VideoCaptionPosition.CENTER_BOTTOM,

                # Audio settings
                narration_volume=1.1,
                bgm_volume=0.2
            )

            series = self.client.create_video_series(custom_series_config)
            self.created_series_ids.append(series.id)

            self.log(f"✅ Successfully created custom series: {series.name}")
            self.log(f"   Custom Content: {series.content_custom[:100]}...")

            return series

        except Exception as e:
            self.log(f"❌ Failed to create custom series: {e}", "ERROR")
            return None

    def test_recurring_series_creation(self):
        """Test 3: Recurring video series with scheduling"""
        self.log("\n" + "=" * 60)
        self.log("TEST 3: Recurring Video Series with Auto-Posting")
        self.log("=" * 60)

        try:
            # Schedule for tomorrow at 9 AM
            tomorrow_9am = (datetime.now(timezone.utc) + timedelta(days=1)).replace(
                hour=9, minute=0, second=0, microsecond=0
            )

            recurring_series_config = PublicAPIGeneratedFacelessVideoSeriesCreate(
                name="Daily Tech Facts",
                content_type=GeneratedFacelessVideoSeriesContentType.FUN_FACTS,
                style=GeneratedFacelessVideoStyle.POP_ART,
                max_duration=30,

                # Recurring settings
                is_recur=True,
                recur_dt=tomorrow_9am,
                recur_interval=AutomationRecurInterval.DAILY_SPECIFIC_TIME_SLOTS,
                recur_interval_time_slots=["09:00", "18:00"],  # 9 AM and 6 PM
                timezone="UTC",

                # Auto-posting settings
                create_scheduled_post=True,
                post_to=AutomationPostTo.DIRECT,
                channel_ids=[self.youtube_channel_id, self.instagram_channel_id]
            )

            series = self.client.create_video_series(recurring_series_config)
            self.created_series_ids.append(series.id)

            self.log(f"✅ Successfully created recurring series: {series.name}")
            self.log(f"   Recurring: {series.is_recur}")
            self.log(f"   Next Run: {series.recur_dt}")
            self.log(f"   Time Slots: {series.recur_interval_time_slots}")
            self.log(f"   Auto-posting to {len(series.channel_ids)} channels")

            return series

        except Exception as e:
            self.log(f"❌ Failed to create recurring series: {e}", "ERROR")
            return None

    def test_advanced_content_types(self):
        """Test 3b: Test various content types from the expanded enum"""
        self.log("\n" + "=" * 60)
        self.log("TEST 3b: Advanced Content Types")
        self.log("=" * 60)

        content_types_to_test = [
            GeneratedFacelessVideoSeriesContentType.SCARY_STORIES,
            GeneratedFacelessVideoSeriesContentType.MOTIVATIONAL,
            GeneratedFacelessVideoSeriesContentType.DID_YOU_KNOW,
            GeneratedFacelessVideoSeriesContentType.LIFE_PRO_TIPS,
            GeneratedFacelessVideoSeriesContentType.PHILOSOPHY
        ]

        styles_to_test = [
            GeneratedFacelessVideoStyle.ANIME,
            GeneratedFacelessVideoStyle.WATERCOLOR,
            GeneratedFacelessVideoStyle.ABSTRACT,
            GeneratedFacelessVideoStyle.FANTASY_CONCEPT_ART,
            GeneratedFacelessVideoStyle.MINIMALISM
        ]

        for i, (content_type, style) in enumerate(zip(content_types_to_test[:2], styles_to_test[:2])):
            try:
                series_config = PublicAPIGeneratedFacelessVideoSeriesCreate(
                    name=f"Test Series {content_type.value}",
                    content_type=content_type,
                    style=style,
                    voice=AIVoice.SARAH.value,  # Different voice
                    max_duration=25,
                    format=GeneratedVideoFormat.SQUARE,  # Different format

                    # Test different caption positions
                    position=VideoCaptionPosition.CENTER_TOP if i % 2 == 0 else VideoCaptionPosition.RIGHT_BOTTOM,
                    font_color=VideoColor.CYAN if i % 2 == 0 else VideoColor.MAGENTA,
                    word_highlight_color=VideoColor.ORANGE
                )

                series = self.client.create_video_series(series_config)
                self.created_series_ids.append(series.id)

                self.log(f"✅ Created {content_type.value} series with {style.value} style")

            except Exception as e:
                self.log(f"❌ Failed to create {content_type.value} series: {e}", "ERROR")

    def test_video_generation(self, series_id: str):
        """Test 4: Video generation from series"""
        self.log("\n" + "=" * 60)
        self.log("TEST 4: Video Generation from Series")
        self.log("=" * 60)

        try:
            self.log(f"🚀 Starting video generation for series: {series_id}")

            # Generate video
            task = self.client.generate_video(series_id)
            self.created_task_ids.append(task.task_id)

            self.log(f"✅ Video generation started")
            self.log(f"   Task ID: {task.task_id}")
            self.log(f"   Series ID: {task.video_series_id}")
            self.log(f"   Initial Status: {task.status}")

            return task

        except RobopostPlanLimitError as e:
            self.log(f"💸 Plan limit reached: {e.message}", "WARNING")
            self.log(f"   Limit: {e.limit}, Current: {e.current_usage}")
            return None
        except Exception as e:
            self.log(f"❌ Failed to generate video: {e}", "ERROR")
            return None

    def test_task_monitoring(self, task_id: str, timeout: int = 60):
        """Test 5: Task monitoring and status checking"""
        self.log("\n" + "=" * 60)
        self.log("TEST 5: Video Task Monitoring")
        self.log("=" * 60)

        try:
            self.log(f"⏳ Monitoring task: {task_id}")
            start_time = time.time()

            while time.time() - start_time < timeout:
                # Check task status
                task_status = self.client.get_video_task(task_id)
                self.log(f"   Status: {task_status.status}")

                # Get detailed info
                details = self.client.get_video_task_details(task_id)
                if 'error' in details and details['error']:
                    self.log(f"   Error: {details['error']}", "WARNING")

                if task_status.status in ["COMPLETE", "ERROR", "NO_CREDITS"]:
                    self.log(f"🏁 Task finished with status: {task_status.status}")

                    if task_status.status == "COMPLETE":
                        # Check for generated video info
                        if 'generated_video' in details:
                            video_info = details['generated_video']
                            self.log(f"📹 Generated video details:")
                            self.log(f"   Title: {video_info.get('title', 'Untitled')}")
                            self.log(f"   UUID: {video_info.get('uploadcare_uuid', 'N/A')}")
                            self.log(f"   Duration: {video_info.get('duration_ms', 'N/A')}ms")

                    return task_status

                # Wait before next check
                time.sleep(5)

            self.log(f"⏰ Task monitoring timed out after {timeout}s", "WARNING")
            return self.client.get_video_task(task_id)

        except Exception as e:
            self.log(f"❌ Error monitoring task: {e}", "ERROR")
            return None

    def test_batch_video_generation(self):
        """Test 6: Batch video generation from multiple series"""
        self.log("\n" + "=" * 60)
        self.log("TEST 6: Batch Video Generation")
        self.log("=" * 60)

        if len(self.created_series_ids) < 2:
            self.log("⚠️ Skipping batch test - need at least 2 series", "WARNING")
            return

        try:
            tasks = []

            # Generate videos from first 2 series
            for series_id in self.created_series_ids[:2]:
                try:
                    task = self.client.generate_video(series_id)
                    tasks.append(task)
                    self.created_task_ids.append(task.task_id)
                    self.log(f"📋 Started task {task.task_id} for series {series_id}")
                except RobopostPlanLimitError:
                    self.log(f"💸 Plan limit reached, skipping series {series_id}", "WARNING")
                    break

            if not tasks:
                self.log("❌ No tasks started due to plan limits", "WARNING")
                return

            # Monitor all tasks
            self.log(f"⏳ Monitoring {len(tasks)} batch tasks...")
            completed = 0
            max_wait = 120  # 2 minutes max
            start_time = time.time()

            while completed < len(tasks) and time.time() - start_time < max_wait:
                for task in tasks:
                    if hasattr(task, '_completed'):
                        continue

                    status = self.client.get_video_task(task.task_id)
                    if status.status in ["COMPLETE", "ERROR", "NO_CREDITS"]:
                        self.log(f"🏁 Task {task.task_id}: {status.status}")
                        task._completed = True
                        completed += 1

                if completed < len(tasks):
                    time.sleep(10)

            self.log(f"✅ Batch generation completed: {completed}/{len(tasks)} tasks finished")

        except Exception as e:
            self.log(f"❌ Batch generation error: {e}", "ERROR")

    def test_series_management(self):
        """Test 7: Series listing, updating, and management"""
        self.log("\n" + "=" * 60)
        self.log("TEST 7: Video Series Management")
        self.log("=" * 60)

        try:
            # List all series
            all_series = self.client.list_video_series(limit=20)
            self.log(f"📊 Found {len(all_series)} total video series")

            # Show first few
            for i, series in enumerate(all_series[:3]):
                self.log(f"   {i + 1}. {series.name} ({series.content_type.value}) - {series.id}")

            # Search functionality
            search_results = self.client.list_video_series(search_text="test", limit=10)
            self.log(f"🔍 Found {len(search_results)} series matching 'test'")

            # Update a series if we have one
            if self.created_series_ids:
                series_id = self.created_series_ids[0]
                self.log(f"✏️ Updating series: {series_id}")

                updates = PublicAPIGeneratedFacelessVideoSeriesUpdate(
                    max_duration=60,  # Increase duration
                    font_size=130,  # Larger font
                    bgm_volume=0.1,  # Quieter background music
                    style=GeneratedFacelessVideoStyle.COMIC,  # Change style
                    font_color=VideoColor.GREEN  # Change color
                )

                updated_series = self.client.update_video_series(series_id, updates)
                self.log(f"✅ Updated series successfully")
                self.log(f"   New max duration: {updated_series.max_duration}s")
                self.log(f"   New font size: {updated_series.font_size}")
                self.log(f"   New style: {updated_series.style}")

        except Exception as e:
            self.log(f"❌ Series management error: {e}", "ERROR")

    def test_task_listing_and_filtering(self):
        """Test 8: Task listing and filtering"""
        self.log("\n" + "=" * 60)
        self.log("TEST 8: Task Listing and Filtering")
        self.log("=" * 60)

        try:
            # List all tasks
            all_tasks = self.client.list_video_tasks(limit=50)
            self.log(f"📋 Found {len(all_tasks)} total video tasks")

            # Group by status
            status_counts = {}
            for task in all_tasks:
                status = task.status
                status_counts[status] = status_counts.get(status, 0) + 1

            self.log("📈 Task status breakdown:")
            for status, count in status_counts.items():
                emoji = {
                    "COMPLETE": "✅",
                    "ERROR": "❌",
                    "IN_PROGRESS": "⏳",
                    "NO_CREDITS": "💸"
                }.get(status, "📋")
                self.log(f"   {emoji} {status}: {count}")

            # Filter by status
            completed_tasks = self.client.list_video_tasks(
                status=GeneratedFacelessVideoProcessState.COMPLETE,
                limit=5
            )
            self.log(f"✅ Found {len(completed_tasks)} completed tasks")

            # Filter by series
            if self.created_series_ids:
                series_tasks = self.client.list_video_tasks(
                    series_id=self.created_series_ids[0],
                    limit=10
                )
                self.log(f"🎬 Found {len(series_tasks)} tasks for series {self.created_series_ids[0]}")

        except Exception as e:
            self.log(f"❌ Task listing error: {e}", "ERROR")

    def test_error_handling(self):
        """Test 9: Error handling scenarios"""
        self.log("\n" + "=" * 60)
        self.log("TEST 9: Error Handling")
        self.log("=" * 60)

        # Test invalid series ID
        try:
            self.client.generate_video("invalid-series-id")
            self.log("❌ Should have failed with invalid series ID", "ERROR")
        except RobopostAPIError as e:
            self.log(f"✅ Correctly caught API error: {e.message}")
        except Exception as e:
            self.log(f"⚠️ Unexpected error type: {e}", "WARNING")

        # Test invalid task ID
        try:
            self.client.get_video_task("invalid-task-id")
            self.log("❌ Should have failed with invalid task ID", "ERROR")
        except RobopostAPIError as e:
            self.log(f"✅ Correctly caught task error: {e.message}")
        except Exception as e:
            self.log(f"⚠️ Unexpected error type: {e}", "WARNING")

        # Test invalid series get
        try:
            self.client.get_video_series("invalid-series-id")
            self.log("❌ Should have failed with invalid series get", "ERROR")
        except RobopostAPIError as e:
            self.log(f"✅ Correctly caught series error: {e.message}")
        except Exception as e:
            self.log(f"⚠️ Unexpected error type: {e}", "WARNING")

    def test_convenience_methods(self):
        """Test 10: Convenience methods"""
        self.log("\n" + "=" * 60)
        self.log("TEST 10: Convenience Methods")
        self.log("=" * 60)

        try:
            # Test create and generate in one call
            series_config = PublicAPIGeneratedFacelessVideoSeriesCreate(
                name="Convenience Test Series",
                content_type=GeneratedFacelessVideoSeriesContentType.ELI5,
                max_duration=15,  # Very short for quick testing
                voice=AIVoice.ALICE.value,
                style=GeneratedFacelessVideoStyle.MINIMALISM,
                format=GeneratedVideoFormat.SQUARE
            )

            self.log("🚀 Testing create_video_series_and_generate...")

            try:
                series, task = self.client.create_video_series_and_generate(
                    series_config=series_config,
                    wait_for_completion=True,
                    timeout=60  # 1 minute timeout for convenience test
                )

                self.created_series_ids.append(series.id)
                self.created_task_ids.append(task.task_id)

                self.log(f"✅ Convenience method completed")
                self.log(f"   Created series: {series.name}")
                self.log(f"   Task final status: {task.status}")

            except TimeoutError:
                self.log("⏰ Convenience method timed out (expected for longer videos)", "WARNING")
            except RobopostPlanLimitError:
                self.log("💸 Plan limit reached during convenience test", "WARNING")

        except Exception as e:
            self.log(f"❌ Convenience method error: {e}", "ERROR")

    def test_all_voices_and_formats(self):
        """Test 11: Test different voices and video formats"""
        self.log("\n" + "=" * 60)
        self.log("TEST 11: Testing Different Voices and Formats")
        self.log("=" * 60)

        # Test different voices
        voices_to_test = [AIVoice.SARAH, AIVoice.BRIAN, AIVoice.CHARLIE]
        formats_to_test = [GeneratedVideoFormat.PORTRAIT, GeneratedVideoFormat.WIDESCREEN, GeneratedVideoFormat.SQUARE]

        for voice, video_format in zip(voices_to_test, formats_to_test):
            try:
                series_config = PublicAPIGeneratedFacelessVideoSeriesCreate(
                    name=f"Voice Test {voice.value} - {video_format.value}",
                    content_type=GeneratedFacelessVideoSeriesContentType.DID_YOU_KNOW,
                    style=GeneratedFacelessVideoStyle.DEFAULT,
                    voice=voice.value,
                    format=video_format,
                    max_duration=20,

                    # Test different caption positions for different formats
                    position=VideoCaptionPosition.CENTER_BOTTOM if video_format == GeneratedVideoFormat.WIDESCREEN
                    else VideoCaptionPosition.CENTER_CENTER,

                    font_color=VideoColor.WHITE,
                    word_highlight_color=VideoColor.YELLOW
                )

                series = self.client.create_video_series(series_config)
                self.created_series_ids.append(series.id)

                self.log(f"✅ Created series with {voice.value} voice and {video_format.value} format")

            except Exception as e:
                self.log(f"❌ Failed to create series with {voice.value}: {e}", "ERROR")

    def run_all_tests(self):
        """Run the complete test suite"""
        self.log("🚀 STARTING ROBOPOST VIDEO SERIES TEST SUITE")
        self.log("=" * 80)

        start_time = time.time()

        try:
            # Core functionality tests
            series1 = self.test_basic_series_creation()
            series2 = self.test_custom_content_series()
            series3 = self.test_recurring_series_creation()

            # Test expanded functionality
            self.test_advanced_content_types()
            self.test_all_voices_and_formats()

            # Video generation tests
            if series1:
                task1 = self.test_video_generation(series1.id)
                if task1:
                    self.test_task_monitoring(task1.task_id, timeout=1200)

            # Batch and management tests
            self.test_batch_video_generation()
            self.test_series_management()
            self.test_task_listing_and_filtering()

            # Advanced tests
            self.test_error_handling()
            self.test_convenience_methods()

        except KeyboardInterrupt:
            self.log("⚠️ Test suite interrupted by user", "WARNING")
        except Exception as e:
            self.log(f"💥 Unexpected error in test suite: {e}", "ERROR")

        end_time = time.time()
        duration = end_time - start_time

        self.log("\n" + "=" * 80)
        self.log(f"🏁 TEST SUITE COMPLETED in {duration:.1f} seconds")
        self.log(f"📊 Created {len(self.created_series_ids)} series, {len(self.created_task_ids)} tasks")
        self.log("=" * 80)


def main():
    """Main test function"""
    # Configuration
    api_key = "168358e9-344f-48a5-9e03-84f081915a73"  # Replace with your actual API key
    api_url = "http://localhost:8093/v1"  # Update for your environment

    print("🤖 ROBOPOST VIDEO SERIES COMPREHENSIVE TEST")
    print("=" * 50)
    print(f"API URL: {api_url}")
    print(f"API Key: {api_key[:8]}...")
    print("=" * 50)

    # Create test directories if they don't exist
    os.makedirs("videos", exist_ok=True)
    os.makedirs("images", exist_ok=True)

    # Initialize and run test suite
    test_suite = VideoSeriesTestSuite(api_key=api_key, base_url=api_url)

    try:
        test_suite.run_all_tests()
    except Exception as e:
        print(f"💥 Fatal error: {e}")

    print("\n🎉 Test execution completed!")


if __name__ == "__main__":
    main()