from django.urls import path
from . import views

urlpatterns=[
    path("", views.video_merger),
    path("ft9ja/<str:link>/", views.decode_short_link, name="video_link")
]