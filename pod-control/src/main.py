import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        port=5000,
        log_level="info",
        access_log=True,
        use_colors=True,
        reload=True,
    )
