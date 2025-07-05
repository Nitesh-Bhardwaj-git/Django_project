from django import forms
from .models import Post, Comment, Profile

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image', 'post_caption']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'What\'s on your mind?'}),
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
            'post_caption': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add a caption...'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        widgets = {
            'comment_text': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Write a comment...'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_image', 'contact_info']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about yourself...'}),
            'contact_info': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Your contact information...'}),
        } 