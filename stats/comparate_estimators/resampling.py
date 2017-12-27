'''This module is about resampling'''
from random import uniform, choice
from core.graphs import box_plot
from ..frequency import FrequencyAnalysis, inverse_by_distribution
from ..models import ResamplingSerie, BaseSerie

def data_from_curve(curve, length=None, probabilities=None):
    '''Get data from curve'''
    stats = FrequencyAnalysis(curve['distribution'])
    if not length is None:
        probabilities = [uniform(0, 1) for i in range(length)]
    return stats.estimates_magnitudes(probabilities, curve['parameters']), probabilities

class Resampling(object):

    def create_base_serie(self, curve, data, n, probabilities=[]):
        serie = BaseSerie.objects.create(length=n, curve=curve, data=data, probabilities=probabilities)
        serie.save()
        return serie

    def serie_from_parameters(self, parameters, distribution_abreviation='gev', n=None, probabilities=[]):
        #distribution = distributions[distribution_abreviation]
        stats = FrequencyAnalysis(distribution_abreviation)
        curve = stats.get_curve(parameters, distribution_abreviation)
        if not probabilities and n is None:
            return "Error",False
        serie = BaseSerie.objects.filter(curve=curve).filter(length=n)
        if serie:
            return serie
        data, probabilities = data_from_curve(curve, n, probabilities)
        return self.create_base_serie(curve, data, n, probabilities=probabilities)

    def resampling_from_serie(self, base_serie, distribution, estimators, n, N):
        resamplings = []
        curves = []  
        print('iniciou tamanho '+str(n))
        for i in range(N):
            data = [choice(base_serie.data) for j in range(n)]
            stats = FrequencyAnalysis(distribution)
            for estimator in estimators:
                parameters = stats.estimate_parameters(data, estimator)
                curve =stats.get_curve(parameters, distribution)
                resamplings.append(ResamplingSerie(data=data, curve=curve, length=n, estimator=estimator, base_serie_id=base_serie.id))
        return resamplings

def plot_comparative(base_serie, length):
    y1 = []; y2 = []
    probabilities = [0.001, 0.002, 0.01, 0.1, 0.2, 0.3, 0.5, 0.7, 0.8, 0.9, 0.99, 0.998, 0.999]
    box = {}
    for serie in ResamplingSerie.objects.filter(base_serie_id=base_serie.id).filter(length=length).filter(estimator='mlh'):
        for p in probabilities:
            m = inverse_by_distribution['gev'](p, serie.curve['parameters']['kappa'],
                loc=serie.curve['parameters']['betha'],
                scale=serie.curve['parameters']['alpha']
            )
            if m<20000:
                box.setdefault(p, []).append(m) 
    list_plot = [[base_serie.data, base_serie.probabilities],]
    list_plot.extend([[box[key], str(key)] for key in box])
    print(list_plot)
    names_plot = ['original',]
    names_plot.extend(probabilities)

    return box_plot(
        list_plot,
        'Cumulative Density Function',
        "percent",
        "%",
        names_plot,
        'm3/s'
    )
