from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app import libs, models, schemas, services
from app.core import logger, settings

router = APIRouter()


async def ws_send(obj_to_send: dict, websocket: WebSocket):
    logger.info(obj_to_send)
    await websocket.send_json(obj_to_send)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()

            command = data.get("command")
            params = data.get("params", [])

            logger.info(f"Received command: {command} with params: {params}")

            if command == "sync":
                settings.disable_ftp = True

                await ws_send(
                    {"command": "sync", "status": "start_refreshing_songs"}, websocket
                )

                libraries = [
                    schemas.Library(**library) for library in models.Library.all()
                ]
                processed_songs = [
                    p.source_file for p in models.Song.get_processed_songs()
                ]

                for library in libraries:
                    songs = list(
                        set(libs.file.get_song_files(library)) - set(processed_songs)
                    )

                    services.audio.process_songs(library, songs)

                if not settings.disable_ftp:
                    services.audio.upload_albums(models.Album.get_unuploaded_albums())

                await ws_send({"command": "sync", "status": "success"}, websocket)
    except WebSocketDisconnect:
        pass
