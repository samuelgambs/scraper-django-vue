from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Cursos
from .serializer import CursosSerializer
from django.db.models import Avg, Max, Min, Sum
from django.db.models import Subquery
import json


estados = {
    "sul": ("PR", "RS", "SC"),
    "sudeste": ("SP", "RJ", "ES", "MG"),
    "centro-oeste": ("MT", "MS", "GO"),
    "norte": ("AM", "RR", "AP", "PA", "TO", "RO", "AC"),
    "nordeste": ("MA", "PI", "CE", "RN", "PE","PB", "SE", "AL", "BA")
}

@api_view(['GET'])
def cursos_list(request):
    """
    List  cursos, or create a new curso.
    """
    data = []
    nextPage = 1
    previousPage = 1
    cursos = Cursos.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(cursos, 10)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    serializer = CursosSerializer(data,context={'request': request},many=True)
    if data.has_next():
        nextPage = data.next_page_number()
    if data.has_previous():
        previousPage = data.previous_page_number()

    return Response({'data': serializer.data , 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': '/api/products/?page=' + str(nextPage), 'prevlink': '/api/products/?page=' + str(previousPage)})


@api_view(['GET'])
def curso_detail(request, pk):
    """
    Retrieve, update or delete a product instance.
    """
    try:
        curso = Cursos.objects.get(pk=pk)
    except Cursos.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CursosSerializer(curso,context={'request': request})
        return Response(serializer.data)

@api_view(['GET'])
def mensalidade_top5(request):
    try:
        cursos = Cursos.objects.values('curso').distinct()
        print(list(cursos))
        estados = Cursos.objects.order_by().values('uf').distinct()
        print(list(estados))

        top = Cursos.objects.annotate(Max('mensalidade')).order_by('-mensalidade')[:5]
    except Cursos.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CursosSerializer(top, context={'request': request})
        return Response(serializer.data)

@api_view(['GET'])
def maior_mensalidade_uf(request, uf):
    try:
        uf = uf.upper()
        cursos = Cursos.objects.all().filter(uf=uf).annotate(Max('mensalidade')).order_by('-mensalidade')[:5]

    except Cursos.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CursosSerializer(cursos, context={'request': request}, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def menor_mensalidade_uf(request, uf):
    try:
        cursos = Cursos.objects.all()
        uf = uf.upper()
        cursos = Cursos.objects.filter(uf=uf).annotate(Min('mensalidade')).order_by('mensalidade')[:5]

    except Cursos.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CursosSerializer(cursos, context={'request': request}, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def menor_mensalidade_regiao(request, regiao):
    try:
        cursos = []
        for estado in estados[regiao]:
            cursos.extend(list(Cursos.objects.filter(uf=estado)))
            
        cursos.annotate(Min('mensalidade')).order_by('mensalidade')

    except Cursos.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CursosSerializer(cursos, context={'request': request}, many=True)
        return Response(serializer.data)
