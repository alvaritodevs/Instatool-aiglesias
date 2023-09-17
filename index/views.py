from instagrapi import Client

from django.templatetags.static import static
import requests
import os
from PIL import Image
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from index.templatetags.functions import guardarPost
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from instagrapi import Client
from instagrapi.exceptions import BadPassword
from pathlib import Path
from django.contrib.auth.models import User
from .models import CuentaIg, PublicacionIg
from datetime import date
import sqlite3
import time
from datetime import datetime
import subprocess
from instagrapi.exceptions import RateLimitError
from django.http import HttpResponse


# Vistas aquí.

def index(request):
    if request.user.is_authenticated:

        return calendario(request)
    
    else:
        return render(request, 'index.html')


def acerca(request):

    return render(request,'acerca.html')


def contacto(request, context=None):

    return render(request,'contacto.html',context)


def register(request):

    return render(request,'register.html')



@login_required
def calendario(request,iglogin=None,iguser=None):

    publicaciones = PublicacionIg.objects.filter(username=request.user.username)
    print(request.user.username)

    try:
        cuenta= CuentaIg.objects.get(username=request.user.username)
        if cuenta is not None:
            iglogin="exito"
            iguser=cuenta.iguser
        else:
            iglogin=None

        context = {'publicaciones': publicaciones, 'iglogin': iglogin, 'iguser': iguser}
        return render(request,'calendario.html',context)
    
    except Exception as error:

        context = {'publicaciones': publicaciones, 'iglogin': iglogin, 'iguser': iguser}
        return render(request,'calendario.html',context)

@csrf_exempt
def editar_post(request,iglogin=None,iguser=None):

    idpost = request.POST.get('id')
    publicacion = PublicacionIg.objects.get(id=idpost)

    try:
        cuenta= CuentaIg.objects.get(username=request.user.username)
        if cuenta is not None:
            iglogin="exito"
            iguser=cuenta.iguser
        else:
            iglogin=None

        context = {'iglogin': iglogin, 'iguser': iguser,'publicacion': publicacion}
        return render(request,'calendarioedit.html',context)
    
    except Exception as error:

        context = {'iglogin': iglogin, 'iguser': iguser,'publicacion': publicacion}
        return render(request,'calendarioedit.html',context)



@login_required
def datos(request, usuariosNoSigo=None, usuariosNoSeguidores=None, masSeguidoSeguidores= None, Seguidores= None, usuarioPic=None, masSeguidoSeguidos= None,misDatos=None,error=None):

    iglogin=None
    iguser=None

    try:
        cuenta= CuentaIg.objects.get(username=request.user.username)

        if cuenta is not None:
            iglogin="exito"
            iguser=cuenta.iguser
        else:
            iglogin=None

        context = {'iglogin': iglogin, 'iguser': iguser, 'usuariosNoSigo': usuariosNoSigo, 'usuariosNoSeguidores': usuariosNoSeguidores, 'masSeguidoSeguidores': masSeguidoSeguidores, 'Seguidores':Seguidores, 'usuarioPic':usuarioPic,'masSeguidoSeguidos':masSeguidoSeguidos,'misDatos':misDatos,'error':error }    

        return render(request,'homedatos.html',context)
    
    except Exception as error:

        iglogin=None
        iguser=None

        print(error)

        context = {'iglogin': iglogin, 'iguser': iguser, 'usuariosNoSigo': usuariosNoSigo, 'usuariosNoSeguidores': usuariosNoSeguidores, 'masSeguidoSeguidores': masSeguidoSeguidores, 'Seguidores':Seguidores, 'usuarioPic':usuarioPic,'masSeguidoSeguidos':masSeguidoSeguidos,'misDatos':misDatos,'error':error }    

        return render(request,'homedatos.html',context)


@login_required
def comentPage(request,error=None):

    try:
        cuenta= CuentaIg.objects.get(username=request.user.username)
        if cuenta is not None:
            iglogin="exito"
            iguser=cuenta.iguser
        else:
            iglogin=None

        context = {'iglogin': iglogin, 'iguser': iguser,'error':error}
        return render(request,'comentpage.html',context)
    
    except Exception as error:

        context = {'iglogin': iglogin, 'iguser': iguser,'error':error}
        return render(request,'comentpage.html',context)





@csrf_exempt
def login_user(request):

    try:

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            
            iguser = None

            login(request, user)


            context = {'user': user,'iguser': iguser}

            return calendario(request)

        else:

            context={'login': 'error'}
            return render(request,'index.html',context)

    except Exception as error:

        print("Hubo un error", error)
        context={'login': 'error'}
        return render(request,'index.html',context)

    finally:
        pass



