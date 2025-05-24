from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0002_create_superuser'),
        ('accounts', '0006_alter_profile_profile_picture'),
    ]

    operations = [
        # No operations needed, just merging the migrations
    ] 