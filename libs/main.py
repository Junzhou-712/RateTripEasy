import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QGridLayout,QAbstractItemView, QHeaderView,
QLabel, QLineEdit, QTextEdit, QTableWidgetItem, QTableView)
from PyQt5 import QtCore
from rater import SceneData,SceneTableWidget, SceneRating
class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.initUi()
    def initUi(self):
        sceneName = QLineEdit()
        searchBtn = QPushButton("搜索")
        searchTip = QLabel("")
        sceneName.setPlaceholderText("请输入景区名等信息进行搜索")
        reviewField = QTextEdit()
        reviewField.setPlaceholderText("留下你的精彩评论吧")
        self.ratingBlock = SceneRating()
        self.scene_table = SceneTableWidget()

        searchBtn.clicked.connect(lambda:self.searchFn(sceneName, self.scene_table,searchTip))

        self.ratingTip = QLabel("目前尚未选中需要进行评分的景区，请选中景区并利用右侧滑块进行评分")
        self.ratingValTip = QLabel("")
        self.scene_table.itemClicked.connect(self.changeTips)
        #提交评分按键
        rateBtn = QPushButton("提交评分")
        rateBtn.clicked.connect(lambda:self.scene_table.sendRate(self.ratingBlock.value()/10))

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(sceneName,1,0,1,1)
        grid.addWidget(searchBtn,1,1)
        grid.addWidget(searchTip,1,2)
        grid.addWidget(self.scene_table,2,0,1,3)
        grid.addWidget(self.ratingBlock,2,4)
        grid.addWidget(rateBtn,3,4)
        grid.addWidget(self.ratingTip,3,0)
        grid.addWidget(self.ratingValTip,4,0)
        grid.addWidget(reviewField,5,0)
        self.setLayout(grid)
        self.setGeometry(600, 400, 400, 450) 
        self.setWindowTitle('Trip Rater Chengdu')
        self.show()
    def searchFn(self,sceneName,dataTable,searchTip):
        if(len(dataTable.selectedItems()) != 0):
            selected_row = dataTable.selectedItems()[0].row() 
            for j in range(3):
                dataTable.item(selected_row,j).setSelected(0)
        if(sceneName.text() != ''):
            searchText = sceneName.text()
            searchitems = dataTable.findItems(searchText,QtCore.Qt.MatchContains)
            if(len(searchitems) < 1):
                searchTip.setText("未查找到数据！")
                return
            row = searchitems[0].row()
            dataTable.verticalScrollBar().setSliderPosition(row)
            for j in range(3):
                dataTable.item(row,j).setSelected(1)
            searchTip.setText("查找成功！")
    def changeTips(self,index):
        selected_content = self.scene_table.selectedItems()[0].text()
        selected_ratings = float(self.scene_table.selectedItems()[1].text())
        if(selected_ratings >= 4.0):
            recommendation = "。该景点的评价优秀，建议游玩"
        else:
            recommendation = " 。该景点的评价较一般，请斟酌考虑"
        self.rating_val = str(self.ratingBlock.value()/10)
        tips_1 = "您选中了"+selected_content+recommendation
        self.ratingBlock.valueChanged.connect(self.changeRate)
        self.ratingTip.setText(tips_1)
    def changeRate(self):
        rating_val = str(self.ratingBlock.value()/10)
        tips_2 = "您为它打了"+rating_val+"/5.0分"
        self.ratingValTip.setText(tips_2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    sys.exit(app.exec())