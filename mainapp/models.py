from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator

class UploadedMovie(models.Model):
    description = models.CharField(max_length=200)
    video = models.FileField(upload_to='videos_uploaded', validators=[FileExtensionValidator(allowed_extensions=['mov', 'avi', 'mp4', 'webm', 'mkv'])])
    date_uploaded = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.description

class MergedMovie(models.Model):
    uploadedmovie=models.ForeignKey(UploadedMovie, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    video = models.FileField(upload_to='Merged_uploaded')
    date_uploaded = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        self.description=self.uploadedmovie.description
        super(MergedMovie,self).save(*args, **kwargs)
