from .common import DatabaseRouter


class RestRouter(DatabaseRouter):
    db = "rest_db"
    route_app_labels = {"airport", "city", "flight", "booking", "user"}
