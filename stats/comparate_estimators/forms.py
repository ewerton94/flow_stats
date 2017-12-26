from django import forms
from ..models import distributions, estimators
from django.utils.translation import gettext_lazy as _

class SerieFromParametersForm(forms.Form):
    probability_or_aleatory = forms.ChoiceField(label=_("Probability Values or Aleatory?")+":",required=False,widget=forms.Select(attrs={'class':'form-control'}),choices=
                                 ((1,_("Probabilities")),(2,_("Aleatory"))))
    probability_values = forms.CharField(label=_("Values of probability (numbers separateds by commas)")+":",required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    sample_size = forms.IntegerField(label=_("Size of sample")+":",required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    distribution = forms.ChoiceField(label=_("Distribution")+":",widget=forms.Select(attrs={'class':'form-control'}),choices=
                                 ((key, distributions[key]) for key in distributions))
    alpha = forms.FloatField(label=_("Apha")+":",widget=forms.TextInput(attrs={'class':'form-control'}))
    betha = forms.FloatField(label=_("Betha")+":",widget=forms.TextInput(attrs={'class':'form-control'}))
    kappa = forms.FloatField(label=_("Kappa")+":",widget=forms.TextInput(attrs={'class':'form-control'}))

class ResamplingSerieForm(forms.Form):
    sample_sizes = forms.MultipleChoiceField(label=_("Sample sizes")+":",required=True,widget=forms.SelectMultiple(attrs={'class':'form-control'}),choices=
                                 ((i,i) for i in [5,10,15,20,25,30,50,100]))
    number_sample = forms.IntegerField(label=_("Number of samples")+":",required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    distribution = forms.ChoiceField(label=_("Distribution")+":",widget=forms.Select(attrs={'class':'form-control'}),choices=
                                 ((key, distributions[key]) for key in distributions))
    estimators = forms.MultipleChoiceField(label=_("Estimators")+":",widget=forms.SelectMultiple(attrs={'class':'form-control'}),choices=
                                 ((key, estimators[key]) for key in estimators))