import uvicorn


if __name__ == "__main__":
    server_config = uvicorn.Config("src.core.app:app", port=8000)
    server = uvicorn.Server(server_config)
    server.run()