@csrf_exempt
def register_user(request):
    
    try:

        username= request.POST.get('username')
        password= request.POST.get('password')

        user = User.objects.create_user(username=username, email=username, password=password)

        if user is not None:

            context={'registro': 'exito','usuario': username}
            return render(request, 'index.html', context=context)
        
        else:

            context={'registro': 'fallido'}
            return render(request, 'register.html', context=context)
                
    except Exception as error:
        print("Hubo un error", error)
        context={'registro': 'fallido'}
        return render(request, 'register.html', context=context)
       
    finally:
        pass

@csrf_exempt
def logout_user(request):

    print("has cerrado sesion")

    logout(request)

    return render(request, 'index.html')



# INSTAGRAM FUNCTIONS
@csrf_exempt
def instaLogin(request):

        iguser = request.POST.get('iguser')
        igpass = request.POST.get('igpass')
        
        print(iguser, ' klk ', igpass)

        try:
            client = Client()

            client.login(username=iguser, password=igpass)

            existe=CuentaIg.objects.filter(username=request.user.username)

            print(existe)


            if existe is None:

                cuenta_ig = CuentaIg(username=request.user.username, iguser=iguser, ispass=igpass)
                cuenta_ig.save()    

            else:
                
                print("actualizada")

                cuenta_ig = CuentaIg.objects.get(username=request.user.username)
                cuenta_ig.iguser = iguser
                cuenta_ig.igpass = igpass
                cuenta_ig.save()



            return calendario(request,'exito',iguser)
        

        except Exception as e:
            print("Error occurred during login:", str(e))

            if str(e)== "The password you entered is incorrect. Please try again.":
                context={'iglogin': 'errorcredenciales'}

                print(e)

                return calendario(request,'errorcredenciales',None)
            elif str(e)== "Invalid Parameters":
                print("asi es")
                
                context={'iglogin': 'errorgeneral'}
                return calendario(request,'errorgeneral',None)
            else:

                cuenta_ig = CuentaIg(username=request.user.username, iguser=iguser, igpass=igpass)
                cuenta_ig.save()  
                return calendario(request,'exito',iguser)

        
def cerrarSesionIg(request):
    
    cuenta= CuentaIg.objects.get(username=request.user.username)
    cuenta.delete()

    return calendario(request)


# Me siguen y no sigo


def not_following(request):

    try:

        cuentaObj = CuentaIg.objects.get(username=request.user.username)

        igUser = cuentaObj.iguser
        igPass = cuentaObj.igpass

        client = Client()
        client.login(igUser, igPass)

        usuarioSeguidos= []
        usuarioSeguidores= []

        following_users = client.user_following(user_id=client.user_id)

        followers = client.user_followers(user_id=client.user_id)

        for user_id, user_object in following_users.items():

            username = user_object.username
            usuarioSeguidos.append(username)

        
        for user_id, user_object in followers.items():

            username = user_object.username
            usuarioSeguidores.append(username)


        usuariosNoSigo = [usuario for usuario in usuarioSeguidores if usuario not in usuarioSeguidos]


        client.logout()
        return datos(request, usuariosNoSigo, None, None, None)
    
    except Exception as e:

        client.logout()
        return datos(request, None, None, None, None, None, None, None,error=e)


# Sigo y no me siguen


def not_followers(request):

    try:
        cuentaObj = CuentaIg.objects.get(username=request.user.username)

        igUser = cuentaObj.iguser
        igPass = cuentaObj.igpass

        client = Client()
        client.login(igUser, igPass)

        usuarioSeguidos= []
        usuarioSeguidores= []

        following_users = client.user_following(user_id=client.user_id,use_cache=False,amount=200)

        followers = client.user_followers(user_id=client.user_id)

        for user_id, user_object in following_users.items():

            username = user_object.username
            usuarioSeguidos.append(username)
            
        for user_id, user_object in followers.items():

            username = user_object.username
            usuarioSeguidores.append(username)

        usuariosNoSeguidores = [usuario for usuario in usuarioSeguidos if usuario not in usuarioSeguidores]
        print(usuariosNoSeguidores)

        client.logout()
        return datos(request, None, usuariosNoSeguidores, None, None)
    
    except Exception as e:


        client.logout()
        return datos(request, None, None, None, None, None, None, None,error=e)




# Usuario más seguido


