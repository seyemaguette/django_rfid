from django.urls import path
from .views import receive_rfid_data, new_rfid,new_etudiant, home,new_fingerprint

urlpatterns = [
    path('',home,name='home'),
    path('receive_rfid_data/',receive_rfid_data,name='receive_rfid_data'),
    path('new_fingerprint/<str:fingerprint_id>/', new_fingerprint, name='new_fingerprint'),
    path('new_rfid/<str:uid>/',new_rfid,name='new_rfid'),
    path('new_etudiant/',new_etudiant,name='new_etudiant'),
    
]
