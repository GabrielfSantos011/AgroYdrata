# Generated by Django 4.2.4 on 2023-09-10 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dados',
            fields=[
                ('id_dados', models.AutoField(primary_key=True, serialize=False)),
                ('nitrogenio', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fosforo', models.DecimalField(decimal_places=2, max_digits=5)),
                ('potassio', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ph', models.DecimalField(decimal_places=2, max_digits=5)),
                ('temperatura', models.DecimalField(decimal_places=2, max_digits=5)),
                ('precipitacao', models.DecimalField(decimal_places=2, max_digits=5)),
                ('umidade', models.DecimalField(decimal_places=2, max_digits=5)),
                ('tp_planta', models.TextField(max_length=255)),
            ],
        ),
    ]