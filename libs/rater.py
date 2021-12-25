import json
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QSlider, QAbstractItemView,QTableWidget, QTableView, QPushButton, QHeaderView
from PyQt5 import QtCore,QtGui
class SceneData:
    items = []
    row = 0
    def __init__(self, *args, **kwargs):
        self.processDataFn()

    def processDataFn(self):
        fileName = 'data.json'
        #处理使用Spider爬取的数据
        with open(fileName) as f:
            pop_data = json.load(f)
            for pop_dict in pop_data:
                scene_name = pop_dict['店铺名']
                rating = pop_dict['店铺总分']
                ratingsNums = pop_dict['评论总数']
                item = [scene_name, rating, ratingsNums]
                self.items.append(item)
                self.row += 1
            f.close()
            
class SceneTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.render()
    def render(self):
        self.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只能选中一行
        self.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑
        self.setSelectionBehavior(QAbstractItemView.SelectRows);  # 设置只有行选中
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(['景区名称', '评分', '评分人数'])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #对排序箭头进行显示
        headers = self.horizontalHeader()
        headers.setSortIndicator(1, QtCore.Qt.DescendingOrder)
        headers.setSortIndicatorShown(True)
        headers.sortIndicatorChanged.connect(self.toggleMode)
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(QTableView.NoEditTriggers)

        data = SceneData()
        self.setRowCount(data.row)
        for i in range(len(data.items)):
            item = data.items[i]
            for j in range(len(item)):
                item = QTableWidgetItem(str(data.items[i][j]))
                self.setItem(i,j,item)

        self.sortItems(1,QtCore.Qt.DescendingOrder)
    def toggleMode(self,index,order):
        if(index != 0):
            self.sortItems(index,order)
    def sendRate(self,ratingVal):
        scene_item = self.selectedItems()
        scene_row = scene_item[0].row()
        sceneName = scene_item[0].text()
        sumRatingNum = float(scene_item[1].text()) * float(scene_item[2].text())
        sumRatingNum += ratingVal
        sumRatings = int(scene_item[2].text())+1
        finalRatingVal = round(float(sumRatingNum/(sumRatings)),2)
        updatedDataLs = [finalRatingVal, sumRatings]
        for i in range(1,3):
            item = QTableWidgetItem(str(updatedDataLs[i-1]))
            self.setItem(scene_row,i,item)

class SceneRating(QSlider):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.render()
    def render(self):
        self.setMinimum(0)
        self.setMaximum(50)
        self.setSingleStep(1)
        self.setValue(0)
        self.setTickPosition(QSlider.TicksBelow)
        self.setTickInterval(1)