def most_followed_followers(request):
    
    try:
        cuentaObj = CuentaIg.objects.get(username=request.user.username)

        igUser = cuentaObj.iguser
        igPass = cuentaObj.igpass

        client = Client()
        client.login(igUser, igPass)

        followers_users = client.user_followers(user_id=client.user_id)

        followers_counts = []

        for username in followers_users:
            user_info = client.user_info(username)
            followers_counts.append((username, user_info.follower_count))
            account_id = username
            usuario = client.username_from_user_id(account_id)
            print(usuario)

        followers_counts.sort(key=lambda x: x[1], reverse=True)

        most_followed_user = followers_counts[0]

        masSeguidoSeguidores = client.username_from_user_id(most_followed_user[0])
        seguidores = most_followed_user[1]
        
        client.logout()
        return datos(request, None, None, masSeguidoSeguidores, seguidores)

    except Exception as e:

        client.logout()
        return datos(request, None, None, None, None, None, None, None,error=e)

def most_followed_following(request):

    try:
        cuentaObj = CuentaIg.objects.get(username=request.user.username)

        igUser = cuentaObj.iguser
        igPass = cuentaObj.igpass

        client = Client()
        client.login(igUser, igPass)

        seguidores=0
        masSeguidoSeguidos="juan"

        following_users = client.user_following(user_id=client.user_id)

        followers_counts = []

        for username in following_users:
            user_info = client.user_info(username)
            followers_counts.append((username, user_info.follower_count))

        followers_counts.sort(key=lambda x: x[1], reverse=True)

        most_followed_user = followers_counts[0]

        masSeguidoSeguidos = client.username_from_user_id(most_followed_user[0])
        seguidores = most_followed_user[1]

        client.logout()
        return datos(request, None, None, None, seguidores, None, masSeguidoSeguidos)

    except Exception as e:

        client.logout()
        return datos(request, None, None, None, None, None, None, None,error=e)


# Foto de perfil completa


def fullProfile(request):

    try:
        cuentaObj = CuentaIg.objects.get(username=request.user.username)
        print("consigue user")
        igUser = cuentaObj.iguser
        igPass = cuentaObj.igpass

        client = Client()
        client.login(igUser, igPass)

        #client.login_by_sessionid()

        usuarioPic = request.POST.get('usuarioPic')

        user = client.user_info_by_username(usuarioPic)

        photo_url = user.profile_pic_url_hd

        response = requests.get(photo_url)
        file_path = os.path.join('index', 'static', 'img', 'full', usuarioPic+'.jpg')


        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
                print('Foto descargada con éxito.')
        else:
            print('Error descargando foto.')

        client.logout()

        return datos(request, None, None, None, None, '/img/full/'+usuarioPic+'.jpg')

    except Exception as e:

        return datos(request, None, None, None, None, None, None, None,error=e)


def todosMisDatos(request):

    try:

        cuentaObj = CuentaIg.objects.get(username=request.user.username)

        igUser = cuentaObj.iguser
        igPass = cuentaObj.igpass

        client = Client()
        client.login(igUser, igPass)
        
        misDatos=client.account_info()


        print(misDatos)

        client.logout()


        return datos(request, None, None, None, None, None, None, misDatos)
    
    except Exception as e:

        return datos(request, None, None, None, None, None, None, None,error=e)
    



# VISTA COMMENTS
# VISTA COMMENTS
# VISTA COMMENTS


def commenTimeline(request):

    try:
        cuentaObj = CuentaIg.objects.get(username=request.user.username)

        igUser = cuentaObj.iguser
        igPass = cuentaObj.igpass

        client = Client()
        client.login(igUser, igPass)

        timeline_posts = client.get_timeline_feed()

        comentario = request.POST.get('comentario')

        if comentario is not None:
            pass
        else:
            comentario = 'Hola.'

        print(len(timeline_posts["feed_items"]) )     

                    #print(timeline_posts["feed_items"][i]["explore_story"]["id"])


        for i in range(6):

            client.media_comment(timeline_posts["feed_items"][i]["explore_story"]["id"], comentario)

        return comentPage(request)
    
    except Exception as e:

        return comentPage(request,e)



def commentHashtag(request):
    
    try:
        cuentaObj = CuentaIg.objects.get(username=request.user.username)

        igUser = cuentaObj.iguser
        igPass = cuentaObj.igpass

        client = Client()
        client.login(igUser, igPass)

        hashtag = request.POST.get('hashtag')
        comentario = request.POST.get('comentario')

        if comentario is not None:
            pass
        else:
            comentario = 'Hola.'

        posts = client.hashtag_medias_top(hashtag)

        
        
        num=0

        for post in posts:
            if num<8:
                media_id = post.pk
                client.media_comment(media_id, comentario)
                num += 1

            else:
                break 

        return comentPage(request)

    except Exception as e:

        return comentPage(request,e)



