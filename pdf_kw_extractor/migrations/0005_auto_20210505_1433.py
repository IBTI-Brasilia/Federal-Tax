# Generated by Django 3.1.2 on 2021-05-05 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_kw_extractor', '0004_jugdments_ementa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='jugdments',
            name='count',
        ),
        migrations.RemoveField(
            model_name='jugdments',
            name='keyword',
        ),
        migrations.CreateModel(
            name='KeywordCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('keyword', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pdf_kw_extractor.keyword')),
            ],
        ),
        migrations.AddField(
            model_name='keyword',
            name='judgment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pdf_kw_extractor.jugdments'),
        ),
    ]
