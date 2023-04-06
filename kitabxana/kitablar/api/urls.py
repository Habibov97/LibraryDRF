from django.urls import path
from kitablar.api import views as api_views

urlpatterns = [
    path('kitablar/',api_views.KitabListCreateAPIView.as_view(), name= 'kitab-listesi'),
    path('kitablar/<int:pk>/',api_views.KitabDetailAPIView.as_view(), name= 'yorum-listesi'),
    path('kitablar/<int:kitab_pk>/yorum_yap', api_views.YorumCreateAPIView.as_view(), name= 'kitab-yorumla'),
    path('yorumlar/<int:pk>', api_views.YorumDetailAPIView.as_view(), name= 'yorumlar'),

]