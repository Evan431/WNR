"""WNR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from appliWNR.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('pageInscription/', signup, name='pageInscription'),
    path('pageConnexion/', login_user, name='pageConnexion'),
    path('resultatsRecherche/', resultatsRecherche, name='resultatsRecherche'),
    path('statistiques/', statistiques, name='statistiques'),
    path('statistiquesGenerales/', statistiquesGenerales,
         name='statistiquesGenerales'),
    path('programme/', programme, name='programme'),
    path('compte/', compte, name='compte'),
    path('cgu/', cgu, name='cgu'),
    path('deconnexion/', logout_request, name='deconnexion'),
    path('pageSuppresionCompte', deleteAccount, name='suppresionCompte'),
    path('pageConfirmationSuppression', confirmationSuppression,
         name="confirmationSuppression"),
    path('detail_programme/<int:id>/', detail_programme, name='detail_programme'),
    path('note_programme/<int:id>/<int:note>/',
         noteProgramme, name="noteProgramme"),
    path('listProgramme/<int:id>/<str:typeListe>/<str:action>/',
         listProgramme, name="listProgramme"),
    path('liste/<str:typeListe>/',
         liste, name="liste"),
    path('programme/<str:type>/', programme, name="programme"),
    # path('', include('appliWNR.urls'))
]
