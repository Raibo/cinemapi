# Generated by Django 2.1.5 on 2019-02-11 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='hall',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sessions', to='cinema.Hall'),
        ),
        migrations.AlterField(
            model_name='session',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sessions', to='cinema.Movie'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tickets', to='cinema.Session'),
        ),
    ]