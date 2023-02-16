from .common import DatabaseRouter


class CoreRouter(DatabaseRouter):
    db = "core_db"
    route_app_labels = {"auth", "contenttypes", "sessions", "admin"}
