# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Cursos(models.Model):
    uf = models.CharField(max_length=2)
    cidade = models.CharField(max_length=50)
    universidade = models.CharField(max_length=150)
    nome_campus = models.CharField(max_length=150)
    curso = models.CharField(max_length=150)
    grau = models.CharField(max_length=150)
    turno = models.CharField(max_length=150)
    mensalidade = models.DecimalField(decimal_places=2,max_digits=5)
    bolsas_integrais_cota = models.PositiveSmallIntegerField(null=True, blank=True)
    bolsas_integrais_ampla = models.PositiveSmallIntegerField(null=True, blank=True)
    bolsas_parciais_cota = models.PositiveSmallIntegerField(null=True, blank=True)
    bolsas_parciais_ampla = models.PositiveSmallIntegerField(null=True, blank=True)
    nota_integral_ampla = models.DecimalField(decimal_places=2,max_digits=5,null=True, blank=True)
    nota_integral_cota = models.DecimalField(decimal_places=2,max_digits=5,null=True, blank=True)
    nota_parcial_ampla = models.DecimalField(decimal_places=2,max_digits=5,null=True, blank=True)
    nota_parcial_cota = models.DecimalField(decimal_places=2,max_digits=5,null=True, blank=True)

    class Meta:
        verbose_name = "Cursos e notas de corte do PROUNI 2018" 
