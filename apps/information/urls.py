from django.conf.urls import url
from . import views

urlpatterns = (
    url(r'^patient/(?P<patient_id>-?\d+)/plot/(?P<diag_id>-?\d+)/$', views.PlotECG.as_view(), name='url_diagnosis_plot'),
    url(r'^patient/(?P<patient_id>-?\d+)/edit/(?P<diag_id>-?\d+)/$', views.diagnosis_edit, name='url_diagnosis_edit'),
    url(r'^patient/(?P<patient_id>-?\d+)/processing/$', views.processing_parameters, name='url_processing_parameters'),
    #url(r'^patient/(?P<patient_id>-?\d+)/processing/(?P<signal_id>-?\d+)/$', views.processing_plot, name='url_processing_plot'),
    url(r'^patient/(?P<patient_id>-?\d+)/processing/(?P<diag_id>-?\d+)/$', views.PlotsECG.as_view(), name='url_processing_plots'),
)