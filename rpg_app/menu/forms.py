from django import forms

class AccountForm(forms.Form):
    """アカウント用"""
    name = forms.CharField(label='アカウント名')
    money = forms.IntegerField(label='金額', initial=0)


class CharacterForm(forms.Form):
    """キャラクター用"""
    name = forms.CharField(label='name')
    job = forms.ChoiceField(label='job',
            choices = (
                    ('戦士','戦士'),
                    ('魔術師','魔術師'),
                    ('盗賊','盗賊'),
                    ('商人','商人'),
                    ),
                    required=True, widget=forms.widgets.Select
            )
            
class NameForm(forms.Form):
    """名前変更用"""
    name = forms.CharField(label='name')