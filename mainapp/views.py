import threading
import random
import string
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import MergedMovie, UploadedMovie, ShortLink
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
from .shortner import generate_short_url
from django.shortcuts import get_object_or_404
from django.http import HttpResponse


video_name=""
def merge_videos(video1_path, video2_path, text, description, uploaded_movie, video_name):
    video1 = VideoFileClip(video1_path).resize(0.3)
    video2 = VideoFileClip(video2_path).resize(video1.size)
    
    text_clip = TextClip(text, fontsize=20, color="white", font="Arial", bg_color="#359602")
    text_clip = text_clip.set_duration(video1.duration)  # Set text duration to match video1

    
    # Calculate position based on screen size
    screen_width, screen_height = video1.size
    text_width, text_height = text_clip.size
    x_pos = int((screen_width - text_width) / 2)
    y_pos = int(screen_height * 0.9 - text_height)
    text_clip = text_clip.set_position((x_pos, y_pos))
    
    # Composite the video and text clip
    composite_clip = CompositeVideoClip([video1, text_clip])
    # Apply optimizations
    # composite_clip = composite_clip.resize(width=1920)  # Resize to a specific width
    composite_clip = composite_clip.set_fps(30)  # Adjust the frames per second

    # output_path1 = f"media/ft9ja/{video_name}"
    output_path1 = f"/home/ft9javideomergeapp/FT9JA-video-merger-app-backend/media/ft9ja/{video_name}"
    composite_clip.write_videofile(output_path1, codec="libx264", audio_codec="aac", threads=32, fps=39)
    
    # Merge output1 and video2
    video3 = VideoFileClip(output_path1)
    merged_video = concatenate_videoclips([video3, video2], method='chain')
    
    # output_path = f"media/Merged_uploaded/{video_name}"
    output_path = f"/home/ft9javideomergeapp/FT9JA-video-merger-app-backend/media/Merged_uploaded/{video_name}"
    merged_video.write_videofile(output_path, codec="libx264", audio_codec="aac", threads=32, fps=39)
    
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
        # return JsonResponse({"details":'Merging complete !. Now click download',"file_name":str(video), "file_loc":f"media/Merged_uploaded/{str(video_name)}", "short_url":generate_short_url(f"http://127.0.0.1:8000/media/Merged_uploaded/{str(video_name)}")})
        return JsonResponse({"details":'Merging complete !. Now click download',"file_name":str(video), "file_loc":f"/home/ft9javideomergeapp/FT9JA-video-merger-app-backend/media/Merged_uploaded/{str(video_name)}", "short_url":generate_short_url(f"http://ft9javideomergeapp.pythonanywhere.com/media/Merged_uploaded/{str(video_name)}")})
    return render(request, "index.html")


def decode_short_link(request, link):
    full_link = get_object_or_404(ShortLink, short_url=link)
    return HttpResponse(status=302, headers={'Location': full_link.original_url})



