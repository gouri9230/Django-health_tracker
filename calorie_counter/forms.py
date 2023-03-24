from django import forms

class QueryForm(forms.Form):
    query = forms.CharField(label='query', max_length=50)
    
class BmiCalForm(forms.Form):
    age = forms.IntegerField(label='Age', widget=forms.TextInput(attrs={'placeholder': 'only for 18 or above'}))
    weight = forms.FloatField(label='Weight', widget=forms.TextInput(attrs={'placeholder': 'in kg'}))
    height = forms.FloatField(label='Height', widget=forms.TextInput(attrs={'placeholder': 'in cm'}))
    gender = forms.ChoiceField(label= 'Gender',choices=[('male', 'Male'), ('female', 'Female')])
    exercise = forms.ChoiceField(label= 'Exercise',choices=[("sedentary","Sedentary"), ("light","Light exercise(1-3 days/week)"),
                                                        ("moderate","Moderate(3-5 days/week)"),("active","Active(6-7 days/week)"),
                                                        ("very-active","Very Active(hard exercise 6-7 days/week)")])
    

