from app.api.api_v1.artists import router as artists_router
from app.api.api_v1.libraries import router as libraries_router
from app.api.api_v1.songs import router as songs_router
from app.api.api_v1.stats import router as stats_router
from app.api.ws.commands import router as ws_commands_router

__all__ = [
    "libraries_router",
    "songs_router",
    "stats_router",
    "ws_commands_router",
    "artists_router",
]
