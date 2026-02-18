from django import forms
from .models import Survey, Question, Choice

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ('title', 'description', 'is_active', 'is_multi_page')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_multi_page': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', 'page', 'order')
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'page': forms.NumberInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('text',)
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SurveyResponseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)
        
        for question in questions:
            choices = question.choices.all()
            if choices:
                self.fields[f'question_{question.id}'] = forms.ModelChoiceField(
                    queryset=choices,
                    widget=forms.RadioSelect,
                    label=question.text,
                    required=True
                )