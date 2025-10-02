import contextvars

# Central definitions
request_id = contextvars.ContextVar("request_id", default="unset")
