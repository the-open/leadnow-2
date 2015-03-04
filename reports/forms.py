from django import forms


class QueryForm(forms.Form):
  query = forms.CharField(label='Query')

class ImportCsvForm(forms.Form):
  file_type = forms.CharField(label='File type',
                              widget=forms.RadioSelect(choices=(('e', 'Emails'), ('a', 'Actions'))))
  file_name = forms.FileField(label='File')

