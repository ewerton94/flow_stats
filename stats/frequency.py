from scipy.stats import genpareto, genextreme#kstest, chisquare, anderson
from lmoments3 import distr

functions_fit = {'gev-mlh':genextreme.fit,'gev-lmom':distr.gev.lmom_fit}
inverse_by_distribution = {'gev':genextreme.ppf}
distribution_functions = {'gev':genextreme.cdf}

class FrequencyAnalysis(object):
    '''This funtion manages the frequency analysis'''
    def __init__(self, distribution):
        '''Initial'''
        self.distribution = distribution
    def estimate_parameters(self, data, estimator):
        '''This method estimates parameters from data and estimator'''
        parameters = functions_fit['%s-%s'%(self.distribution, estimator)](data)
        if hasattr(parameters, 'values'):
            parameters = list(parameters.values())
        return {'kappa': parameters[0], 'alpha': parameters[2], 'betha': parameters[1]}

    def estimates_magnitudes(self, probabilities, parameters):
        '''This method estimates magnitudes from probabilities and parameters'''
        if probabilities is None:
            return []
        data = [
            inverse_by_distribution[self.distribution](
                p,
                parameters['kappa'],
                loc=parameters['betha'],
                scale=parameters['alpha']) for p in probabilities]
        return data

    def get_curve(self, parameters, distribution):
        '''Gets dictionary of curve'''
        return {'distribution': distribution, 'parameters':parameters}
