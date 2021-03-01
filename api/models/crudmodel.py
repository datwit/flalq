#!/usr/bin/python
# -*- coding: utf-8 -*-

from api.utils.database import session, engine


class Crudmodel():
    def create(self, row):
        session.add(row)
        return session.commit()

    def update(self):
        return session.commit()

    def delete(self, row):
        session.delete(row)
        return session.commit()