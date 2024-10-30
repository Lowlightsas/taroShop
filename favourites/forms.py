from django import forms


class FavouriteForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput)