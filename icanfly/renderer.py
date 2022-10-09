from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        renderer_response: Response = renderer_context["response"]

        if str(renderer_response.status_code).startswith("2"):
            response = {"data": data}
        else:
            response = {
                "error": {
                    "code": renderer_response.status_code,
                    "message": renderer_response.status_text,
                    "errors": data,
                }
            }

        return super().render(response, accepted_media_type, renderer_context)
