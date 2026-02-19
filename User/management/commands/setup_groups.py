from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Create Operator, SuperUser, and Admin groups with permissions'

    def handle(self, *args, **kwargs):
        # Create Admin group
        admin_group, created = Group.objects.get_or_create(name='Admin')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Admin group'))
        
        # Admin gets all permissions
        admin_group.permissions.set(Permission.objects.all())
        
        # Create SuperUser group
        superuser_group, created = Group.objects.get_or_create(name='SuperUser')
        if created:
            self.stdout.write(self.style.SUCCESS('Created SuperUser group'))
        
        # SuperUser gets all permissions (same as Admin but no Django admin access)
        superuser_group.permissions.set(Permission.objects.all())
        
        # Create Operator group
        operator_group, created = Group.objects.get_or_create(name='Operator')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Operator group'))
        
        # Operator gets all permissions except user management
        operator_permissions = Permission.objects.exclude(
            content_type__app_label='auth',
            content_type__model='user'
        ).exclude(
            content_type__app_label='auth',
            content_type__model='group'
        )
        operator_group.permissions.set(operator_permissions)
        
        self.stdout.write(self.style.SUCCESS('Successfully configured groups'))
