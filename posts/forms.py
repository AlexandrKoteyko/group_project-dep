from django import forms
from .models import Post, Comment, Hashtag

class PostForm(forms.ModelForm):
    hashtags = forms.CharField(
        required=False,
        help_text='Введіть хештеги через кому, наприклад: #mirage, #awp, #highlight',
        widget=forms.TextInput(attrs={'placeholder': '#mirage, #awp, #highlight'})
    )
    
    class Meta:
        model = Post
        fields = ('content', 'media_type', 'media_file')
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'maxlength': 280,
                'class': 'form-control',
                'placeholder': 'Що нового у CS2?'
            }),
            'media_type': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'content': 'Текст поста',
            'media_type': 'Тип медіа',
            'media_file': 'Файл',
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > 280:
            raise forms.ValidationError('Пост не може бути довшим за 280 символів')
        return content

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
                'placeholder': 'Додайте коментар...',
                'maxlength': 500
            })
        }
        labels = {
            'content': 'Коментар'
        }

class HashtagForm(forms.ModelForm):
    class Meta:
        model = Hashtag
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '#назва'
            })
        }