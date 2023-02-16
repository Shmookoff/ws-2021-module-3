from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class ResponseRenderer(JSONRenderer):
    def render(
        self, data, accepted_media_type=None, renderer_context: dict | None = None
    ):
        response: Response = renderer_context["response"]
        if str(response.status_code).startswith("2"):
            processed_data = {"data": data} if data else None
        else:
            processed_data = {
                "error": {
                    "code": response.status_code,
                    "message": response.status_text,
                }
            }
            if detail := data.get("detail"):
                processed_data["error"]["message"] = detail
            else:
                processed_data["error"]["errors"] = data
        return super().render(processed_data, accepted_media_type, renderer_context)
