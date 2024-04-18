from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import UID,Etudiant
# Create your views here.

uid = None  # Variable globale pour stocker l'UID
test = None  # Variable globale pour stocker l'UID
check = None  # Variable globale pour stocker l'UID


def home(request):
    return render(request,'home.html')
@csrf_exempt
def receive_rfid_data(request):
    global uid
    global test
    global check
    if request.method == 'POST':
        uid = request.POST.get('uid', None)
        # UID.objects.create(uid=uid).save()
        check=Etudiant.objects.filter(uid=uid)
        if check :
            test=get_object_or_404(Etudiant,uid=uid)
        print(uid)
        return render(request,'receive_rfid_data.html', {'uid': uid, 'test': test,'check':check})
    
    elif request.method == 'GET':
            check=Etudiant.objects.filter(uid=uid)
            if check :
                test=get_object_or_404(Etudiant, uid=uid)
                print(test)
            
            return render(request,'receive_rfid_data.html', {'uid': uid, 'test': test,'check':check})
        
    else:

        return render(request,'receive_rfid_data.html', {'uid': uid, 'test': test,'check':check})



def new_etudiant(request,uid):
    # uid= get_object_or_404(UID,uid=uid)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name.isalpha() :
            etudiant=Etudiant.objects.create(
            uid =uid,  
            name =name,  
            )
            etudiant.save()
            messages.success(request, "L'etudiant a ete bien ajoute")
            return redirect('/')
        else  :
            messages.error(request, "Le nom doit comporter uniquement des caractères alphabétiques et doit pas etre nul")

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
 