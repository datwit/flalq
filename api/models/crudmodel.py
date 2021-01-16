#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import Session


session = Session()


class crudmodel():
    def create(self, row):
        session.add(row)
        session.commit()
        return self

    def update(self, row):
        session.add(row)
        session.commit()
        return self

    def delete(self, row):
        session.add(row)
        session.commit()
        return self