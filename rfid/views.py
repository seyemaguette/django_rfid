from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import UID,Etudiant
# Create your views here.

uid = None  # Variable globale pour stocker l'UID
fingerprint_id = None
test = None
check_uid = False
check_fingerprint_id = False
testuid = None
testfingerprint_id = None
response_data = {}

def home(request):
    return render(request,'home.html')




@csrf_exempt
def receive_rfid_data(request):
    global uid
    global fingerprint_id
    global check_uid
    global check_fingerprint_id
    global testuid
    global testfingerprint_id
    # uid = 'kk3nnn65'
        
    if request.method == 'POST':
        uid = request.POST.get('uid', None)
        fingerprint_id = request.POST.get('fingerprint_id', None)
        if uid:
            print(f"****** UID: {uid} *********")
        if fingerprint_id :
             print(f"****** Fingerprint ID: {fingerprint_id} *********")

        
        return render(request, 'receive_rfid_data.html', {'uid': uid, 'fingerprint_id': fingerprint_id, 'testfingerprint_id': testfingerprint_id, 'testuid': testuid,'check_uid': check_uid, 'check_fingerprint_id': check_fingerprint_id})

    elif request.method == 'GET':
        if uid:
            check_uid = Etudiant.objects.filter(uid=uid).exists()
            if check_uid:
                testuid = get_object_or_404(Etudiant, uid=uid)
                print(f"testuid: {testuid}")
            else:
                print(f"No student found with UID {uid}")
            return render(request, 'receive_rfid_data.html', {'uid': uid, 'fingerprint_id': fingerprint_id, 'testfingerprint_id': testfingerprint_id, 'testuid': testuid,'check_uid': check_uid, 'check_fingerprint_id': check_fingerprint_id})
        
        if fingerprint_id:
            check_fingerprint_id = Etudiant.objects.filter(fingerprint_id=fingerprint_id).exists()
            if check_fingerprint_id:
                testfingerprint_id = get_object_or_404(Etudiant, fingerprint_id=fingerprint_id)
                print(f"testfingerprint_id: {testfingerprint_id}")
            else:
                print(f"No student found with fingerprint_id {fingerprint_id}")

            return render(request, 'receive_rfid_data.html', {'uid': uid, 'fingerprint_id': fingerprint_id, 'testfingerprint_id': testfingerprint_id, 'testuid': testuid,'check_uid': check_uid, 'check_fingerprint_id': check_fingerprint_id})

        return render(request, 'receive_rfid_data.html', {'uid': uid, 'fingerprint_id': fingerprint_id, 'testfingerprint_id': testfingerprint_id, 'testuid': testuid,'check_uid': check_uid, 'check_fingerprint_id': check_fingerprint_id})


def new_etudiant(request):
    # uid= get_object_or_404(UID,uid=uid)
    if request.method == 'POST':
        codePermenant = request.POST.get('codePermenant')
        name = request.POST.get('name')
        if codePermenant.isdigit() :
            etudiant=Etudiant.objects.create(
            name =name,  
            codePermenant =codePermenant,  
            )
            etudiant.save()
            messages.success(request, "L'etudiant a ete bien ajoute")
            return redirect('/')
        else  :
            messages.error(request, "Le code permenant doit comporter uniquement des caractères numeriques et doit pas etre nul")

    return render(request,'new_etudiant.html',{"uid":uid})


def new_fingerprint(request,fingerprint_id):
    # uid= get_object_or_404(UID,uid=uid)
    if request.method == 'POST':
        codePermenant = request.POST.get('codePermenant')
        if codePermenant.isdigit() :
            etudiantexist=Etudiant.objects.filter(codePermenant=codePermenant).exists()
            if etudiantexist :
                etudiant=Etudiant.objects.get(codePermenant=codePermenant)
                finger= etudiant.fingerprint_id
                if finger :
                    messages.error(request, "L'etudiant "+codePermenant+" est deja enrgistrer son empreinte")
                else :
                    etudiant.fingerprint_id =fingerprint_id  
                    etudiant.save()
                    messages.success(request, "L'empreinte a ete bien ajoute")
                    return redirect('/')

            else  :
                messages.error(request, "Il n'y a d'etudiant ayant un code permenant "+codePermenant)
        else  :
            messages.error(request, "Le code permenant doit comporter uniquement des caractères numeriques et doit pas etre nul")
            return render(request,'new_fingerprint.html',{"fingerprint_id":fingerprint_id})

    return render(request,'new_fingerprint.html',{"fingerprint_id":fingerprint_id})


def new_rfid(request,uid):
    # uid= get_object_or_404(UID,uid=uid)
    if request.method == 'POST':
        codePermenant = request.POST.get('codePermenant')
        if codePermenant.isdigit() :
            etudiantexist=Etudiant.objects.filter(codePermenant=codePermenant).exists()
            if etudiantexist :
                    etudiant=Etudiant.objects.get(codePermenant=codePermenant)
                    uid_exist=etudiant.uid 
                    if uid_exist :
                        messages.error(request, "L'etudiant "+codePermenant+" est deja enrgistrer sa carte")
                    else  :
            
                        etudiant.uid =uid  
                        etudiant.save()
                        messages.success(request, "L'uid de la carte a ete bien ajoute")
                        return redirect('/')
            else:
                        messages.error(request, "Il n'y a d'etudiant ayant un code permenant "+codePermenant)

        else  :
            messages.error(request, "Le nom doit comporter uniquement des caractères alphabétiques et doit pas etre nul")

    return render(request,'new_rfid.html',{"uid":uid})
