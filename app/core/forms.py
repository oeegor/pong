# coding: utf-8

from django.forms import HiddenInput, ModelForm

from .models import SetResult


class SetResultForm(ModelForm):

    def set_hidden_inputs(self):
        for name in ['group', 'player1', 'player2', 'created_at', 'player1_approved', 'player2_approved']:
            self.fields[name].widget = HiddenInput()

    class Meta:
        model = SetResult
        exclude = []
