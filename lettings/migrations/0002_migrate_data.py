from django.db import migrations


# MODIFICATION: Ce script de migration a été créé pour transférer les données
# des modèles originaux dans oc_lettings_site vers les nouveaux modèles dans
# l'application lettings. Dans le projet original, tous les modèles étaient
# dans l'application oc_lettings_site.
def migrate_addresses_and_lettings(apps, schema_editor):
    # Récupération des classes de modèles anciens et nouveaux
    OldAddress = apps.get_model("oc_lettings_site", "Address")
    NewAddress = apps.get_model("lettings", "Address")
    OldLetting = apps.get_model("oc_lettings_site", "Letting")
    NewLetting = apps.get_model("lettings", "Letting")

    # Migration des addresses - copie toutes les propriétés
    for old_address in OldAddress.objects.all():
        new_address = NewAddress(
            id=old_address.id,  # Conserve le même ID pour maintenir les relations
            number=old_address.number,
            street=old_address.street,
            city=old_address.city,
            state=old_address.state,
            zip_code=old_address.zip_code,
            country_iso_code=old_address.country_iso_code,
        )
        new_address.save()

    # Migration des biens immobiliers - met à jour les relations
    for old_letting in OldLetting.objects.all():
        # Trouve l'adresse correspondante dans le nouveau modèle
        new_address = NewAddress.objects.get(id=old_letting.address.id)
        new_letting = NewLetting(
            id=old_letting.id, title=old_letting.title, address=new_address
        )
        new_letting.save()


class Migration(migrations.Migration):
    # MODIFICATION: Cette migration dépend à la fois de la création des
    # nouveaux modèles et de l'existence des anciens modèles
    dependencies = [
        ("lettings", "0001_initial"),  # Les nouveaux modèles doivent exister
        (
            "oc_lettings_site",
            "0001_initial",
        ),  # Les anciens modèles contenant les données
    ]

    operations = [
        # Exécution de la fonction Python pour migrer les données
        migrations.RunPython(migrate_addresses_and_lettings),
    ]
