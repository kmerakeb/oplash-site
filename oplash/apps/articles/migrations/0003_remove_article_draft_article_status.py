# Generated by Django 4.0.4 on 2022-06-23 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_article_draft_article_next_article_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='draft',
        ),
        migrations.AddField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[('D', 'Draft'), ('P', 'Published')], default='D', max_length=1),
        ),
    ]
