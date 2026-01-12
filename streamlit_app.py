import streamlit as st

class Song:
    def __init__(self, title, artist, audio_file):
        self.title = title
        self.artist = artist
        self.audio_file = audio_file
        self.next_song = None

    def __str__(self):
        return f"{self.title} by {self.artist}"

class MusicPlaylist:
    def __init__(self):
        self.head = None
        self.current_song = None
        self.length = 0

    def add_song(self, title, artist, audio_file):
        song = Song(title, artist, audio_file)
        if not self.head:
            self.head = song
            self.current_song = song
        else:
            cur = self.head
            while cur.next_song:
                cur = cur.next_song
            cur.next_song = song
        self.length += 1

    def display(self):
        res = []
        cur = self.head
        i = 1
        while cur:
            marker = "▶️ " if cur == self.current_song else ""
            res.append(f"{marker}{i}. {cur.title} - {cur.artist}")
            cur = cur.next_song
            i += 1
        return res

    def play(self):
        if self.current_song:
            st.audio(self.current_song.audio_file)

    def next(self):
        if self.current_song and self.current_song.next_song:
            self.current_song = self.current_song.next_song

    def prev(self):
        if self.current_song != self.head:
            cur = self.head
            while cur.next_song != self.current_song:
                cur = cur.next_song
            self.current_song = cur

st.title("🎵 Music Playlist")

if "playlist" not in st.session_state:
    st.session_state.playlist = MusicPlaylist()

st.sidebar.header("Add Song")
title = st.sidebar.text_input("Title")
artist = st.sidebar.text_input("Artist")
file = st.sidebar.file_uploader("Upload mp3 / wav", type=["mp3", "wav"])

if st.sidebar.button("Add"):
    if title and artist and file:
        st.session_state.playlist.add_song(title, artist, file)

st.header("Playlist")
for s in st.session_state.playlist.display():
    st.write(s)

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("⏮ Prev"):
        st.session_state.playlist.prev()
        st.session_state.playlist.play()

with c2:
    if st.button("▶ Play"):
        st.session_state.playlist.play()

with c3:
    if st.button("⏭ Next"):
        st.session_state.playlist.next()
        st.session_state.playlist.play()
