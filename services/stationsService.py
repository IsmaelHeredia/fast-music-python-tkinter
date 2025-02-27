#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from database import get_session
from models import Stations

class StationsService:

    def list(self):
        with get_session() as session:
            stations = session.query(Stations).order_by(Stations.updated_at.desc()).all()
            return [{
                "id": station.id,
                "name": station.name,
                "link": station.link,
                "categories": station.categories,
            } for station in stations]

    def findStationByName(self, stationName):
        with get_session() as session:
            station = session.query(Stations).filter(Stations.name == stationName).first()
            if station:
                return {
                    "id": station.id,
                    "name": station.name,
                    "link": station.link,
                    "categories": station.categories
                }
        return None

    def importFile(self, fullpath):
        try:
            with open(fullpath, 'r') as json_file:
                json_list = json.load(json_file)
                with get_session() as session:
                    for item in json_list:
                        name = item['name']
                        link = item['link']
                        categories = item['categories']
                        if not session.query(Stations).filter_by(name=name).first():
                            station = Stations(
                                name=name,
                                link=link,
                                categories=categories
                            )
                            session.add(station)
                    session.commit()
            return True
        except Exception as e:
            return False

    def validate(self):
        with get_session() as session:
            stations = session.query(Stations).order_by(Stations.updated_at.desc()).all()
            for station in stations:
                try:
                    response = requests.get(station.link, stream=True, timeout=5)
                    if response.status_code == 200:
                        print(f'Station {station.name} OK')
                    else:
                        print(f'Station {station.name} {station.link} FAIL')
                        session.delete(station)
                        session.commit()
                except requests.RequestException:
                    print(f'Station {station.name} {station.link} FAIL')
                    session.delete(station)
                    session.commit()
        return True

    def exportFile(self):
        return True
