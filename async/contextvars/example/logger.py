from .context import request_id

def log(msg: str):
    rid = request_id.get()
    print(f"[req={rid}] {msg}")
