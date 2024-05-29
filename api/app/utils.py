def build_path(host: str, port: str, token: str) -> str:
    token_prefix = "?X-Plex-Token="
    return f"http://{host}:{port}/library/sections{token_prefix}{token}"
