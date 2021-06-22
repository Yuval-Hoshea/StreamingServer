import sys
from client import Client
from videoplayer import VideoPlayer
from dialogs import VideoDialog
from gui import Window, AskingForFrameThread
from ClientConfig import SERVER_IP, SERVER_PORT
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget


def make_client():
    video_player = VideoPlayer()
    client = Client(SERVER_IP, SERVER_PORT, video_player)
    client.threaded_connect_and_listen_to_server()

    return client, video_player


def make_window(client: Client, video_player: VideoPlayer, videos_dialog: VideoDialog)->Window:
    vid_name = videos_dialog.video_name()
    client.ask_for_video_details(vid_name)
    client.ask_for_new_location(vid_name, 0)

    video_player.wait_for_video_details()
    asking_frames_thread = AskingForFrameThread(client, video_player, vid_name)
    asking_frames_thread.start()

    win = Window(client, video_player, vid_name, asking_frames_thread)
    return win, asking_frames_thread


def main():
    app = QApplication(sys.argv)
    # create clients and get available videos
    try:
        client, video_player = make_client()
        videos = client.ask_for_all_videos_available()
    except ConnectionRefusedError:
        # if there is not connection with the server (For example, the server is not running).
        QMessageBox.about(QWidget(), "ERROR", "There is no server available.")
        return

    # choose videos dialog
    videos_dialog = VideoDialog(videos)

    while True:
        win, thread = make_window(client, video_player, videos_dialog)
        win.show()

        app.exec_()

        videos_dialog = VideoDialog(videos)
        thread.kill()
        video_player.empty(0)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
