from django.urls import path, include
from . import views


urlpatterns = [

    path('social-auth/', include('social_django.urls', namespace='social')),
    #Vistas de páginas

    path('', views.index, name="inicio"),
    path('calendario/', views.calendario, name="calendario"),
    path('datos/', views.datos, name="homedatos"),
    path('comentPage/', views.comentPage, name="comentPage"),
    path('register/', views.register, name="register"),
    path('acerca/', views.acerca, name="acerca"),
    path('contacto/', views.contacto, name="contacto"),


    #Vistas de logins

    path('loginUser', views.login_user, name="loginUser"),
    path('registerUser', views.register_user, name="registerUser"),
    path('logout/', views.logout_user, name="logout"),
    path('instalogin/', views.instaLogin, name="instaLogin"),
    path('cerrarSesionIg/', views.cerrarSesionIg, name="cerrarSesionIg"),


    #Vistas de funciones

    path('deletePost/', views.eliminar_post, name="deletePost"),
    path('guardarPost', views.guardar_post, name="guardarPost"),
    path('guardarEditedPost', views.guardar_editedpost, name="guardar_editedpost"),
    path('editPost/', views.editar_post, name="editPost"),
    path('subir_posts/', views.subir_posts, name="subir_posts"),
    
    path('not_following/', views.not_following, name="not_following"),
    path('not_followers/', views.not_followers, name="not_followers"),
    path('most_followed_followers/', views.most_followed_followers, name="most_followed_followers"),
    path('most_followed_following/', views.most_followed_following, name="most_followed_following"),
    path('todos_mis_datos/', views.todosMisDatos, name="todos_mis_datos"),
    path('full_profile/', views.fullProfile, name="full_profile"),

    path('commenTimeline', views.commenTimeline, name="commenTimeline"),
    path('commentHashtag', views.commentHashtag, name="commentHashtag"),
    path('likeHashtag', views.likeHashtag, name="likeHashtag"),
    path('likeTimeline', views.likeTimeline, name="likeTimeline"),
    path('followHashtag', views.followHashtag, name="followHashtag"),
    

]