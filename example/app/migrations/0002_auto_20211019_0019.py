# Generated by Django 3.2.8 on 2021-10-18 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testmodel',
            name='f_field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='app.foreignmodel', verbose_name='Привет'),
        ),
        migrations.CreateModel(
            name='F2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foreign_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.foreignmodel')),
            ],
        ),
    ]
