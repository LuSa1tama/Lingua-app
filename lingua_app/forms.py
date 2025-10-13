from django import forms

class SettingsForm(forms.Form):
    THEME_CHOICES = [
        ('light', 'Светлая'),
        ('dark', 'Тёмная'),
    ]
    theme = forms.ChoiceField(choices=THEME_CHOICES, label='Тема')