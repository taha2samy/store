from django.urls import path
from .views import ElementListView,ElementUpdateView,ElementDeleteView,ElementCreateView 
from .views import SubElementUpdateView,SubElementCreateView,SubElementDeleteView,SubElementListView
urlpatterns = [
    path('element/list/', ElementListView.as_view(), name='main_element_list'),
    path("element/create/",ElementCreateView.as_view(),name='main_element_create'),
    path("element/update/<int:pk>/",ElementUpdateView.as_view(),name="main_element_update"),
    path("element/delete/<int:pk>/",ElementDeleteView.as_view(),name="main_element_delete"),
    path("subelement/list/", SubElementListView.as_view(), name='sub_element_list'),
    path("subelement/create/", SubElementCreateView.as_view(), name='sub_element_create'),
    path("subelement/update/<int:pk>/", SubElementUpdateView.as_view(), name='sub_element_update'),
    path("subelement/delete/<int:pk>/", SubElementDeleteView.as_view(), name='sub_element_delete'),
    
]