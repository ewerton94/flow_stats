from django.conf.urls import url
from .comparate_estimators.views import (
    comparate_estimators_view,
    SerieFromParameters,
    SerieResamplingDetail,
)

urlpatterns = (
    #url(r'^results/(?P<stats_name>.*)/(?P<station_id>[^/]+)/(?P<filters>.*)$', stats_view, name='stats_view'),
    url(r'^$', comparate_estimators_view, name='stats_study_view'),
    url(r'^study/$', comparate_estimators_view, name='stats_study_view'),
    url(
        r'^study/serie_from_parameters/$',
        SerieFromParameters.as_view(),
        name='serie_from_parameters'
    ),
    url(
        r'^study/resampling_serie/(?P<base_serie_id>[^/]+)$',
        SerieResamplingDetail.as_view(),
        name='serie_resampling_detail'
    ),
)
