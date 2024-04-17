from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UID,Etudiant
# Create your views here.

uid = None  # Variable globale pour stocker l'UID
test = None  # Variable globale pour stocker l'UID


def home(request):
    return render(request,'home.html')
@csrf_exempt
def receive_rfid_data(request):
    global uid
    global test
    if request.method == 'POST':
        uid = request.POST.get('uid', None)
        test=Etudiant.objects.filter(uid=uid)
        UID.objects.get_or_create(uid=uid)
        print(uid)
        return render(request,'receive_rfid_data.html', {'uid': uid, 'test': test})
    
    elif request.method == 'GET':
            return render(request,'receive_rfid_data.html', {'uid': uid, 'test': test})
        
    else:

        return render(request,'receive_rfid_data.html', {'uid': uid, 'test': test})



def new_etudiant(request):
    uid= UID.objects.last
    if request.method == 'POST':
        uid = request.POST.get('uid')
        name = request.POST.get('name')
        if name :
            etudiant=Etudiant.objects.create(
            uid =uid,  
            name =name,  
            )
            etudiant.save()
            return redirect('/')
    return render(request,'new_etudiant.html',{"uid":uid})


 # created = Etudiant.objects.filter(uid=uid)
            # if name and name !='':
                # if created :
                #     messsage='Cette Carte est deja enregistree'
                #     print(messsage)
                #     render(request,'receive_rfid_data.html', {'uid': uid,'messsage':messsage})
                #     # return redirect('/receive_rfid_data/')
            #     else :
            #         messsage='Etudiant  enregistree'
            #         etudiant = Etudiant.objects.create(
            #         name=name,
            #         uid=uid

            #         )
            #         etudiant.save()
            #         return redirect('/receive_rfid_data/')

def check_rfid_data(request):
    global uid
    if request.method == 'POST':
        uid = request.POST.get('uid', None)
        if uid:
            return JsonResponse({'status': 'success', 'uid': uid})
        else:
            return JsonResponse({'status': 'error', 'message': 'UID not provided'})
    elif request.method == 'GET':
        if uid:
            return JsonResponse({'status': 'success', 'uid': uid})
        else:
            return JsonResponse({'status': 'error', 'message': 'UID not available'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST and GET methods allowed'})
 