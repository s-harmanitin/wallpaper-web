from .models import tag,Post
from django import forms



class postform(forms.ModelForm):   
    class Meta:
        model = Post
        fields = ("__all__")
         
    def __init__(self,*args,**kwargs):
        super(postform,self).__init__(*args,**kwargs)
        self.fields['tag'].empty_label = "select Tag"
        