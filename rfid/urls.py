from django.urls import path
from .views import receive_rfid_data, new_etudiant, home

urlpatterns = [
    path('',home,name='home'),
    path('receive_rfid_data/',receive_rfid_data,name='receive_rfid_data'),
    path('new_etudiant/<str:uid>/',new_etudiant,name='new_etudiant'),
    
]
