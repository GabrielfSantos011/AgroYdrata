# Generated by Django 4.2.4 on 2023-09-16 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_AgroYdrata', '0005_dados_data_insercao_dados_horario_insercao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dados',
            name='horario_insercao',
        ),
    ]
