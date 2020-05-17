from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import QSize,pyqtSlot
from PyQt5.QtWidgets import QMainWindow,QApplication, QWidget, QScrollArea, QVBoxLayout,QStackedWidget,QLineEdit,QGridLayout, QGroupBox, QLabel, QPushButton, QFormLayout,QToolBox,QMessageBox,QTabWidget
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
from get_mangainfo import get_latest,get_popular
import ctypes, functools,requests, time,sys
start = time.time()



           
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        latest_images, latest_titles = get_latest()
        popular_images, popular_titles = get_popular()

        self.user = ctypes.windll.user32
        

        #Setting up Main Window Properties
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle("Manga Reader")
        self.setStyleSheet("background-color: grey;")
        self.resize(self.user.GetSystemMetrics(0), self.user.GetSystemMetrics(1))
        
        #Setting up Layout and Scroll area properties
        layout = QtWidgets.QHBoxLayout(self)
        scrollArea = QtWidgets.QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollAreaWidgetContents = QtWidgets.QWidget()
        gridLayout = QtWidgets.QGridLayout(scrollAreaWidgetContents)
        scrollArea.setWidget(scrollAreaWidgetContents)

        layout.addWidget(scrollArea)
        layout.setGeometry(QtCore.QRect(0,0,int(self.frameGeometry().width()),self.frameGeometry().height()))
        
        #Variable declartion for properties
        horizontal_space = 100
        searchbox_size = [100,20]
        gridLayout.setHorizontalSpacing(horizontal_space)
        #Searchbox and buttons
        searchBox = QLineEdit(self)
        searchBox.setStyleSheet("background-color: white;")
        searchBox.setGeometry(self.user.GetSystemMetrics(0) - 200,10,searchbox_size[0],searchbox_size[1])

        search_button = QPushButton(self)
        search_button.setStyleSheet("background-color:white;");
        search_button.setFixedSize(50,20)
        search_button.setGeometry(self.user.GetSystemMetrics(0) - 80,10,0,0)

        #Main
        self.load_resources(20,latest_images,latest_titles,gridLayout,popular_images)
        self.setCentralWidget(self.centralwidget)
        self.showMaximized()

        self.show()
        
    def loadImage(self,image_url):
            img = QImage()
            req = Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
            data = urlopen(req).read()
            img.loadFromData(data)  
            img = img.scaled(100,150)
            return img
    def localImage(self,source,label,scaleW,scaleH):
        pixmap = QPixmap(source)
        label.setFixedSize(scaleW,scaleH)
        label.setPixmap(pixmap)
        return label
        
    def popup_message(self,event,message):
        msg = QMessageBox()
        msg.setWindowTitle("Manga Summary")

        msg.setText(' '.join(message.split()))
        x = msg.exec_()  # this will show our messagebox

    def on_click(self,num_loops,images,imgList):
        for x in range(num_loops):
            imgList[x].setPixmap(QPixmap(self.loadImage(images[x])))
            
        
    def load_resources(self,num_loops,images,titles,gridLayout,popular_images):
        popular = QPushButton(self)
        popular.setStyleSheet("background-color:white;");
        popular.setFixedSize(50,20)
        popular.setGeometry(0,10,0,0)
        
        titleList,imgList = [],[]
        photo_horizontal, title_horizontal = 0,0,
        title_vertical = 2
        photo_vertical = 3
        title_size = [100,50]
        rowcol_stretch = 100
        for i in  range(num_loops):
                F = QtWidgets.QLabel(self.centralwidget)
                F.setPixmap(QPixmap(self.loadImage(images[i])))

                label_title = QPushButton(self)
                label_title.setStyleSheet("QPushButton { background-color: rgba(255, 255, 255, 0); color : white; }");
                label_title.setFixedSize(title_size[0],title_size[1])
                titleList.append(label_title)
                imgList.append(F)

                gridLayout.setRowStretch(i,rowcol_stretch)
                gridLayout.setColumnStretch(i,rowcol_stretch)

                if title_horizontal >= 5:
                    title_vertical += 2
                    photo_vertical += 2
                    title_horizontal , photo_horizontal = 0,0

                gridLayout.addWidget(titleList[i],title_vertical,title_horizontal)

                gridLayout.addWidget(imgList[i], photo_vertical, photo_horizontal)

                title_horizontal += 1
                photo_horizontal += 1

                titleList[i].setText(titles[i])

                #titleList[i].mousePressEvent = functools.partial(self.label_event2, F=imgList[i])
        popular.clicked.connect(functools.partial(self.on_click,20,popular_images,imgList))

App = QApplication(sys.argv)
window = Window()
end = time.time()
print(end-start)
sys.exit(App.exec())
