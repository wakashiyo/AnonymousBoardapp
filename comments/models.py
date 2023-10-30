from django.db import models
from django.conf import settings
from django.utils import timezone


class Comment(models.Model):
    body = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')
    password = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        ordering = ['-updated_at'] # 降順ソート


class Like(models.Model):
    target = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)


# class Favorite(models.Model):
#     target = models.ForeignKey(Comment, on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(default=timezone.now)