from rest_framework import serializers
from django.contrib.auth import get_user_model

from BusTracker import models

User = get_user_model()

class BulkUserUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def create_users_from_csv(self, csv_file):
        import csv, io
        decoded_file = csv_file.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(decoded_file))

        users = []
        errors = []

        for row in reader:
            try:
                user = User(
                    username=row['username'],
                    email=row['email'],
                )
                user.set_password(row['password'])  # Proper hashing
                user.save()
                models.Bus.objects.get(license_number=row['license_number']).staff.add(user)
                users.append(user)
            except Exception as e:
                errors.append({"row": row, "error": str(e)})

        return users, errors
