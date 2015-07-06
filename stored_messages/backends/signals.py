from django.dispatch import Signal

inbox_stored = Signal(providing_args=["user", "message"])
inbox_deleted = Signal(providing_args=["user", "message_id"])
inbox_purged = Signal(providing_args=["user"])

archive_stored = Signal(providing_args=["user", "message"])
