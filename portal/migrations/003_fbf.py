# Create a new migration file in your portal/migrations/ directory
# Name it something like 0002_add_farmerbiodata_foreignkey.py

from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_add_farmerbiodata_foreignkey'),  # Replace with your last migration
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiarydetails',
            name='farmerbiodata',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='portal.farmerbiodata'
            ),
        ),
    ]
    