def likeHashtag(request):
        
    try:
        cuentaObj = CuentaIg.objects.get(username=request.user.username)

        igUser = cuentaObj.iguser
        igPass = cuentaObj.igpass

        client = Client()
        client.login(igUser, igPass)

        hashtag = request.POST.get('hashtag')
        posts = client.hashtag_medias_top(hashtag)

        num=0

        for post in posts:
            if num<8:
                media_id = post.pk
                client.media_like(media_id)
                num += 1

            else:
                break 

        return comentPage(request)

    except Exception as e:

        return comentPage(request,e)

def likeTimeline(request):

    try:
        cuentaObj = CuentaIg.objects.get(username=request.user.username)

        igUser = cuentaObj.iguser
        igPass = cuentaObj.igpass

        client = Client()
        client.login(igUser, igPass)

        client.logout()

        timeline_posts = client.get_timeline_feed()

        print(len(timeline_posts["feed_items"]) )     

        for i in range(8):
            
            client.media_like(timeline_posts["feed_items"][i]["explore_story"]["id"])


        return comentPage(request)
    
    except Exception as e:

        return comentPage(request,e)




def followHashtag(request):

    try:
        cuentaObj = CuentaIg.objects.get(username=request.user.username)

        igUser = cuentaObj.iguser
        igPass = cuentaObj.igpass

        client = Client()
        client.login(igUser, igPass)

        hashtag = request.POST.get('hashtag')
        posts = client.hashtag_medias_top(hashtag)

        num=0

        for post in posts:

            if num<8:
                username = post.user
                
                client.user_follow(username.pk)
                num += 1

            else:
                break 

        return comentPage(request)

    except Exception as e:

        return comentPage(request,e)

@csrf_exempt
def guardar_post(request):

    piefoto = request.POST.get('piefoto')
    fecha = request.POST.get('fecha')
    imagenfile = request.FILES['imagen']

    print(fecha)

    publicacion = PublicacionIg()

    # Set attribute values
    publicacion.username = request.user.username
    publicacion.piefoto = piefoto
    publicacion.fecha = fecha
    publicacion.imagen = "image.jpg"

    publicacion.save()

    nombreFichero = str(publicacion.id) + '_' + imagenfile.name

    file_path = os.path.join('index', 'static', 'img', 'upload', nombreFichero)

    file_pathdatabase = os.path.join('img', 'upload', nombreFichero)

    with open(file_path, 'wb') as destination:
        for chunk in imagenfile.chunks():
            destination.write(chunk)

    publicacion.imagen = file_pathdatabase
    publicacion.save()

    return calendario(request)


@csrf_exempt
def guardar_editedpost(request):

    idpost = request.POST.get('id')
    piefoto = request.POST.get('piefoto')
    fecha = request.POST.get('fecha')
    new_image = request.FILES.get('newimage')
    newruta_image = None
    publicacion= PublicacionIg.objects.get(id=idpost)

    print(request.FILES)
    if new_image:

        old_image= publicacion.imagen

        os.remove(os.path.join('index', 'static', old_image))

        nombreFichero = str(publicacion.id) + '_' + new_image.name

        file_path = os.path.join('index', 'static', 'img', 'upload', nombreFichero)

        file_pathdatabase = os.path.join('img', 'upload', nombreFichero)

        # Save the file
        with open(file_path, 'wb') as destination:
            for chunk in new_image.chunks():
                destination.write(chunk)

        newruta_image = file_pathdatabase
        publicacion.imagen = newruta_image

    publicacion.piefoto = piefoto
    publicacion.fecha = fecha
    publicacion.save()

    return calendario(request)



@csrf_exempt
def eliminar_post(request):

    idpost = request.POST.get('id')

    publicacion = PublicacionIg.objects.get(id=idpost)
    publicacion.delete()

    return calendario(request)

@csrf_exempt
def subir_posts(request):

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y/%m/%d %H:%M")

    print(formatted_datetime)

    publicaciones = PublicacionIg.objects.filter()

    for publicacion in publicaciones:

        formatted_datetime = current_datetime.strftime("%Y/%m/%d %H:%M")

        format_str = "%Y/%m/%d %H:%M"

        fecha = datetime.strptime(publicacion.fecha, format_str)
        hoy = datetime.strptime(formatted_datetime, format_str)

        if fecha < hoy:

            cuentaObj = CuentaIg.objects.get(username=request.user.username)
            cl = Client()
            cl.login(cuentaObj.iguser,cuentaObj.igpass)

            pie_foto = publicacion.piefoto

            print("index\\static\\"+publicacion.imagen)

            cl.photo_upload("index\\static\\"+publicacion.imagen , pie_foto)
            cl = None

        else:
            print("llegara")


    return calendario(request)




