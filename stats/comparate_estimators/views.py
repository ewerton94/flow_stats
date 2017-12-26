# -*- coding: utf-8 -*-
from furl import furl
from datetime import datetime
import pandas as pd
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views import View
from core.graphs import plot_web
from ..models import BaseSerie, ResamplingSerie
from .forms import SerieFromParametersForm, ResamplingSerieForm
from ..resampling import Resampling, plot_comparative

'''
def export_xls(reduceds,stats_name):
    import xlwt
    response = HttpResponse(content_type ='application/ms-excel')
    filename='%s.xls'%stats_name
    response['Content-Disposition'] = 'attachment; filename=%s'%filename
    wb = xlwt.Workbook(encoding='utf-8')
    for reduced in reduceds:
        ws = wb.add_sheet(str(reduced.discretization)+str(reduced.variable))
        row_num = 0
        columns = []
        [columns.extend([('date',6000),(name,6000)]) for name in reduced.names]
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num][0], font_style)
            # set column width
            ws.col(col_num).width = columns[col_num][1]

        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1
        date_style=xlwt.XFStyle()
        date_style.num_format_str = 'dd/mm/yyyy'
        col_num = 0
        row_num += 1
        aux=row_num
        first=True
        for xy in reduced.xys:
            x,y = xy
            xy=list(zip(x,y))
            for row_num in range(len(x)):
                date=pd.to_datetime(xy[row_num][0],utc=True)
                ws.write(row_num+aux, col_num, datetime(date.year,date.month,date.day), date_style)
                ws.write(row_num+aux, col_num+1, xy[row_num][1], font_style)
            col_num+=2
    wb.save(response)
    return response
'''
def comparate_estimators_view(request,**kwargs):
    return render(request,'stats_study_information.html',{'resamplings':BaseSerie.objects.all()})

class SerieFromParameters(View):
    '''This class '''

    context = {"BASE_URL":""}

    def get(self, request, *args, **kwargs):
        self.context['form']=SerieFromParametersForm
        return render(request,'stats_information.html',self.context)

    def post(self, request, *args, **kwargs):
        form = SerieFromParametersForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            data['probability_or_aleatory']
            abreviation_distribution = data['distribution']
            sample_size = data['sample_size']
            probability_values = data['probability_values']
            if probability_values:
                probability_values = list(map(float,probability_values.split(',')))
            else:
                probability_values = []
            alpha = data['alpha']
            betha = data['betha']
            kappa = data['kappa']
            resampling = Resampling()
            parameters = {'alpha':alpha, 'betha':betha, 'kappa':kappa}
            serie = resampling.serie_from_parameters(parameters, distribution_abreviation=abreviation_distribution, n=sample_size, probabilities=probability_values)
            return HttpResponseRedirect("/stats/study/")        
        return self.get(request, *args, **kwargs)
        
class SerieResamplingDetail(View):
    '''This class '''

    context = {"BASE_URL":  ""}

    def get(self, request,base_serie_id, *args, **kwargs):
        base_serie = BaseSerie.objects.get(id=base_serie_id)
        #print(resampling_serie.probabilities)
        self.context['form'] = ResamplingSerieForm
        if not base_serie.probabilities:
            pass
        self.context['base_serie'] = base_serie
        self.context["graph"] = plot_web([[base_serie.data,base_serie.probabilities],], 'Cumulative Density Function',"percent","%",['quantile',],'m3/s',mode='markers')
        graphs = []
        for n in [5,]:#,10,15,20,25,30,50,100]:
            graphs.append(plot_comparative(base_serie, n))
            print(n)
        self.context["graphs"] = graphs
        return render(request,'resampling_information.html',self.context)

    def post(self, request, base_serie_id, *args, **kwargs):
        a = datetime.now()
        form = ResamplingSerieForm(request.POST)
        resampling_serie = BaseSerie.objects.get(id=base_serie_id)
        if form.is_valid():
            if ResamplingSerie.objects.filter(base_serie_id=base_serie_id):
                print('exists')
                return self.get(request, resampling_serie_id, *args, **kwargs)
            data=form.cleaned_data
            distribution = data['distribution']
            estimators = list(data['estimators'])
            sample_sizes = list(map(int,data['sample_sizes']))
            number_sample = int(data['number_sample'])
            resampling = Resampling()
            resamplings = []
            for n in sample_sizes:
                resamplings.extend(resampling.resampling_from_serie(resampling_serie, distribution, estimators, n, number_sample))     
            resampling_serie = ResamplingSerie.objects.bulk_create(resamplings)
        print(datetime.now()-a)
        return self.get(request, base_serie_id, *args, **kwargs)
