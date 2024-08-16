# files/models.py
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import secrets
from django.core.validators import MinValueValidator, MaxValueValidator

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_count = models.IntegerField(default=0)  # New field for total count
    GENRE_CHOICES = [('action', 'Action'),('comedy', 'Comedy'),('drama', 'Drama'),('sci-fi', 'Science Fiction'),('horror', 'Horror'),('self-help', 'Self-Help'),]
    genre = models.CharField(max_length=10,choices=GENRE_CHOICES,default='action',blank=True)
    
    # Add a new field to store the unique token
    unique_token = models.CharField(max_length=32, unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate a unique token for the file
        if not self.unique_token:
            self.unique_token = secrets.token_urlsafe(16)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey('UploadedFile', related_name='ratings', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

