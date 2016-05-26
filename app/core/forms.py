# coding: utf-8

from django.forms import HiddenInput, ModelForm

from .models import SetResult


class SetResultForm(ModelForm):

    def set_inputs(self, player1, player2):
        for name in ['group', 'player1', 'player2', 'created_at', 'player1_approved', 'player2_approved']:
            self.fields[name].widget = HiddenInput()
        self.fields["player1_wins"].label = "%s wins" % player1.full_name
        self.fields["player1_points"].label = "%s points" % player1.full_name
        self.fields["player2_points"].label = "%s points" % player2.full_name

    class Meta:
        model = SetResult
        exclude = []
