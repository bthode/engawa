# Start the app
uv run uvicorn app.main:app --port 8000 --reload

# Debug the app
uv run python -Xfrozen_modules=off -m debugpy --listen 5678 -m uvicorn app.main:app --reload

# Debug the app, halt until debugger is attached
uv run python -Xfrozen_modules=off -m debugpy --listen 5678 --wait-for-client -m uvicorn app.main:app --reload

See the launch.json in this same folder