# Generated by Django 4.0.6 on 2022-08-10 02:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booktest', '0003_buy_car'),
    ]

    operations = [
        migrations.AddField(
            model_name='buy_car',
            name='p_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='booktest.people'),
        ),
        migrations.AlterField(
            model_name='buy_car',
            name='g_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='booktest.goods'),
        ),
    ]
