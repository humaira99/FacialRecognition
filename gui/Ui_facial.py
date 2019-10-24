import os
import time

from PyQt5.Qt import *
from PIL import Image
from gui.FacialGui import Ui_MainWindow
from gui.Popup import Ui_Dialog
import sys


class MyDialog(QDialog):
    """Initialises pop up dataset showing the matched person

    """
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)


class MainWindow(QMainWindow):
    """Initialises main window of the GUI

    Attributes
    -----------
        counter: int
        keeps count of the number of people in the dataset
        _active: bool
        keeps track of whether the algorithm is running for the progress bar

    """

    def __init__(self):
        """Init's main window with basic layout of the GUI"""
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        self.counter = 0
        self.ui.stackedWidget.setCurrentIndex(0)
        self.getNames()
        self.ui.browseButton.clicked.connect(self.imageupload)
        self.ui.backButton.clicked.connect(self.backButtonPressed)
        self.ui.forwardButton.clicked.connect(self.forwardButtonPressed)
        self.ui.processButton.clicked.connect(self.process)
        self._active = False
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setMaximum(100)

    def progress(self):
        """Performs operation that shows the progress bar running"""

        while True:
            time.sleep(0.1)
            value = self.ui.progressBar.value() + 1
            self.ui.progressBar.setValue(value)
            QApplication.processEvents()
            if value > 80:
                break

    def backButtonPressed(self):
        """Performs operation to go back a page when the back arrow is pressed for showing dataset

        If back arrow is pressed on page 1, the page will go to 10 (loops)
        """

        if self.ui.stackedWidget.currentIndex() == 0:
            self.ui.stackedWidget.setCurrentIndex(9)
            self.ui.pageNumber.setText("Page " + str(10))
        else:
            self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.currentIndex() - 1)
            self.ui.pageNumber.setText("Page " + str(self.ui.stackedWidget.currentIndex() + 1))

    def forwardButtonPressed(self):
        """Performs operation to go forward a page when the forward arrow is pressed for showing dataset

        If forward arrow is pressed on page 10, the page will go to 1 (loops)
        """

        if self.ui.stackedWidget.currentIndex() == 9:
            self.ui.stackedWidget.setCurrentIndex(0)
            self.ui.pageNumber.setText("Page " + str(1))
        else:
            self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.currentIndex() + 1)
            self.ui.pageNumber.setText("Page " + str(self.ui.stackedWidget.currentIndex() + 1))

    def imageupload(self):
        """Displays dialoge box to choose the image to process

        Shows dialoge box as a pop up
        Shows the file path on the GUI
        Displays the chosen image

        """
        # show dialoge box to choose image
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '/Desktop', 'Images (*.jpg *.png)')

        # show filepath
        if self.filename:
            print(self.filename)
            self.ui.filepath.setText(str(self.filename))
            self.pixmap = QPixmap(self.filename)
            self.pixmap = self.pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.ui.uploaded.setPixmap(self.pixmap)

    def process(self):
        """Performs the facial recognition algorithm

        Sets _active to true as algorithm is running
        Runs algorithm and shows the processed image ON GUI

        """
        self._active = True

        if self.filename:
            self.progress()

            size = 300, 300

            foo = Image.open(self.filename)
            foo.thumbnail(size, Image.ANTIALIAS)
            foo.save(self.filename)

            cmd = 'python /Users/humairaahmed/Documents/SecondYear/G52GRP/AML/aml/face-recognition-opencv/recognize_faces_image.py ' \
                  '--encodings /Users/humairaahmed/Documents/SecondYear/G52GRP/AML/aml/face-recognition-opencv/encodings.pickle --image ' \
                  + self.filename
            os.system(cmd)

            self.ui.progressBar.setValue(100)
            # show analysed image
            self.pixmap2 = QPixmap('analysed_image.png')
            self.pixmap2 = self.pixmap2.scaled(300, 300, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.ui.analysed.setPixmap(self.pixmap2)

            # get name of the matched person
            self.nameFromFile()

    def getNames(self):
        """Gets names of all the people in the dataset from the name of the directory"""

        rootdir = "/Users/humairaahmed/Documents/SecondYear/G52GRP/AML/aml/face-recognition-opencv/dataset"

        for subdir, dirs, files in os.walk(rootdir):
            # loop through and get name for all directory; call method to show images
            for name in dirs:
                self.showImages(name)

    def showImages(self, name):
        """Displays the dataset

        Shows name and images of each person in the dataset

        Parameters
        ----------
            name: str
            name of the person to display pictures for

        """

        pics = []
        rootdir = "/Users/humairaahmed/Documents/SecondYear/G52GRP/AML/aml/face-recognition-opencv/dataset"
        self.counter += 1

        # loop through all images in each directory
        for file in os.listdir(rootdir + "/" + name):
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png") or file.endswith(
                    ".PNG") or file.endswith(".JPG"):
                pics.append(file)
        # create an icon for each image
        for i in range(len(pics)):
            item = QListWidgetItem()
            icon = QIcon()
            icon.addPixmap(QPixmap('' + rootdir + '/' + name + '/' + pics[i]), QIcon.Normal, QIcon.Off)

            item.setIcon(icon)
            widge = 'listWidget_' + str(self.counter)

            # display images and name
            eval('self.ui.' + widge + '.addItem(item)')
            eval('self.ui.label_' + str(self.counter) + '.setText(name)')

    def nameFromFile(self):
        """Gets the name of the matched person in the processed image from file, for the pop up"""

        # open file and get name
        f = open("namepopup.txt", "r")
        self.nameofperson = f.read()


        if(self.nameofperson != "Unknown"):
            if(self.nameofperson != ""):
                self.popup()


    def popup(self):
        """create a pop up which shows dataset of matched person"""

        if (self.nameofperson != "Unknown"):
            if (self.nameofperson != ""):
                self.myDialog = MyDialog()
                self.myDialog.ui.label.setText(self.nameofperson)

            pics = []
            rootdir = "/Users/humairaahmed/Documents/SecondYear/G52GRP/AML/aml/face-recognition-opencv/dataset"

            for file in os.listdir(rootdir + "/" + self.nameofperson):
                if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png") or file.endswith(
                        ".PNG") or file.endswith(".JPG"):
                    pics.append(file)

            for i in range(len(pics)):
                item = QListWidgetItem()
                icon = QIcon()
                icon.addPixmap(QPixmap('' + rootdir + '/' + self.nameofperson + '/' + pics[i]), QIcon.Normal, QIcon.Off)
                item.setIcon(icon)
                self.myDialog.ui.listWidget.addItem(item)

            self.myDialog.show()

            f = open("namepopup.txt", "w")
            f.truncate(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

# pyuic5 gui/facialgui.ui -o gui/FacialGui.py
# pyuic5 gui/popup.ui -o gui/PopUp.py
