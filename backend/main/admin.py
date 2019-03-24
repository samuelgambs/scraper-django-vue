# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from main.models import Cursos

from django.contrib import admin


class CursosAdmin(admin.ModelAdmin):

    list_display = ['uf', 'cidade', 'universidade', 'nome_campus',
                    'curso', 'grau', 'turno', 'mensalidade',
                    'bolsas_integrais_cota',
                    'bolsas_integrais_ampla', 'bolsas_parciais_cota',
                    'bolsas_parciais_ampla', 'nota_integral_ampla',
                    'nota_integral_cota', 'nota_parcial_ampla',
                    'nota_parcial_cota']

    list_filter = ['uf', 'cidade', 'universidade', 'nome_campus', 'curso']

admin.site.register(Cursos, CursosAdmin)
