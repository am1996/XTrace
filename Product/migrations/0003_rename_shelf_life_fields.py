from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0002_product_equipment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='shelf_life_days',
            new_name='shelf_life',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='unit',
            new_name='shelf_life_unit',
        ),
    ]
