# Generated by Django 3.2 on 2022-05-04 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmwork',
            name='type',
            field=models.TextField(choices=[('movie', 'Movie'), ('tw_show', 'Tw Show')], verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='personfilmwork',
            name='role',
            field=models.TextField(choices=[('actor', 'Actor'), ('director', 'Director'), ('writer', 'Writer')], null=True, verbose_name='role'),
        ),
        migrations.AlterUniqueTogether(
            name='genrefilmwork',
            unique_together={('film_work', 'genre')},
        ),
        migrations.AlterUniqueTogether(
            name='personfilmwork',
            unique_together={('film_work', 'person', 'role')},
        ),
        migrations.AlterIndexTogether(
            name='filmwork',
            index_together={('creation_date', 'rating')},
        ),
        migrations.AlterIndexTogether(
            name='genrefilmwork',
            index_together={('film_work', 'genre')},
        ),
        migrations.AlterIndexTogether(
            name='personfilmwork',
            index_together={('film_work', 'person', 'role')},
        ),
    ]