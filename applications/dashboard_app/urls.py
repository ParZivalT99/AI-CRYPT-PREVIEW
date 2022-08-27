from django.urls import path 
from . import views

app_name = "dashboard_app"
urlpatterns = [
    path('',views.InicioView.as_view(),name='inicio'),
    path('dashboard/inicio/',views.InicioView.as_view(),name='inicio_d'),
    path('dashboard/prediction/',views.PredictionView.as_view(),name='prediction'),
    path('dashboard/prediction-consult/',views.PredictionConsultView.as_view(),name='prediction-consult'),
    path('dashboard/history/',views.HistoryPredictionView.as_view(),name='history'),
    path('dashboard/terms-and-uses/',views.TermsAndUsesView.as_view(),name='terms-and-uses'),
]
