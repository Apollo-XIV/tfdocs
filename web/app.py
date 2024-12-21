from flask import Flask, render_template, redirect, send_file
from web.s3 import list_available_releases, get_download_link

app = Flask(__name__)


@app.route('/')
def home():
    """Serve the home page."""
    available_releases = list_available_releases()[:5]
    return render_template("index.html", releases=available_releases)


@app.route("/install")
def install():
    """Redirect to the install.sh script"""
    return send_file("static/install.sh", mimetype='text/x-shellscript')


@app.route('/releases')
def releases():
    """Serve a page listing all available releases"""
    available_releases = list_available_releases()
    return render_template("releases.html", releases=available_releases)


@app.route('/releases/latest')
def release_latest():
    """Redirect to the latest version of the app"""
    latest_release = list_available_releases()[0]
    return render_template("releases.html", version=latest_release)


@app.route('/releases/latest/download')
def download_latest():
    """Redirect to the latest version of the app"""
    latest_release = list_available_releases()[0]
    return redirect(get_download_link(latest_release))


@app.route('/releases/<version_number>')
def release(version_number):
    return render_template("release.html", version=version_number)


@app.route('/releases/<version_number>/download')
def release_download(version_number):
    return redirect(get_download_link(version_number))
