"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url
from main import views


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/cursos/$', views.cursos_list),
    url(r'^api/cursos/(?P<pk>[0-9]+)$', views.curso_detail),
    url(r'^api/cursos/mensalidade/top5/$', views.mensalidade_top5),
    #url(r'^api/cursos/maior-mensalidade/curso/$', views.maior_mensalidade_curso),
    #url(r'^api/cursos/maior-mensalidade/regiao/$', views.maior_mensalidade_regiao),
    url(r'^api/cursos/maior-mensalidade/uf/(?P<uf>[\w\-]+)/$', views.maior_mensalidade_uf),
    #url(r'^api/cursos/menor-mensalidade/curso/$', views.menor_mensalidade_curso),
    #url(r'^api/cursos/menor-mensalidade/regiao/$', views.menor_mensalidade_regiao),
    #url(r'^api/cursos/menor-mensalidade/uf/$', views.menor_mensalidade_uf),
    #url(r'^api/cursos/maior_mensalidade/regiao/$', views.mensalidade_top5),
    #url(r'^api/cursos/top5/max/nota-integral-ampla/regiao/$', views.mensalidade_top5),
    #url(r'^api/cursos/top5/min/nota-integral-ampla/regiao/$', views.mensalidade_top5),
    #url(r'^api/cursos/top5/media/nota-integral-ampla/regiao/$', views.mensalidade_top5),





]
