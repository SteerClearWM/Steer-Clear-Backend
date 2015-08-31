from steerclear import app

"""
internal_error
--------------
Error handler for internal server errors.
For some reason this is needed for the logger
to log internal server errors correctly
"""
@app.error_handler(500):
def internal_error(error):
    return
