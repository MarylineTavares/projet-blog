from django import forms

from shop.models import Order


class OrderForm(forms.ModelForm):
    quantity = forms.ChoiceField(choices=[(i,i) for i in range(1,11)])
    delete = forms.BooleanField(initial=False,
                                required=False)
    class Meta:
        model = Order
        fields = ["quantity"]


    def save(self, *args, **kwargs):
        if self.cleaned_data["delete"]:
            return self.instance.delete()
        return super().save(*args, **kwargs)