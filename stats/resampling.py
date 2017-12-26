from random import uniform, choice
import pandas as pd
from core.graphs import plot_web
from .frequency import FrequencyAnalysis, distribution_functions
from .models import ResamplingSerie, BaseSerie

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
    magnitudes, probabilities = base_serie.data, base_serie.probabilities
    for serie in ResamplingSerie.objects.filter(base_serie_id=base_serie.id).filter(length=length).filter(estimator='mlh'):
        data = []
        for m in magnitudes:
            data.append(
                distribution_functions['gev'](m, serie.curve['parameters']['kappa'],
                loc=serie.curve['parameters']['betha'],
                scale=serie.curve['parameters']['alpha'])
            )
        df = pd.DataFrame(data)
        y1.append(df.quantile(0.25).values[0])
        y2.append(df.quantile(0.75).values[0])
    print(y1)
    print(y2)
    return plot_web(
        [[magnitudes, y1], [magnitudes, probabilities], [magnitudes, y2]],
        'Cumulative Density Function',
        "percent",
        "%",
        ['interval1', 'original', 'interval2'],
        'm3/s',
        mode='markers'
)
