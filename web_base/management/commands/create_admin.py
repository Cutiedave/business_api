from base.models import MyUser
from django.core.management.base import BaseCommand
class Command(BaseCommand):

    def handle(self, *args, **options):
        if not MyUser.objects.filter(email='admin@gmail.com').first():
            
            username = 'admin'
            email = 'admin@gmail.com'
            password = 'admin'
            print('Creating account for %s (%s)' % (username, email))
            admin = MyUser.objects.create_superuser(email=email,full_name='me', password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')