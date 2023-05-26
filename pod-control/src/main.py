import uvicorn

DEVELOPMENT = True

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        port=5000,
        log_level="info",
        use_colors=True,
        reload=DEVELOPMENT,
    )
