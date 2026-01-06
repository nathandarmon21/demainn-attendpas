"""
Video processing utilities for extracting clips and adding captions
"""
import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
import subprocess


class VideoProcessor:
    def __init__(self):
        self.temp_dir = "outputs/short_videos"
        os.makedirs(self.temp_dir, exist_ok=True)

    def extract_clip(self, video_path, start_time, end_time, output_path):
        """
        Extract a clip from video between start_time and end_time (in seconds)
        """
        try:
            video = VideoFileClip(video_path)
            clip = video.subclip(start_time, end_time)

            # Ensure clip is in vertical format for shorts/reels (9:16 aspect ratio)
            # If the video is horizontal, we'll crop it to center
            w, h = clip.size
            target_aspect = 9/16
            current_aspect = w/h

            if current_aspect > target_aspect:
                # Video is too wide, crop width
                new_width = int(h * target_aspect)
                x_center = w / 2
                x1 = int(x_center - new_width / 2)
                clip = clip.crop(x1=x1, width=new_width)
            elif current_aspect < target_aspect:
                # Video is too tall, crop height
                new_height = int(w / target_aspect)
                y_center = h / 2
                y1 = int(y_center - new_height / 2)
                clip = clip.crop(y1=y1, height=new_height)

            clip.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                fps=30
            )
            video.close()
            clip.close()
            return True
        except Exception as e:
            print(f"Error extracting clip: {str(e)}")
            return False

    def add_captions(self, video_path, caption_text, output_path):
        """
        Add centered caption text to video (for short clips)
        """
        try:
            video = VideoFileClip(video_path)

            # Create text clip with styling for social media
            txt_clip = TextClip(
                caption_text,
                fontsize=40,
                color='white',
                stroke_color='black',
                stroke_width=2,
                font='Arial-Bold',
                method='caption',
                size=(video.w * 0.9, None),
                align='center'
            )

            # Position at bottom of video
            txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(video.duration)

            # Composite video with text
            final = CompositeVideoClip([video, txt_clip])

            final.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                fps=30
            )

            video.close()
            txt_clip.close()
            final.close()
            return True
        except Exception as e:
            print(f"Error adding captions: {str(e)}")
            return False

    def get_video_duration(self, video_path):
        """Get total duration of video in seconds"""
        try:
            video = VideoFileClip(video_path)
            duration = video.duration
            video.close()
            return duration
        except Exception as e:
            print(f"Error getting video duration: {str(e)}")
            return None

    def create_clip_with_captions(self, video_path, start_time, end_time, caption_text, output_path):
        """
        All-in-one: extract clip and add captions
        """
        temp_clip_path = output_path.replace('.mp4', '_temp.mp4')

        # Extract clip
        if not self.extract_clip(video_path, start_time, end_time, temp_clip_path):
            return False

        # Add captions if provided
        if caption_text:
            success = self.add_captions(temp_clip_path, caption_text, output_path)
            # Clean up temp file
            if os.path.exists(temp_clip_path):
                os.remove(temp_clip_path)
            return success
        else:
            # No captions, just rename temp file
            os.rename(temp_clip_path, output_path)
            return True
