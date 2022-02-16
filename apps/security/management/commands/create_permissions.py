from django.contrib.contenttypes.models import ContentType # NOQA
from django.contrib.auth.models import Permission # NOQA
from django.core.management.base import BaseCommand

from utils.permissions import data_content_types, all_permissions


class Command(BaseCommand):
    help = "Command for CREATE permissions based in utils.permissions file"

    def add_arguments(self, parser):
        parser.add_argument(
            "-r",
            "--reset",
            type=str,
            help=(
                "Define if want reset (Y) or (N) just update and create "
                "if has new content types and permission. Default N"
            )
        )

    def handle(self, *args, **kwargs):
        def _creating_content_types():
            for content_type in data_content_types:
                if not ContentType.objects.filter(
                    app_label=content_type.get('app_label'),
                    model=content_type.get('model')
                ).exists():
                    ContentType.objects.create(
                        app_label=content_type.get('app_label'),
                        model=content_type.get('model')
                    )

        def _creating_permissions():
            counter = 0
            for permission in all_permissions:
                content = ContentType.objects.filter(
                    app_label=permission.get('content_type_name')
                ).first()
                if content is None:
                    msg = (
                        f'Permission with name: {permission.get("name")} '
                        'doesnt have content type asociated correctly'
                    )
                    print(msg)
                else:
                    if not Permission.objects.filter(
                        name=permission.get('name'),
                        content_type=content.pk,
                        codename=permission.get('codename')
                    ).exists():
                        Permission.objects.create(
                            name=permission.get('name'),
                            content_type=content,
                            codename=permission.get('codename')
                        )
                        counter = counter + 1
                        msg = (
                            f'Permission: {permission.get("name")}... '
                            f'With Content Type {permission.get("content_type_name")}...'
                            f'created!!'
                        )
                        print(msg)

            print(f'Number of permissions created: {counter}')

        reset = kwargs.get("reset") or 'N'
        if reset == 'S':
            try:
                ContentType.objects.filter().delete()
                Permission.objects.filter().delete()
                print("Reseted Content Types and Permissions!!")
            except Exception as e:
                print(
                    f"Problem white reseting content type and permission msj:{e.__str__()}"
                )
        _creating_content_types()
        _creating_permissions()
        self.stdout.write(self.style.SUCCESS("Command execution ended Successfully!!"))
