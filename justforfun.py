import re
import sys
import json
from urllib.request import urlretrieve
import requests
import jsonpath
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")#
        MainWindow.resize(642, 455)#设置窗口大小
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(120, 50, 401, 41))
        self.lineEdit.setInputMask("")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(240, 340, 131, 41))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 642, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(self.download_mp3)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "QQ音乐下载器"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "请输入歌曲名称"))
        self.pushButton.setText(_translate("MainWindow", "点击下载"))

    def download_mp3(self):
        kw = self.lineEdit.text()
        url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=61781579913876194&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=10&w={}&g_tk_new_20200303=604315274&g_tk=604315274&loginUin=3421355804&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0'.format(
            kw)
        resp = requests.get(url)
        html_doc = resp.json()
        # print(html_doc)
        mids = jsonpath.jsonpath(html_doc, '$..mid')
        print(mids)
        one_url = 'http://www.douqq.com/qqmusic/qqapi.php'
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '65',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.douqq.com',
            'Origin': 'http://www.douqq.com',
            'Referer': 'http://www.douqq.com/qqmusic/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        data = {'mid': 'https://y.qq.com/n/yqq/song/{}.html'.format(mids[0])}
        req = requests.post(one_url, data=data, headers=headers).text
        print(req)
        # https://y.qq.com/portal/search.html#page=1&searchid=1&remoteplace=txt.yqq.top&t=song&w=%E6%A1%A5%E8%BE%B9%E5%A7%91%E5%A8%98

        # 字符串中提取数据！re  \/ 换成/   //
        req = json.loads(req)
        req = req.replace('\/', '/')
        print(req)
        # 万能匹配公式 除换行符以外 都可以匹配！
        rg = re.compile('"m4a":"(.*?)",')
        rs = re.findall(rg, req)
        print(rs)
        rs = rs[0]
        urlretrieve(rs, kw + '.mp3')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的软件app
    MainWindow = QtWidgets.QMainWindow()  # 创建一个QMainWindow，用来装载你需要的各种组件、控件
    ui = Ui_MainWindow()  # ui是你创建的ui类的实例化对象
    ui.setupUi(MainWindow)  # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow

    MainWindow.show()  # 执行QMainWindow的show()方法，显示这个QMainWindow
    sys.exit(app.exec_())
