# Generated by Django 4.1.7 on 2023-03-16 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0004_alter_order_price_usd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='price_rub',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='price_usd',
            field=models.IntegerField(null=True),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['number'], name='market_orde_number_e3af38_idx'),
        ),
    ]