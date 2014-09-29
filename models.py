#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import *

database = SqliteDatabase('accounts.db')

class Base(Model):
	class Meta:
		database = database

class Account(Base):
	login = CharField()
	password = CharField()