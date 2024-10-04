from django.db import models
import uuid
from authentication.models import User

# Create your models here.

def media_directory_path(instance, filename):
    return 'chirp_media/{0}/{1}/{2}'.format(instance.chirp.chirper.username, instance.chirp.text[0:30], filename)

class Chirp(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    text = models.TextField(max_length=500, null=True)
    chirper = models.ForeignKey(User, on_delete=models.CASCADE)
    chirped = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text[0:30]

class ChirpMedia(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    media = models.FileField(upload_to=media_directory_path, blank=True, null=True)
    caption = models.CharField(max_length=100, blank=True, null=True, default='')
    chirp = models.ForeignKey(Chirp, on_delete=models.CASCADE, related_name='media', default=None)

    def __str__(self):
        return f"Media for Chirp: {self.chirp.text[0:30]}"

class ChirpComment(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    text = models.TextField(max_length=500)
    chirper = models.ForeignKey(User, on_delete=models.CASCADE)
    chirp = models.ForeignKey(Chirp, on_delete=models.CASCADE)
    sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.chirper.username} commented on this chirp: {self.chirp}"

class ChirpLike(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    chirper = models.ForeignKey(User, on_delete=models.CASCADE)
    chirp = models.ForeignKey(Chirp, on_delete=models.CASCADE)
    liked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.chirper.username} liked this chirp: {self.chirp}"

