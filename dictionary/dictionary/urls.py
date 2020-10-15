from django.urls import path

from . import views

app_name = 'dictionary'

urlpatterns = [
    path('', views.DictionaryListView.as_view(), name='dictionary-list-view'),
    path('<int:pk>/', views.DictionaryDetailView.as_view(), name='dictionary-info-view'),
    path('add/', views.DictionaryCreateView.as_view(), name='create-dictionary'),
    path('<int:pk>/words/', views.WordListView.as_view(), name='word-list-view'),
    path('<int:pk>/words/add/', views.WordCreateView.as_view(), name='create-word-view'),
    path('<int:pk_dict>/words/delete/<int:pk>', views.WordDeleteView.as_view(), name='delete-word-view'),
    path('<int:pk_dict>/words/<int:pk>/update/', views.WordUpdateView.as_view(), name='update-word-view'),
    path('<int:pk>/texts/', views.TextListView.as_view(), name='text-list-view'),
    path('<int:pk>/texts/add/', views.TextCreateView.as_view(), name='create-text-view'),
    path('<int:pk_dict>/texts/<int:pk>/', views.TextDetailView.as_view(), name='text-info-view'),
    path('<int:pk_dict>/texts/update/<int:pk>/', views.TextUpdateView.as_view(), name='update-text-view')
]
