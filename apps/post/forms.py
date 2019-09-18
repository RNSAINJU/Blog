from django import forms
from .models import Comment
class CommentForm(forms.Form):
    message=forms.CharField(
        widget=forms.Textarea(
            attrs={"class":"form-control",
                   "placeholder":"Your message"
                   }
        )
    )
