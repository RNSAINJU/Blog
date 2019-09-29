from django import forms
from .models import Comment, Post
from tinymce import TinyMCE
#
# class TinyMCEWidget(TinyMCE):
#     def use_required_attribute(self,*args):
#         return False

class CommentForm(forms.ModelForm):
    message=forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class":"form-control",
                "placeholder":"Your message"
                   }
        )
    )

    class Meta:
        model= Comment
        fields=('message',)

class PostForm(forms.ModelForm):
    # description= forms.CharField(
    #     widget=TinyMCEWidget(
    #         attrs={'required':False,'cols':30,'rows':10}
    #     )
    # )

    class Meta:
        model= Post
        fields=('title', 'description','categories','image','status','featured')
