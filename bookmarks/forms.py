from django import forms



class BukMarks(forms.Form):
    datas = forms.CharField(max_length=250)