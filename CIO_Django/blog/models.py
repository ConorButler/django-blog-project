from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Csstats(models.Model):
    player = models.CharField(max_length=20) 
    awp_kills_per_round = models.FloatField()
    ak_kills_per_round = models.FloatField() 
    headshot_percent = models.FloatField()
    hours = models.IntegerField() 

