import os.path
import sys
from typing import Dict
import cv2
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
import image_functions


IMAGES_IN_LINE = 3
TITLE_IMAGE = "title.jpg"


def get_title_qimage() -> QImage:
    # get the path of the title image
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, TITLE_IMAGE)
    # get the image and convert to QImage
    img_arr = cv2.imread(image_path)
    q_img = image_functions.convert_numpy_array_to_qimage(img_arr)
    return q_img


class VideoDialog(QDialog):
    def __init__(self, videos: Dict[str, str]):
        """
        :param videos: list of string. List of all the videos.
        """
        super(VideoDialog, self).__init__()
        self.setGeometry(0, 0, 500, 500)
        self.__video_name = ""
        self.layout = QVBoxLayout(self)
        # Title image
        title_image = QLabel()
        title_image.setPixmap(QPixmap(get_title_qimage()))
        self.layout.addWidget(title_image)

        last_row_layout = None
        # add videos buttons to the dialog
        for (index, video) in enumerate(videos.keys()):
            img_arr = image_functions.resize_image_to_specific_height(videos[video], wanted_height=250)
            q_img = image_functions.convert_numpy_array_to_qimage(img_arr)
            image = ImageButton(self, video, q_img)

            row, col = index // IMAGES_IN_LINE + 1, index % IMAGES_IN_LINE
            if col == 0:
                # create new row
                row_layout = QHBoxLayout()
                self.layout.addLayout(row_layout)
                last_row_layout = row_layout
            else:
                row_layout = last_row_layout

            row_layout.addWidget(image)

        for _ in range(0, IMAGES_IN_LINE - last_row_layout.count()):
            last_row_layout.addWidget(QLabel())

        self.style()
        self.show()

        if self.exec_() == QDialog.Rejected:
            sys.exit()

    def video_name(self):
        return self.__video_name

    def set_selected_video(self, video_name: str):
        self.__video_name = video_name

    def style(self):
        style = """
                QDialog{
                    background-color: white;
                }
                """

        self.setStyleSheet(style)


class ImageButton(QLabel):

    def __init__(self, dialog: VideoDialog, video_name: str, q_image: QImage, *args, **kwargs):
        super(ImageButton, self).__init__(*args, **kwargs)
        self.__dialog = dialog
        self.__video_name = video_name
        pixmap = QPixmap(q_image)
        self.setPixmap(pixmap)
        self.style_image()

    def style_image(self):
        style = """
                QLabel {
                    margin: 10px 10px;
                    padding: 10px 10px;
                }
                QLabel:hover {
                    background-color: rgb(196, 196, 196);
                }
                """

        self.setStyleSheet(style)

    def mousePressEvent(self, ev) -> None:
        """
        When button pressed we close the dialog by accepting it.
        """
        super().mousePressEvent(ev)
        self.__dialog.set_selected_video(self.__video_name)
        self.__dialog.accept()
