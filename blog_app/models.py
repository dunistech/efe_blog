from django.db import models
from django.contrib.auth.models import User, AbstractUser



# Create your models here.


# class User(AbstractUser):
#     bio = models.TextField(blank=True, null=True)
#     profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
#     location = models.CharField(max_length=100, blank=True, null=True)

#     def __str__(self):
#         return self.username    
    
# class User(AbstractUser):
#     # Remove default username validators
#     username = models.CharField(
#         max_length=150, 
#         unique=True, 
#         blank=False, 
#         null=False
#     )
    
#     bio = models.TextField(blank=True, null=True)
#     profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
#     location = models.CharField(max_length=100, blank=True, null=True)

#     def __str__(self):
#         return self.username


class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
            while User.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{self.pk}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    
    


# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Post Model (modified to include image and video)
# class Post(models.Model):
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     media_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')], blank=True, null=True)
#     media_file = models.FileField(upload_to='media/', blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['title', 'author'], name='unique_post')
#         ] #using Django's unique_together or UniqueConstraint. This ensures that there can never be two posts with the same title and author,

#     def __str__(self):
#         return self.title


from django.utils.text import slugify

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)
    media_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')], blank=True, null=True)
    media_file = models.FileField(upload_to='media/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'], name='unique_post')
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            # Create a slug from the title and ensure uniqueness
            self.slug = slugify(self.title)
            while Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{self.pk}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# Comment Model
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"
    
    
    
    
    
    
    
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('like', 'Like'),
        ('comment', 'Comment'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    text = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender.username} {self.notification_type} on {self.post.title}"
    
    
    
    
    
# Add to models.py
class ChatRoom(models.Model):
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chat between {', '.join(user.username for user in self.participants.all())}"

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message from {self.sender.username} at {self.created_at}"

# _____________________________________________________

# ***SQL Command To Delete All Row Data in a Table***
        # TRUNCATE TABLE table_name;
# ____________________________________________________
