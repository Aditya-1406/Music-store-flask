from flask.views import MethodView
from flask import render_template, request, redirect, url_for, flash
from app.extensions import db
from db import Album, Song,OrderItem
from app.utils import save_cover_image,login_required, admin_required
from sqlalchemy import or_

class AlbumCreateView(MethodView):

    @admin_required
    def get(self):
        return render_template("create_album.html")

    def post(self):
        title = request.form.get("title")
        artist = request.form.get("artist")
        cover = request.files.get("cover")
        songs = request.form.getlist("songs[]")
        copies = request.form.get("copies")
        amount = request.form.get("amount")

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
            copies = copies,
            amount = amount
        )

        db.session.add(album)
        db.session.commit()

        for name in songs:
            if name.strip():
                db.session.add(Song(title=name, album_id=album.id))

        db.session.commit()

        flash("Album created successfully!")
        return redirect(url_for("list_albums"))
    

class StoreView(MethodView):
    @login_required
    def get(self):
        albums = Album.query.order_by(Album.id.desc()).limit(4).all()
        return render_template("store.html", albums=albums)
    
class AlbumDetailView(MethodView):
    @login_required
    def get(self, album_id):
        album = Album.query.get_or_404(album_id)
        return render_template("album_detail.html", album=album)
    
class ListAlbumAdView(MethodView):
    @admin_required
    def get(self):
       
        page = request.args.get("page", 1, type=int)
        search = request.args.get("search", "")

        query = Album.query

        if search:
            query = query.filter(
                or_(
                    Album.title.ilike(f"%{search}%"),
                    Album.artist.ilike(f"%{search}%")
                )
            )

        albums = query.order_by(Album.id.desc()).paginate(
            page=page,
            per_page=1,
            error_out=False
        )

        return render_template("list_albumad.html", albums=albums, search=search)
    
class UpdateAlbum(MethodView):
    @admin_required
    def get(self,album_id):
        album = Album.query.get_or_404(album_id)
        return render_template("update_album.html",album=album)
    
    @admin_required
    def post(self,album_id):
        album = Album.query.get_or_404(album_id)
        album.title = request.form.get("title")
        album.artist = request.form.get("artist")
        album.copies = request.form.get("copies")
        album.amount = request.form.get("amount")

        
        cover = request.files.get("cover")
        if cover and cover.filename != "":
            filename = save_cover_image(cover)
            if filename:
                album.cover_image = filename

        db.session.commit()
        flash("Album updated successfully!")
        return redirect(url_for("list_albums"))
    
class DeleteAlbumView(MethodView):
    @admin_required
    def post(self,album_id):
        album = Album.query.get_or_404(album_id)
        existing_order = OrderItem.query.filter_by(album_id=album_id).first()
        if existing_order:
            flash("❌ Cannot delete album. It has been ordered by users.", "danger")
            return redirect(url_for("dashboard")) 
        db.session.delete(album)
        db.session.commit()
        flash("Album Deleted successfully!")
        return redirect(url_for("list_albums"))


class HomeView(MethodView):
    @login_required
    def get(self):
        page = request.args.get("page", 1, type=int)
        search = request.args.get("search", "")

        query = Album.query

        if search:
            query = query.filter(
                or_(
                    Album.title.ilike(f"%{search}%"),
                    Album.artist.ilike(f"%{search}%")
                )
            )

        albums = query.order_by(Album.id.desc()).paginate(
            page=page,
            per_page=1,
            error_out=False
        )

        return render_template("home.html", albums=albums, search=search)