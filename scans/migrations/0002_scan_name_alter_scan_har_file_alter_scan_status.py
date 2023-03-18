# Generated by Django 4.1.7 on 2023-03-18 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scans', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scan',
            name='name',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='scan',
            name='har_file',
            field=models.FileField(editable=False, upload_to=''),
        ),
        migrations.AlterField(
            model_name='scan',
            name='status',
            field=models.TextField(choices=[('pending', 'Pending'), ('running', 'Running'), ('success', 'Success'), ('error', 'Error')], default='pending', editable=False),
        ),
    ]
