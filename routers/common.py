from typing import ClassVar, Type

from django.db.models import Model


class DatabaseRouter:
    db: str = ""
    route_app_labels: ClassVar[set] = set()

    def db_for_read(self, model: Type[Model], **hints):
        if model._meta.app_label in self.route_app_labels:
            return self.db
        return None

    def db_for_write(self, model: Type[Model], **hints):
        if model._meta.app_label in self.route_app_labels:
            return self.db
        return None

    def allow_relation(self, obj1: Model, obj2: Model, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(
        self, db: str, app_label: str, model_name: str | None = None, **hints
    ):
        """
        Make sure the auth and contenttypes apps only appear in the
        'auth_db' database.
        """
        if app_label in self.route_app_labels:
            return db == self.db
        return None
