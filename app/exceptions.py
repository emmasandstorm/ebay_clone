import werkzeug
from app import myobj
from flask import flash, redirect


@myobj.errorhandler(werkzeug.exceptions.RequestEntityTooLarge)
def request_entity_too_large(error):
    flash("File too large to upload, please select a smaller file.")
    return redirect("/newlisting")
