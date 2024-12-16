from flask import request
from werkzeug.exceptions import HTTPException
from .permission_exceptions import PermissionDenied


def register_resources_exception_handler(api):
    @api.errorhandler(PermissionDenied)
    def handle_permission_denied(e: PermissionDenied):
        request.logger.error(getattr(e, "description", str(e)))
        return {"code": 403, "message": getattr(e, "description", str(e))}, 403
    @api.errorhandler(HTTPException)
    def handle_default_http_exception(e: HTTPException):
         return {
            "code": e.code,
            "message": getattr(e, "description", str(e)),
        }