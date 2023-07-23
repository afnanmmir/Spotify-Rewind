import os
from dotenv import load_dotenv
from flask import Flask, redirect, url_for, render_template,request,session,flash
from flask_session import Session
import spotipy
import uuid
def create_app():
    app = Flask(__name__)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = './.flask_session/'
    Session(app)

    load_dotenv()
    SPOTIFY_CLIENT_ID = os.getenv("CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.getenv("CLIENT_SECRET")

    caches_folder = './.spotify_caches/'
    if not os.path.exists(caches_folder):
        os.makedirs(caches_folder)
    def session_cache_path():
        return caches_folder + session.get('uuid')

    def WeightedAverage(artists):
        added = 0
        weights = 0
        n = len(artists)
        for (i,x) in enumerate(artists):
            added += (2.5*n-i)*(x['popularity'])
            weights += (2.5*n-i)
        return round(added/weights)

    @app.route("/")
    def home():
        #uuid is given when a new visitor enters the website. If a visitor has already been to the website, they will already have a uuid
        if(not session.get('uuid')):
            session['uuid'] = str(uuid.uuid4())
        authenticate_manager = spotipy.oauth2.SpotifyOAuth(client_id = SPOTIFY_CLIENT_ID,client_secret = SPOTIFY_CLIENT_SECRET,redirect_uri = 'https://spotify-rewind-cxzlw32vta-uc.a.run.app',scope = 'user-top-read',cache_path = session_cache_path(),show_dialog = True)
        #This will handle the logging in part. Then it will run the function again and take them to the next page
        if(request.args.get('code')):
            authenticate_manager.get_access_token(request.args.get('code'))
            return redirect("/")
        #If the user has not logged in before yet, then take them to the home page
        if(not authenticate_manager.get_cached_token()):
            a_url = authenticate_manager.get_authorize_url()
            return render_template("home.html",a_url = a_url)
        return redirect("/shortterm")
    @app.route("/shortterm")
    def short_term():    
        if(session.get('uuid') is None):
            return redirect("/")
        auth_manage = spotipy.oauth2.SpotifyOAuth(client_id = SPOTIFY_CLIENT_ID,client_secret = SPOTIFY_CLIENT_SECRET,redirect_uri = 'https://spotify-rewind-cxzlw32vta-uc.a.run.app',scope = 'user-top-read',cache_path = session_cache_path(),show_dialog = True)
        if(not auth_manage.get_cached_token()):
            return redirect("/")
        spotify = spotipy.Spotify(auth_manager=auth_manage)
        results = spotify.current_user_top_artists(15,0,"short_term")
        songs = spotify.current_user_top_tracks(15,0,"short_term")
        weighted = WeightedAverage(results['items'])
        songavg = WeightedAverage(songs['items'])
        return render_template("test.html", results = results['items'],songs = songs['items'],avg = weighted,songavg = songavg, timeFrame = "4 weeks")
    @app.route("/mediumterm")
    def medium_term():    
        if(session.get('uuid') is None):
            return redirect("/")
        auth_manage = spotipy.oauth2.SpotifyOAuth(client_id = SPOTIFY_CLIENT_ID,client_secret = SPOTIFY_CLIENT_SECRET,redirect_uri = 'https://spotify-rewind-cxzlw32vta-uc.a.run.app',scope = 'user-top-read',cache_path = session_cache_path(),show_dialog = True)
        if(not auth_manage.get_cached_token()):
            return redirect("/")
        spotify = spotipy.Spotify(auth_manager=auth_manage)
        results = spotify.current_user_top_artists(15,0,"medium_term")
        songs = spotify.current_user_top_tracks(15,0,"medium_term")
        weighted = WeightedAverage(results['items'])
        songavg = WeightedAverage(songs['items'])
        return render_template("test.html", results = results['items'],songs = songs['items'],avg = weighted,songavg = songavg, timeFrame = "6 months")
    @app.route("/longterm")
    def long_term():    
        if(session.get('uuid') is None):
            return redirect("/")
        auth_manage = spotipy.oauth2.SpotifyOAuth(client_id = SPOTIFY_CLIENT_ID,client_secret = SPOTIFY_CLIENT_SECRET,redirect_uri = 'https://spotify-rewind-cxzlw32vta-uc.a.run.app',scope = 'user-top-read',cache_path = session_cache_path(),show_dialog = True)
        if(not auth_manage.get_cached_token()):
            return redirect("/")
        spotify = spotipy.Spotify(auth_manager=auth_manage)
        results = spotify.current_user_top_artists(15,0,"long_term")
        songs = spotify.current_user_top_tracks(15,0,"long_term")
        weighted = WeightedAverage(results['items'])
        songavg = WeightedAverage(songs['items'])
        return render_template("test.html", results = results['items'],songs = songs['items'],avg = weighted,songavg = songavg, timeFrame = "All time")
    @app.route("/index")
    def test():
        auth_manage = spotipy.oauth2.SpotifyOAuth(client_id = SPOTIFY_CLIENT_ID,client_secret = SPOTIFY_CLIENT_SECRET,redirect_uri = 'https://spotify-rewind-cxzlw32vta-uc.a.run.app',scope = 'user-top-read',cache_path = session_cache_path(),show_dialog = True)
        if(not auth_manage.get_cached_token()):
            return redirect("/")
        spotify = spotipy.Spotify(auth_manager=auth_manage)
        results = spotify.current_user_top_artists(15,0,"medium_term")
        songs = spotify.current_user_top_tracks(15,0,"medium_term")
        weighted = WeightedAverage(results['items'])
        songavg = WeightedAverage(songs['items'])
        return render_template("test.html", results = results['items'],songs = songs['items'],avg = weighted,songavg = songavg)
    @app.route("/logout")
    def logout():
        try:
            # Remove the CACHE file (.cache-test) so that a new user can authorize.
            os.remove(session_cache_path())
            session.clear()
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
        return redirect('/')
    return app
