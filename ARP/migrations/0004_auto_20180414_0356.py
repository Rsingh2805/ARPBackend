# Generated by Django 2.0.1 on 2018-04-14 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ARP', '0003_infection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arpuser',
            name='machine_status',
            field=models.CharField(choices=[('INF', 'Infected'), ('SAF', 'Safe')], default='SAF', max_length=3, verbose_name='PC Status'),
        ),
        migrations.AlterField(
            model_name='infection',
            name='victim_employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='infections', to='ARP.ARPUser', verbose_name='Victim'),
        ),
    ]
