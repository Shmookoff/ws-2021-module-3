### Custom renderer

```py
class ResponseRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context = None):
        response: Response = renderer_context["response"]

        #do smth with data

        return super().render(data, accepted_media_type, renderer_context)
```

```py
REST_FRAMEWORK = {
    ...
    "DEFAULT_RENDERER_CLASSES": ("module.ResponseRenderer",),
}
```
