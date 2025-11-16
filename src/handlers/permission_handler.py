from .base_handler import BaseHandler

from src.service import PermissionService


class PermissionHandler(BaseHandler):
    def __init__(self, service: PermissionService):
        super().__init__(service)
