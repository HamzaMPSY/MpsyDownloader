from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import os
from os import path
import sys
import urllib.request
import pafy


FORM_CLASS,_= loadUiType(path.join(path.dirname(__file__),"main.ui"))


class MainApp(QMainWindow,FORM_CLASS):
	"""docstring for MainApp"""
	def __init__(self, arg=None):
		super(MainApp, self).__init__(arg)
		QMainWindow.__init__(self)
		self.setupUi(self)
		self.handel_UI()
		self.handel_Buttons()
	
	def handel_UI(self):
		self.setWindowTitle('MPSY Downloader')
		self.setFixedSize(504,200)
		self.setWindowIcon(QIcon('images.png'))
			


	def handel_Buttons(self):
		self.QBtnStart.clicked.connect(self.Download)
		self.QBtnBrs.clicked.connect(self.handel_Browse1)
		self.QBtnBrs_2.clicked.connect(self.handel_Browse2)
		self.QBtnStart_2.clicked.connect(self.download_youtube)
		self.QBtnBrs_4.clicked.connect(self.get_Streams)
		self.QBtnBrs_5.clicked.connect(self.get_Streams_list)
		self.QBtnStart_3.clicked.connect(self.download_youtube_list)
		self.QBtnBrs_3.clicked.connect(self.handel_Browse2)

	def handel_Browse1(self):
		save_place = QFileDialog.getSaveFileName(self,caption="Save As",directory=".",filter="All Files (*.*)")
		self.QTxtLoc.setText(save_place[0])


	def handel_Browse2(self):
		save_place = QFileDialog.getExistingDirectory(self,caption="Select Directory")
		self.QTxtLoc_2.setText(save_place)
		self.QTxtLoc_3.setText(save_place)


	def handel_progressBar(self,blocknumber,blocksize,totalsize):
		read = blocknumber * blocksize
		if totalsize  > 0 :
			per = read*100/totalsize
			self.QProBar.setValue(per)
			QApplication.processEvents()

	def handel_progressBar2(self,total, recvd, ratio, rate, eta):
		self.QProBar_2.setValue(ratio*100)
		QApplication.processEvents()

	def handel_progressBar3(self,total, recvd, ratio, rate, eta):
		self.QProBar_3.setValue(ratio*100)
		QApplication.processEvents()

	def Download(self):
		#url, location, progress
		url = self.QTxtUrl.text()
		location = self.QTxtLoc.text()
		if url == '' or location == '':
			QMessageBox.warning(self,"Error","please complete all fields")
		else:
			try:
				urllib.request.urlretrieve(url,location,self.handel_progressBar)
				QMessageBox.information(self,"Download Completed","The Download Finished")
			except Exception as e:
				raise(e)
				QMessageBox.warning(self,"Download Error","The Download Failed")
			
			self.QProBar.setValue(0)
			self.QTxtUrl.setText('')
			self.QTxtLoc.setText('')

	def download_youtube(self):
		url = self.QTxtUrl_2.text()
		location = self.QTxtLoc_2.text()
		if url == '' or location == '':
			QMessageBox.warning(self,"Error","please complete all fields")
		else:
			v=pafy.new(url)
			save_place= location
			st = v.allstreams
			quality = self.comboBox.currentIndex()
			try:
				down = st[quality].download(save_place,callback=self.handel_progressBar2)
				QMessageBox.information(self,"Download Completed","The Download Finished")
			except Exception as e:
				QMessageBox.warning(self,"Download Error","The Download Failed")

	def get_Streams(self):
		v=pafy.new(self.QTxtUrl_2.text())
		st = v.allstreams
		for s in st:
			size=s.get_filesize()
			data = '{} {} {} {}'.format(s.mediatype,s.extension,s.quality,size)
			self.comboBox.addItem(data)

	def get_Streams_list(self):
		self.comboBox_2.addItem('Audio')
		self.comboBox_2.addItem('Video')

	def download_youtube_list(self):
		url = self.QTxtUrl_3.text()
		save_place= self.QTxtLoc_3.text()
		if url == '' or save_place == '':
			QMessageBox.warning(self,"Error","please complete all fields")
		else:
			v=pafy.get_playlist(url)
			quality = self.comboBox_2.currentIndex()
			os.chdir(save_place)
			if os.path.exists(str(v['title'])):
				os.chdir(str(v['title']))
			else:
				os.mkdir(str(v['title']))
				os.chdir(str(v['title']))
			
			if quality == 0:
				i=1;
				for vi in v['items']:
					self.label_9.setText(str(i) + "/" + str(len(v['items'])))
					i+=1
					try:
						vi['pafy'].getbestaudio().download(callback=self.handel_progressBar3)
					except Exception as e:
						pass
					


			elif quality == 1 :
				i=1
				for vi in v['items']:
					self.label_9.setText(str(i) + "/" + str(len(v['items'])))
					i+=1
					try:
						vi['pafy'].getbest(preftype='mp4').download(callback=self.handel_progressBar3)
					except Exception as e:
						pass
					

def main():
	app = QApplication(sys.argv)
	window = MainApp()
	window.show()
	app.exec_()

if __name__ == '__main__':
	main()