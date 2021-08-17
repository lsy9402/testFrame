if __name__ == '__main__':
    from uvicorn import run

    run("main:app", port=8001, debug=True, reload_dirs=[
        "app/api",
        "app/core",
        "app/db",
        "app/schemas",
        "app/testTools",
        "app/utils",
    ])
