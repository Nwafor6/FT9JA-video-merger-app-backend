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
import subprocess

def merge_videos(video1_path, video2_path, text, description, uploaded_movie, video_name):


    # Concatenate the video and text using ffmpeg
    # output_path1 = f"media/ft9ja/{video_name}"
    # cmd = [
    #     "ffmpeg",
    #     "-i", video1_path,
    #     "-vf", f"drawtext=text='{description}':x=(w-text_w)/2:y=(h-text_h)/2:fontcolor=white:fontsize=80",
    #     "-c:a", "copy",
    #     output_path1
    # ]
    # subprocess.run(cmd, check=True)
    # output_path = f"media/Merged_uploaded/{video_name}"
    # cmd = [
    # #     "ffmpeg",
    # #     "-i", output_path1,
    # #     "-i", video2_path,
    # #     # "-filter_complex", f"[0:v]setpts=PTS-STARTPTS, scale=640x480 [v0]; [1:v]setpts=PTS-STARTPTS, scale=640x480 [v1]; [v0][v1]concat=n=2:v=1:a=1[outv]",
    # #     "-filter_complex", f"[0:v]setpts=PTS-STARTPTS, scale=640x480 [v0]; [1:v]setpts=PTS-STARTPTS, scale=640x480 [v1]; [v0][v1]concat=n=2:v=1:a=0[outv]",
    # #     "-map", "[outv]",
    # #     "-c:v", "libx264",
    # #     "-crf", "23",
    # #     "-preset", "medium",
    # #     "-shortest",
    # #     "-y",
    # #     output_path
    # # ]
    # # subprocess.run(cmd, check=True)
    # import ffmpeg
    # ffmpeg.input(output_path1).concat(video1_path).output(output_path).run()
    # Output path for the merged video
  

#    # Concatenate the video and text using ffmpeg
#     output_path = f"media/Merged_uploaded/{video_name}"

#     # Generate the ffmpeg command
#     # cmd = f"ffmpeg -i {video1_path} -i {video2_path} -filter_complex \"[0:v]drawtext=text='{description}':x=(w-text_w)/4:y=(h-text_h)/4:fontcolor=white:fontsize=80[v];[v][1:v]concat=n=2:v=1:a=0\" -c:v libx264 -preset fast -crf 18 -movflags +faststart {output_path}"
#     cmd = f"ffmpeg -i {video1_path} -i {video2_path} -filter_complex \"[0:v]drawtext=text='{description}':x=(w-text_w)/2:y=(h-text_h)/2:fontcolor=white:fontsize=80[v];[v][1:v]concat=n=2:v=1:a=1\" -c:v libx264 -preset fast -crf 18 -movflags +faststart {output_path}"
#     # Execute the command using subprocess
#     subprocess.run(cmd, shell=True, check=True)
    from moviepy.video.io.ffmpeg_tools import ffmpeg_merge_video_audio
    output_path = f"media/Merged_uploaded/{video_name}"
    ffmpeg_merge_video_audio(video1_path, video2_path, output_path, ffmpeg_output=True)



    # Update the MergedMovie object
    merged_video = MergedMovie.objects.create(
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
        
        video1_path = f"media/videos_uploaded/{str(video)}"
        video2_path = "media/ft9ja/ft9ja.mp4"
        # video2_path = "/home/ft9javideomergeapp/FT9JA-video-merger-app-backend/media/ft9ja/ft9ja.mp4"
        text = description
        # Create a thread for merging the videos
        # cmd += [ ffmpeg -i video2_path -vf “drawtext=text=’Hello World’:fontfile=/path/to/font.ttf:fontsize=50:fontcolor=white:x=100:y=100” -codec:a copy output_video.mp4]
        merge_thread = threading.Thread(target=merge_videos, args=(video1_path, video2_path, text, description, uploaded_movie, video_name))
        merge_thread.start()
        merge_thread.join()
        print(video_name)
        merged_video=MergedMovie.objects.get(video=f'Merged_uploaded/{video_name}')
        return JsonResponse({"details":'Merging complete !. Now click download',"file_name":str(video), "file_loc":f"media/Merged_uploaded/{str(video_name)}", "short_url":generate_short_url(f"http://127.0.0.1:8000/media/Merged_uploaded/{str(video_name)}")})
        # return JsonResponse({"details":'Merging complete !. Now click download',"file_name":str(video), "file_loc":f"/home/ft9javideomergeapp/FT9JA-video-merger-app-backend/media/Merged_uploaded/{str(video_name)}", "short_url":generate_short_url(f"http://ft9javideomergeapp.pythonanywhere.com/media/Merged_uploaded/{str(video_name)}")})
    return render(request, "index.html")


def decode_short_link(request, link):
    full_link = get_object_or_404(ShortLink, short_url=link)
    return HttpResponse(status=302, headers={'Location': full_link.original_url})








# def merge_videos(video1_path, video2_path, text, description, uploaded_movie, video_name):


#     # Concatenate the video and text using ffmpeg
#     output_path = f"media/Merged_uploaded/{video_name}"
#     cmd = [
#         "ffmpeg",
#         "-i", video1_path,
#         "-i", video2_path,
#         "-vf", f"drawtext=text='{description}':x=(w-text_w)/2:y=(h-text_h)/2:fontcolor=white:fontsize=80",
#         "-c:a", "copy",
#         output_path
#     ]
#     subprocess.run(cmd, check=True)



#     # Update the MergedMovie object
#     merged_video = MergedMovie.objects.create(
#         uploadedmovie=uploaded_movie,
#         description=description,
#         video=f"Merged_uploaded/{video_name}",
#     )









