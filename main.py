from flask import Flask, render_template, flash, request, redirect
import datetime
import requests

App = Flask(__name__)
App.secret_key = 'Secret Key'

@App.route('/')
def main():
    CurrentYear = datetime.datetime.now().year
    return render_template('index.html',CurrentYear=CurrentYear,flag="False")

@App.route('/sending',methods=["POST"])
def sending():
    CurrentYear = datetime.datetime.now().year
    webhook_url = request.form.get("webhook_url")
    content = request.form.get("content")
    color = request.form.get("color")
    title = request.form.get("title")
    description = request.form.get("description")
    author = request.form.get("author")
    image_url = request.form.get("image_url")
    thumbnail_url = request.form.get("thumbnail_url")
    footer = request.form.get("footer")

    data = {}

    if content != "":
        data["content"] = content

    if description != "":
        data["embeds"] = [{}]
        
        if title != "":
            data["embeds"][0]['title']=title
        if color != "":
            data["embeds"][0]['color']=int(color[1:],16)
        if description != "":
            data["embeds"][0]['description']=description
        if author != "":
            data["embeds"][0]['author']={'name':author}
        if image_url != "":
            data["embeds"][0]['image']={"url":image_url}
        if thumbnail_url != "":
            data["embeds"][0]['thumbnail']={"url":thumbnail_url}
        if footer != "":
            data["embeds"][0]['footer']={"text":footer}

    response = requests.post(webhook_url, json = data)
    try:
        if response.ok:
            flash('success')
            return redirect('/')
        flash('error')
        return redirect('/')
    except Exception: 
        flash('error')
        return redirect('/')