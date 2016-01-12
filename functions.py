from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from django.contrib.auth.models import User
import base64
from django.shortcuts import render



''' upload image'''
def upload(request):
    imgData=request.POST['file']
    user_id=request.user.id
    print('sachin sharma')
    file_name=request.POST['name']
    split_img=imgData.partition(',')
    b64_str=split_img[2]
    fh = open('lender/static/uploads/'+file_name, "wb")
    fh.write(base64.b64decode(b64_str))
    save_path='/static/uploads/'+file_name
    fh.close()
    Lender.objects.filter(user_id=user_id).update(logo=save_path)
    return HttpResponse("success")


''' Sign in function '''
def sign_in(request):
    redirect = request.GET.get('redirect', '')
    email = request.POST['email']
    password = request.POST['password']

    user = authenticate(username=email, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/lender/#' + redirect)
        else:
            return HttpResponse("Account disabled!")
    else:
        #return HttpResponse("Invalid Login")
        return render(request, 'template.html', {'msg': ''})


