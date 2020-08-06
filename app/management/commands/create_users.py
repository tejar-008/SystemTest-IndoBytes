from django.core.management.base import BaseCommand
from app.models import User


class Command(BaseCommand):
    '''
        It will create Default Roles
    '''

    def handle(self, *args, **options):
        try:
            user = User.objects.create(username=admin, email="admin@gmail.com", is_superuser=True)
            user.set_password("qwerty@12")
            user.save()
        except:
            pass
        for num in range(1, 5):
            username = "user" + str(num)
            try:
                user = User.objects.create(username=username, email=username + "@gmail.com")
                user.set_password("qwerty@12")
                user.save()
            except:
                pass
        print("Users Created Successfully.")
