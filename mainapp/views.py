from django.shortcuts import render
from .models import MergedMovie,UploadedMovie

# Create your views here.

def video_merger(request):
    if request.method =="POST":
       description=request.POST["video-description"] 
       video=request.FILES["video-file"]
       uploaded_movie=UploadedMovie.objects.create(
           description=description,
           video=video
       )
       MergedMovie.objects.create(
           uploadedmovie=uploaded_movie,
           description=description,
           video=video,
       )
    return render(request, "index.html")
