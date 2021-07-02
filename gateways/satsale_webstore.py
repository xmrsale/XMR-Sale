from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, emit
import time
import os
import csv

def load_items(file="static/store.csv"):
    items = []
    with open(file) as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            items.append(row)
    return items

def save_items(items, file="static/store.csv"):
    with open(file, 'w') as csvfile:
        spamwriter = csv.writer(csvfile)
        for item in items:
            try:
                spamwriter.writerow(item)
            except Exception as e:
                print(e)
                continue
    return

def add_webstore_decorators(app, file="static/store.csv"):
    if not os.path.exists(file):
        app.items = [["Roosters", 5, "https://img.jakpost.net/c/2020/08/18/2020_08_18_102621_1597723826._large.jpg"], ['Apples', 2, None], ['Pizza', 5, None]]
        save_items(app.items, file)
    else:
        app.items = load_items(file)

    @app.route("/store")
    def store():
        # Render store page
        return render_template("store.html", params=app.items)

    @app.route("/admin")
    def admin():
        # Render store admin page
        return render_template("admin.html", params=app.items)

    @app.route("/additem", methods = ['GET', 'POST'])
    def add_item():
        params = dict(request.args)
        print(params)
        app.items.append([params['itemName'], params['itemPrice'], params['itemURL']])
        save_items(app.items)
        return "success"

    @app.route('/uploader', methods = ['GET', 'POST'])
    def upload_file(file="static/store.csv"):
       if request.method == 'POST':
          f = request.files['file']
          f.save(file)
          app.items = load_items()
          return render_template("store.html", params=app.items)
          return "success"


    return app
