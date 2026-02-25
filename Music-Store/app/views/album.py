from flask.views import MethodView
from flask import render_template, request, redirect, url_for, flash
from app.extensions import db
from db import Album, Song
from app.utils import save_cover_image

class AlbumCreateView(MethodView):

    def get(self):
        return render_template("create_album.html")

    def post(self):
        title = request.form.get("title")
        artist = request.form.get("artist")
        cover = request.files.get("cover")
        songs = request.form.getlist("songs[]")
        copies = request.form.get("copies")

        if not cover:
            flash("Cover image required")
            return redirect(url_for("create_album"))

        filename = save_cover_image(cover)

        if not filename:
            flash("Invalid image format")
            return redirect(url_for("create_album"))

        album = Album(
            title=title,
            artist=artist,
            cover_image=filename,
            copies = copies
        )

        db.session.add(album)
        db.session.commit()

        for name in songs:
            if name.strip():
                db.session.add(Song(title=name, album_id=album.id))

        db.session.commit()

        flash("Album created successfully!")
        return redirect(url_for("store"))
    

class StoreView(MethodView):
    def get(self):
        albums = Album.query.all()
        return render_template("store.html", albums=albums)
    
class AlbumDetailView(MethodView):
    def get(self, album_id):
        album = Album.query.get_or_404(album_id)
        return render_template("album_detail.html", album=album)