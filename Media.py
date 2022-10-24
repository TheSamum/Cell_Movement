from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

from Ploter import ploting
class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.mas = []

        self.a = 0

        self.setWindowTitle("PyQt5 Video Player")
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.recordButton = QPushButton("Start Record")
        self.recordButton.setEnabled(True)
        self.recordButton.clicked.connect(self.startRecord)

        self.stopRecordButton = QPushButton("Stop Record")
        self.stopRecordButton.setEnabled(False)
        self.stopRecordButton.clicked.connect(self.stopRecord)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.error = QLabel()
        self.error.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        self.setMouseTracking(True)
        self.point = None

        self.tracker = QLabel()
        self.timer = TimerWidget()
        openButton = QPushButton("Open Video")
        openButton.setToolTip("Open Video File")
        openButton.setStatusTip("Open Video File")
        openButton.setFixedHeight(24)
        openButton.clicked.connect(self.openFile)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        butlayout = QHBoxLayout()
        butlayout.addWidget(openButton)
        butlayout.addWidget(self.recordButton)
        butlayout.addWidget(self.stopRecordButton)
        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(self.videoWidget, stretch = 3)
        layout.addLayout(controlLayout)
        layout.addWidget(self.timer)
        layout.addWidget(self.error)
        layout.addLayout(butlayout)
        layout.addWidget(self.tracker)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        self.marker_label = QLabel(self)

        pixmap = QPixmap(3, 3)
        pixmap.fill(Qt.black)

        self.marker_label.setPixmap(pixmap)
        self.marker_label.adjustSize()
        self.marker_label.hide()
        self.marker_label.raise_()

    def mousePressEvent(self, event):
        if not self.videoWidget.rect().contains(event.pos()):
            return
        if self.a == 0:
            return
        self.marker_label.move(event.pos() - self.marker_label.rect().center())
        self.marker_label.show()
        cord = event.pos()
        self.mas.append((cord.x(), cord.y(), self.mediaPlayer.position()))
        self.mediaPlayer.setPosition(self.mediaPlayer.position() + 167)

    def openFile(self):
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())

        if self.fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(self.fileName)))
            self.playButton.setEnabled(True)

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        self.timer.updatePosition(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        self.timer.updateDuration(duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.error.setText("Error: " + self.mediaPlayer.errorString())

    def mouseMoveEvent(self, event):
        self.tracker.setText('Mouse coords: ( %d : %d )' % (event.x(), event.y()))

    def startRecord(self):
        self.recordButton.setEnabled(False)
        self.stopRecordButton.setEnabled(True)
        self.playButton.setEnabled(False)
        self.a = 1
        self.mediaPlayer.pause()

    def stopRecord(self):
        self.recordButton.setEnabled(True)
        self.stopRecordButton.setEnabled(False)
        self.playButton.setEnabled(True)
        self.a = 0
        self.marker_label.hide()

    # def wheelEvent(self,event):
    #     mwidth = self.frameGeometry().width()
    #     mheight = self.frameGeometry().height()
    #     mleft = self.frameGeometry().left()
    #     mtop = self.frameGeometry().top()
    #     mscale = event.angleDelta().y() / 5
    #     self.setGeometry(mleft, mtop, mwidth + mscale, round((mwidth + mscale) / 1.778))



class TimerWidget(QLabel):
    def __init__(self):
        super().__init__()
        self.position = 0
        self.duration = 0

    def updatePosition(self, position):
        self.position = position
        self.updateText()

    def updateDuration(self, duration):
        self.duration = duration
        self.updateText()

    def updateText(self):
        self.setText(f'Time: {self.position//60000}:{(self.position%60000)//1000}:{self.position%1000} / {self.duration//60000}:{(self.duration%60000)//1000}:{self.duration%1000}')


app = QApplication(sys.argv)
videoplayer = VideoPlayer()
videoplayer.resize(640, 480)
videoplayer.show()
result = app.exec_()
resultName = '{}.result.txt'.format(videoplayer.fileName.split('/')[-1])
with open(resultName, 'w') as f:
    for dot in videoplayer.mas:
        f.write(' '.join(map(str, dot)))
        f.write('\n')
ploting(resultName)
sys.exit(result)
