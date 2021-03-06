# Generated by Django 2.1.7 on 2019-03-17 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cursos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uf', models.CharField(max_length=2)),
                ('cidade', models.CharField(max_length=50)),
                ('universidade', models.CharField(max_length=150)),
                ('nome_campus', models.CharField(max_length=150)),
                ('curso', models.CharField(max_length=150)),
                ('grau', models.CharField(max_length=150)),
                ('turno', models.CharField(max_length=150)),
                ('mensalidade', models.DecimalField(decimal_places=2, max_digits=5)),
                ('bolsas_integrais_cota', models.PositiveSmallIntegerField()),
                ('bolsas_integrais_ampla', models.PositiveSmallIntegerField()),
                ('bolsas_parciais_cota', models.PositiveSmallIntegerField()),
                ('bolsas_parciais_ampla', models.PositiveSmallIntegerField()),
                ('nota_integral_ampla', models.DecimalField(decimal_places=2, max_digits=5)),
                ('nota_integral_cota', models.DecimalField(decimal_places=2, max_digits=5)),
                ('nota_parcial_ampla', models.DecimalField(decimal_places=2, max_digits=5)),
                ('nota_parcial_cota', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'verbose_name': 'Cursos e notas de corte do PROUNI 2018',
            },
        ),
    ]
