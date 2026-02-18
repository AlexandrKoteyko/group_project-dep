from django import forms
from .models import Vote, VoteOption

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ('title', 'description', 'vote_type', 'is_active', 'end_date')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'vote_type': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'end_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }

class VoteOptionForm(forms.ModelForm):
    class Meta:
        model = VoteOption
        fields = ('text', 'image')
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class UserVoteForm(forms.Form):
    option = forms.ModelChoiceField(
        queryset=VoteOption.objects.none(),
        widget=forms.RadioSelect,
        label="Ваш вибір"
    )
    
    def __init__(self, *args, **kwargs):
        vote = kwargs.pop('vote', None)
        super().__init__(*args, **kwargs)
        if vote:
            self.fields['option'].queryset = vote.options.all()