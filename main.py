#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import signal
import re

from PyQt4 import QtGui, QtCore, uic

from password_strength import PasswordStats
from models import Account
	


class SignInForm(QtGui.QWidget):
	def __init__(self):
		super(SignInForm, self).__init__()
		self.initUI()
		self.OkButton.clicked.connect(self.signingIn)
		self.SignUpButton.clicked.connect(self.signUp)

	def initUI(self):
		uic.loadUi("ui/SignInForm.ui", self)
		self.setWindowTitle(u"Авторизация")
		self.InfLabel.hide()
		centerOnScreen(self)
		self.setFixedSize(self.size())

	def signingIn(self):
		login = self.LoginTextEdit.text()
		password = self.PasswordTextEdit.text()
		if not login and not password:
			self.InfLabel.setText(u'Не заполнено поле')
			self.InfLabel.show()
		else:

			try:
				user = Account.get(login=login)
				if user:
					if login == user.login and password == user.password:
						self.form = InfoForm(login)
						self.form.show()
						self.close()
					else:
						self.InfLabel.setText(u'Неправильный логин или пароль') 
						self.InfLabel.show()	
			except:
				self.InfLabel.setText(u'Неправильный логин или пароль') 
				self.InfLabel.show()

	def signUp(self):
		self.form = SignUpForm()
		self.form.show()


class InfoForm(QtGui.QWidget):
	def __init__(self, login):
		super(InfoForm, self).__init__()
		self.initUI(login)


	def initUI(self, login):
		uic.loadUi("ui/InfoForm.ui", self)
		if  login:
			self.setWindowTitle(u"Привет %s" % login)
			self.InfLabel.setText(u'Залогинился')
		else:
			self.setWindowTitle(u"Регистрация прошла успешно")
			self.InfLabel.setText(u'Спасибо за регистрацию')
		centerOnScreen(self)
		self.setFixedSize(self.size())

class SignUpForm(QtGui.QWidget):
	def __init__(self):
		super(SignUpForm, self).__init__()
		self.initUI()
		self.LoginTextEdit.textChanged.connect(self.checkPass)
		self.PasswordTextEdit.textChanged.connect(self.checkPass)
		self.RePasswordTextEdit.textChanged.connect(self.checkPass)
		self.OkButton.clicked.connect(self.save)

	def initUI(self):
		uic.loadUi("ui/SignUpForm.ui", self)
		self.setWindowTitle(u"Регистрация")
		self.PasswordLabel.hide()
		self.PasswordProgressBar.hide()
		self.OkButton.setDisabled(True)
		centerOnScreen(self)
		self.setFixedSize(self.size())
	#[a-zA-Zа-яА-Я_0-9-]

	def checkPass(self):                              
		login = self.LoginTextEdit.text()
		password = self.PasswordTextEdit.text()
		repassword = self.RePasswordTextEdit.text()

		if not password or not repassword:
			self.PasswordLabel.hide()
			self.PasswordProgressBar.hide()
			self.OkButton.setDisabled(True)
		elif password != repassword:
			self.PasswordLabel.setText(u'Пароли не совпадают')
			self.PasswordLabel.show()
			self.OkButton.setDisabled(True)
		else:
			self.PasswordLabel.setText(u'Пароли совпадают')
			self.PasswordLabel.show()

			p = PasswordStats(password)
			passwordStrength = round((1-p.weakness_factor)*p.strength(), 2)*100

			self.PasswordProgressBar.setValue(passwordStrength)
			self.PasswordProgressBar.show()

			if not login:
				self.OkButton.setDisabled(True)
			else:
				pattern = re.compile(r'\w+')
				result = re.match(pattern, login)
				if not result:
					self.PasswordLabel.setText(u'Запрещенные символы в логине')
					return


				if passwordStrength > 10:
					self.OkButton.setEnabled(True)
				else:
					self.OkButton.setDisabled(True)
					self.PasswordLabel.setText(u'Слишком слабый пароль')

		
	def save(self):
		login = self.LoginTextEdit.text()
		password = self.PasswordTextEdit.text()
		try:
			existRecord = Account.get(login=login)
			self.PasswordLabel.setText(u'Такой логин занят')
		except:
			Account.create(login=login, password=password)
			self.form = InfoForm(login=None)
			self.form.show()
			self.close()


def centerOnScreen(self):
	resolution = QtGui.QDesktopWidget().screenGeometry()
	self.move(resolution.width()/2 - self.frameSize().width()/2, resolution.height()/2 - self.frameSize().height()/2 )
		

def main():
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	app = QtGui.QApplication(sys.argv)
	w = SignInForm()
	w.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()