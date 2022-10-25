from app import app, db

@app.shell_context_processor
def make_shell_context():
    import app.models
    return {k:getattr(app.models, k) for k in dir(app.models)}

    # import app.models
    # return {k:getattr(app.models, k) for k in dir(app.models)}


