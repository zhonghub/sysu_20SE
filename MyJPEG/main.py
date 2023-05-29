import Compress
import os
from PyQt5.QtWidgets import QLineEdit, QPushButton, QLabel, QGridLayout, QFileDialog, QDialog, QApplication
from PyQt5.QtGui import QPixmap

myJpeg = Compress.MyJPEG()


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.msg = ""
        self.openfile_name = "正在压缩"
        # 设置窗口标题和大小
        self.setWindowTitle('JPEG图像压缩')
        # self.setFixedSize(1800, 1200)
        # 可拉伸窗口
        self.setMinimumSize(1000, 600)

        # 图片显示
        self.avatar_label1 = QLabel("原始图片")
        pixmap = QPixmap("")
        self.avatar_label1.setPixmap(pixmap)
        self.avatar_label1.setScaledContents(True)

        self.avatar_label2 = QLabel("解压后图片")
        pixmap = QPixmap('')
        self.avatar_label2.setPixmap(pixmap)
        self.avatar_label2.setScaledContents(True)
        # 创建控件并添加到窗口中
        self.btn1 = QPushButton('开始压缩')
        self.btn2 = QPushButton('解压')
        self.label11 = QLabel('原始图片:')
        self.label12 = QLabel('解压后图片:')
        self.label2 = QLabel('压缩信息:')
        self.label0 = QLabel('输入压缩程度(1~999,越大压缩程度越高):')
        self.rate_edit = QLineEdit()
        self.rate_edit.setText("100")

        # 创建网格布局管理器，并将控件添加到网格中
        layout = QGridLayout()
        layout.addWidget(self.label0, 0, 0)
        layout.addWidget(self.rate_edit, 0, 1)
        layout.addWidget(self.label11, 1, 0)
        layout.addWidget(self.label12, 1, 1)
        layout.addWidget(self.avatar_label1, 2, 0)
        layout.addWidget(self.avatar_label2, 2, 1)
        layout.addWidget(self.btn1, 3, 0)
        layout.addWidget(self.btn2, 3, 1)
        layout.addWidget(self.label2, 4, 0, 1, -1)
        # layout.addWidget(self.label2, 4, 1)
        # 设置布局管理器
        self.setLayout(layout)

        # 将 clicked 信号绑定到 btn1_clicked 函数
        self.btn1.clicked.connect(self.btn1_clicked)
        self.btn2.clicked.connect(self.btn2_clicked)

    # 压缩按钮
    def btn1_clicked(self):
        pixmap = QPixmap("")
        self.avatar_label1.setPixmap(pixmap)
        pixmap = QPixmap("")
        self.avatar_label2.setPixmap(pixmap)
        self.msg = "压缩信息:\n\n"
        self.label2.setText(self.msg)

        myJpeg.init_Quantization_Table(int(self.rate_edit.text()))
        openfile_name1 = QFileDialog.getOpenFileName(self, '选择文件', '', 'Images (*.png *.xpm *.jpg)')
        self.openfile_name = openfile_name1[0]
        myJpeg.Compress(self.openfile_name)
        img_path2 = os.path.splitext(self.openfile_name)[0] + ".txt"
        file_size1 = os.path.getsize(self.openfile_name)
        file_size2 = os.path.getsize(img_path2)
        self.msg += "原始图片大小(Byte): —— " + self.openfile_name + "\n"
        self.msg += "" + str(file_size1) + "\n"
        self.msg += "开始压缩\n压缩完成\n"
        self.msg += "压缩文件大小(Byte): —— " + img_path2 + "\n"
        self.msg += "" + str(file_size2) + "\n" + "压缩比=" + str(file_size1 / file_size2) + "\n\n"
        self.label2.setText(self.msg)
        pixmap = QPixmap(openfile_name1[0])
        self.avatar_label1.setPixmap(pixmap)

    # 解压按钮
    def btn2_clicked(self):
        self.msg += "开始解码" + "\n"
        self.label2.setText(self.msg)
        img_path2 = os.path.splitext(self.openfile_name)[0] + ".txt"
        myJpeg.Decompress(img_path2)
        img_path = os.path.splitext(self.openfile_name)[0] + "_result.png"
        pixmap = QPixmap(img_path)
        self.avatar_label2.setPixmap(pixmap)
        self.msg += "解码完成" + "\n" + img_path + "\n\n"
        self.label2.setText(self.msg)


if __name__ == '__main__':
    app = QApplication([])
    login_dialog = LoginDialog()
    login_dialog.show()
    app.exec()
