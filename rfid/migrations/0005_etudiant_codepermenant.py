# Generated by Django 5.0.4 on 2024-05-21 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rfid', '0004_alter_etudiant_fingerprint_id_alter_etudiant_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='etudiant',
            name='codePermenant',
            field=models.CharField(max_length=50, null=True),
        ),
    ]