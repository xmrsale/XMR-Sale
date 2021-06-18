from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, emit
import time
import os

def add_webstore_decorators(app):
    app.items = [["Roosters", 5, "https://img.jakpost.net/c/2020/08/18/2020_08_18_102621_1597723826._large.jpg"], ['Apples', 2, None], ['Pizza', 5, None]]

    @app.route("/store")
    def store():
        # Render store page
        return render_template("store.html", params=app.items)

    @app.route("/additem")
    def add_item():
        params = dict(request.args)
        app.items.append("Wee")
        print(app.items)
        # Check API key
        return

    return app
