# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField, JSONField

estimators = {'lmom':"L-Moments", 'mlh': "Maximum Likely-Hood"} 
distributions = {'gev': "Generalized Extreme Value"}    

'''
class ProbabilityCurve(models.Model):
    """This class manages probability curves"""
    distribution = models.CharField(max_length=5, verbose_name=_('distribution'), blank=True, choices=((key,distributions[key]) for key in distributions))
    alpha = models.FloatField(verbose_name=_('alpha'))
    betha = models.FloatField(verbose_name=_('betha'))
    kappa = models.FloatField(verbose_name=_('kappa'))

    @property
    def parameters(self):
        return {"alpha": self.alpha, "betha": self.betha, 'kappa': self.kappa}
'''
class BaseSerie(models.Model):
    """This class manages series"""
    length = models.IntegerField(verbose_name=_('length'))
    curve = JSONField(verbose_name=_('curve'), blank=True, null=True)
    data = ArrayField(models.FloatField(), verbose_name=_('data'), blank=True, null=True)
    probabilities = ArrayField(
        models.FloatField(),
        verbose_name=_('probabilities'),
        blank=True,
        null=True
    )
    @property
    def distribution(self):
        '''property: distribution'''
        return self.curve['distribution']
    @property
    def alpha(self):
        '''property: alpha'''
        return self.curve['parameters']['alpha']
    @property
    def betha(self):
        '''property: betha'''
        return self.curve['parameters']['betha']
    @property
    def kappa(self):
        '''property: kappa'''
        return self.curve['parameters']['kappa']

class ResamplingSerie(models.Model):
    """This class manages resampling series"""
    base_serie_id = models.IntegerField(verbose_name=_('base_serie'))
    length = models.IntegerField(verbose_name=_('length'))
    curve = JSONField(verbose_name=_('curve'), blank=True, null=True)
    data = ArrayField(models.FloatField(), verbose_name=_('data'), blank=True, null=True)
    probabilities = ArrayField(
        models.FloatField(), verbose_name=_('probabilities'), blank=True, null=True
    )
    estimator = models.CharField(
        max_length=5,
        verbose_name=_('estimator'),
        blank=True,
        choices=((key, estimators[key]) for key in estimators)
    )
