# blog/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Post, Category, Comment

  
  

# Custom User Update Form for Profile Page
# class UserUpdateForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'bio', 'profile_image', 'location']
class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        help_text='',  # Empty help text
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'profile_image', 'location']
        

class PostCreationForm(forms.ModelForm):
    # Radio buttons to select between image or video post
    media_type = forms.ChoiceField(
        choices=[('image', 'Image'), ('video', 'Video')],
        required=True,
        widget=forms.RadioSelect
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image', 'video_url']

    image = forms.ImageField(required=False)  # Optional image field
    video_url = forms.URLField(required=False)  # Optional video URL field

    def clean(self):
        cleaned_data = super().clean()
        media_type = cleaned_data.get('media_type')
        
        # Make sure that the user uploads either an image or a video
        if media_type == 'image' and not cleaned_data.get('image'):
            self.add_error('image', 'You must upload an image.')
        elif media_type == 'video' and not cleaned_data.get('video_url'):
            self.add_error('video_url', 'You must provide a video URL.')
        
        return cleaned_data

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        widgets = {
            'comment_text': forms.Textarea(attrs={'placeholder': 'Write your comment...', 'rows': 4, 'cols': 40}),
        }

