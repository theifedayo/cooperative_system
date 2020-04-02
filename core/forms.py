from django import forms
from .models import Sub, Subscriber, Search, Pop
from django.core.validators import validate_slug
from django.core.exceptions import ValidationError
import os
import glob
import pandas as pd
import csv


class SearchForm(forms.Form):
    s_word = forms.CharField()

class SearchModelForm(forms.ModelForm):
    class Meta:
        model = Search
        fields = ['s_word']

class SubscriberForm(forms.Form):
    id_no = forms.IntegerField()
    sub_name = forms.CharField()
    phone_no = forms.IntegerField()
    no_of_plot = forms.IntegerField()
    payable_amount = forms.IntegerField()
    payment_starting_date = forms.CharField()
    supposed_end_date = forms.CharField()
    amount_paid = forms.IntegerField()

class SubscriberModelForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['id_no', 'sub_name','phone_no', 'no_of_plot', 'payable_amount',
            'payment_starting_date', 'supposed_end_date','amount_paid']



class SubForm(forms.Form):
    doc = forms.FileField()
    name = forms.CharField(max_length=22)




class SubModelForm(forms.ModelForm):

    class Meta:
        model = Sub
        fields = [ 'doc']


    def validate(self, value):
        # First run the parent class' validation routine
        super().validate(value)
        # Run our own file extension check
        file_extension = os.path.splitext(value.name)[1]
        if file_extension != '.xlsx':
            raise forms.ValidationError(
                 ('Invalid file extension'),
                 code='invalid'
            )
        return file_extension

class PopForm(forms.Form):
    name = forms.CharField(max_length=22)
