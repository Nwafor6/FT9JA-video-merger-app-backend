import threading
import random
import string
from django.shortcuts import render
from django.http import JsonResponse
from .models import MergedMovie, UploadedMovie
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip

video_name=""
def merge_videos(video1_path, video2_path, text, description, uploaded_movie, video_name):
    video1 = VideoFileClip(video1_path).resize(width=1080)
    video2 = VideoFileClip(video2_path)
    
    text_clip = TextClip(text, fontsize=80, color="white", font="Arial", bg_color="#359602")
    text_clip = text_clip.set_duration(video1.duration)  # Set text duration to match video1

    
    # Calculate position based on screen size
    screen_width, screen_height = video1.size
    text_width, text_height = text_clip.size
    x_pos = int((screen_width - text_width) / 2)
    y_pos = int(screen_height * 0.9 - text_height)
    text_clip = text_clip.set_position((x_pos, y_pos))
    
    # Composite the video and text clip
    composite_clip = CompositeVideoClip([video1, text_clip])
    # output_path1 = f"media/ft9ja/{video_name}"
    output_path1 = f"/home/ft9javideomergeapp/FT9JA-video-merger-app-backend/media/ft9ja/{video_name}"
    composite_clip.write_videofile(output_path1, codec="libx264", audio_codec="aac", threads=8, fps=24)
    
    # Merge output1 and video2
    video3 = VideoFileClip(output_path1)
    merged_video = concatenate_videoclips([video3, video2])
    
    # output_path = f"media/Merged_uploaded/{video_name}"
    output_path = f"/home/ft9javideomergeapp/FT9JA-video-merger-app-backend/media/Merged_uploaded/{video_name}"
    merged_video.write_videofile(output_path, codec="libx264", audio_codec="aac", threads=8, fps=24)
    
    merged_video=MergedMovie.objects.create(
        uploadedmovie=uploaded_movie,
        description=description,
        video=f"Merged_uploaded/{video_name}",
    )

def video_merger(request):
    if request.method == "POST":
        description = request.POST["description"]
        video = request.FILES["video"]
        video_name=f"{''.join(random.choices(string.ascii_letters + string.digits, k=6))}{video}"
        uploaded_movie = UploadedMovie.objects.create(
            description=description,
            video=video
        )
        
        video1_path = uploaded_movie.video.path
        # video2_path = "media/ft9ja/ft9ja.mp4"
        video2_path = "/home/ft9javideomergeapp/FT9JA-video-merger-app-backend/media/ft9ja/ft9ja.mp4"
        text = description
        # Create a thread for merging the videos
        merge_thread = threading.Thread(target=merge_videos, args=(video1_path, video2_path, text, description, uploaded_movie, video_name))
        merge_thread.start()
        merge_thread.join()
        print(video_name)
        merged_video=MergedMovie.objects.get(video=f'Merged_uploaded/{video_name}')
        # return JsonResponse({"details":'Merging complete !. Now click download',"file_name":str(video), "file_loc":f"media/Merged_uploaded/{str(video_name)}"})
        return JsonResponse({"details":'Merging complete !. Now click download',"file_name":str(video), "file_loc":f"/home/ft9javideomergeapp/FT9JA-video-merger-app-backend/media/Merged_uploaded/{str(video_name)}"})
    return render(request, "index.html")
