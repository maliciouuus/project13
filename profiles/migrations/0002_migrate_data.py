from django.db import migrations


def migrate_profiles(apps, schema_editor):
    # Get old and new model classes
    OldProfile = apps.get_model("oc_lettings_site", "Profile")
    NewProfile = apps.get_model("profiles", "Profile")

    # Migrate profiles
    for old_profile in OldProfile.objects.all():
        new_profile = NewProfile(
            id=old_profile.id,
            user=old_profile.user,
            favorite_city=old_profile.favorite_city,
        )
        new_profile.save()


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0001_initial"),
        ("oc_lettings_site", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(migrate_profiles),
    ]
