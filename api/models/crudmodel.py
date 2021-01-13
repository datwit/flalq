#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import session

class cud():
    def create(self):
        session.add(self)
        session.commit()
        return self