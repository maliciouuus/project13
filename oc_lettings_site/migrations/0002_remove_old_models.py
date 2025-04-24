from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("oc_lettings_site", "0001_initial"),
        ("lettings", "0002_migrate_data"),
        ("profiles", "0002_migrate_data"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Letting",
        ),
        migrations.DeleteModel(
            name="Address",
        ),
        migrations.DeleteModel(
            name="Profile",
        ),
    ]
