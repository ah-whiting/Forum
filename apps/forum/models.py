from django.db import models
from django.utils import timezone

class TopicManager(models.Manager):
    def validator(self, data):
        e = {}
        if len(data["title"]) < 5 or len(data["title"]) > 45:
            e["title"] = "Title must be between 5 and 45 characters"
        if len(data["message"]) < 10:
            e["message"] = "Message must be at least 10 characters"
        return e
            
class CommentManager(models.Manager):
    def validator(self, data):
        e = {}
        if len(data["message"]) < 2:
            e["message"] = "Comment must be at least 2 characters"
        return e

class Topic(models.Model):
    title = models.TextField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    views = models.IntegerField(default = 0)
    created_by = models.ForeignKey("login.User", related_name = 'topics')
    objects = TopicManager()
    def elapsed_time(self):
        return timezone.now() - self.created_at
    def last_page(self, page_count = 10):
        comment_count = self.comments.count()
        return comment_count // page_count + (comment_count % page_count > 0)


class Comment(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    topic = models.ForeignKey(Topic, related_name = 'comments')
    created_by = models.ForeignKey("login.User", related_name = 'comments')
    is_active = models.BooleanField(default=True)
    is_edited = models.BooleanField(default=False)
    objects = CommentManager()
    def elapsed_time(self, update=False):
        time = self.created_at
        context = {
            "str":"some string",
            "delta": timezone.now() - time
        }
        delta = context["delta"].total_seconds()
        if delta < 60:
            context["str"] = f"{int(delta)} seconds ago"
        elif delta < 3600:
            context["str"] = f"{int(delta // 60)} minutes ago"
        elif delta < 3600*24:
            context["str"] = f"{int(delta // 3600)} hours ago"
        else:
            context["str"] = f"{int(context['delta'].days)} days ago"
        return context
    def elapsed_update(self):
        time = self.updated_at
        context = {
            "str":"some string",
            "delta": timezone.now() - time
        }
        delta = context["delta"].total_seconds()
        if delta < 60:
            context["str"] = f"{int(delta)} seconds ago"
        elif delta < 3600:
            context["str"] = f"{int(delta // 60)} minutes ago"
        elif delta < 3600*24:
            context["str"] = f"{int(delta // 3600)} hours ago"
        else:
            context["str"] = f"{int(context['delta'].days)} days ago"
        return context
