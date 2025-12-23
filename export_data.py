import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ak1.settings')
django.setup()

from django.core import serializers
from django.db.models import Model

# Collect all model instances
all_objects = []
for model in django.apps.apps.get_models():
    all_objects.extend(model.objects.all())

# Serialize to JSON
data = serializers.serialize('json', all_objects, indent=2)

# Write without BOM
with open('db_backup_clean.json', 'w', encoding='utf-8') as f:
    f.write(data)

print("Data exported to db_backup_clean.json")
print(f"Total objects exported: {len(all_objects)}")
