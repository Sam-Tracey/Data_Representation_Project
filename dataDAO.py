import mysql.connector
from mysql.connector import cursor
import config as cfg
import requests
import json


class DataDAO:
    
    db=""
    def initConnect(self):
        db = mysql.connector.connect(
            host=cfg.db['host'],
            user=cfg.db['user'],
            password=cfg.db['password'],
            database=cfg.db['database'],
            pool_name = "mypool",
            pool_size = 25
        )
        return db

    def getConnection(self):
        db = mysql.connector.connect(
            pool_name = "mypool"

        )
        return db


    def __init__(self):
        self.url = cfg.fred['url']
        self.url_end = cfg.fred['url_end']
        self.db = self.initConnect()

    # Functions to load data from the FRED API (https://fred.stlouisfed.org/)
    
    def loadUnemployment(self, table = cfg.fred['unemployment']):
        db = self.getConnection()
        self.table = table
        self.response = requests.get(self.url + table + self.url_end)
        cursor = db.cursor()
        data = self.response.json()
        for d in data['observations']:
            date = d['date']
            value = d['value']
            # Since we are reading this file from an API we only want to update if there is new data.
            sql = "insert into unemployment (date, unemploymentRate) values (%s, %s) ON DUPLICATE KEY UPDATE date=date;"
            values = (date, value)
            cursor.execute(sql, values)
        db.commit()
        db.close()
        cursor.close()
        return

    def loadMFGEMP(self, table = cfg.fred['MFGEMP']):
        db = self.getConnection()
        self.table = table
        self.response = requests.get(self.url + table + self.url_end)
        cursor = db.cursor()
        data = self.response.json()
        for d in data['observations']:
            date = d['date']
            value = d['value']
            # Since we are reading this file from an API we only want to update if there is new data.
            sql = "insert into mfgemployees (date, num_employees) values (%s, %s) ON DUPLICATE KEY UPDATE date=date;"
            values = (date, value)
            cursor.execute(sql, values)
        db.commit()
        db.close()
        cursor.close()
        return

    def loadQuits(self, table = cfg.fred['Quits']):
        db = self.getConnection()
        self.table = table
        self.response = requests.get(self.url + table + self.url_end)
        cursor = db.cursor()
        data = self.response.json()
        for d in data['observations']:
            date = d['date']
            value = d['value']
            # Since we are reading this file from an API we only want to update if there is new data.
            sql = "insert into quits (date, num_quits) values (%s, %s) ON DUPLICATE KEY UPDATE date=date;"
            values = (date, value)
            cursor.execute(sql, values)
        db.commit()
        db.close()
        cursor.close()
        return

    def loadOpenings(self, table = cfg.fred['Openings']):
        db = self.getConnection()
        self.table = table
        self.response = requests.get(self.url + table + self.url_end)
        cursor = db.cursor()
        data = self.response.json()
        for d in data['observations']:
            date = d['date']
            value = d['value']
            # Since we are reading this file from an API we only want to update if there is new data.
            sql = "insert into jobopenings (date, num_openings) values (%s, %s) ON DUPLICATE KEY UPDATE date=date;"
            values = (date, value)
            cursor.execute(sql, values)
        db.commit()
        db.close()
        cursor.close()
        return

    def readUnemployment(self):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql="select * from unemployment"
        cursor.execute(sql)
        result = cursor.fetchall()
        # Convert all datetime.date returned from mysql to string
        for r in result:
            r['date'] = r['date'].strftime("%Y-%m-%d")
        db.close()
        cursor.close()
        return result


    def readMFGEMP(self):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql="select * from mfgemployees"
        cursor.execute(sql)
        result = cursor.fetchall()
        # Convert all datetime.date returned from mysql to string
        for r in result:
            r['date'] = r['date'].strftime("%Y-%m-%d")
        db.close()
        cursor.close()
        return result


    def readQuits(self):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql="select * from localattritionrate order by date desc"
        cursor.execute(sql)
        result = cursor.fetchall()
        # Convert all datetime.date returned from mysql to string
        for r in result:
            r['date'] = r['date'].strftime("%Y-%m-%d")
        cursor.close()
        db.close()
        return result

    def readOpenings(self):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql="select * from jobopenings"
        cursor.execute(sql)
        result = cursor.fetchall()
        # Convert all datetime.date returned from mysql to string
        for r in result:
            r['date'] = r['date'].strftime("%Y-%m-%d")
        cursor.close()
        db.close()
        return result

    def readSCQuits(self):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql="select * from quits"
        cursor.execute(sql)
        result = cursor.fetchall()
        # Convert all datetime.date returned from mysql to string
        for r in result:
            r['date'] = r['date'].strftime("%Y-%m-%d")
        db.close()
        cursor.close()
        return result
        

    # Reads local .csv file containing data on employee quits for the business (local_quits.csv)

    def loadLocalQuits(self):
        db = self.getConnection()
        cursor = db.cursor()
        # open csv with first column as date in format YYYY-MM-DD and second column as number of quits
        with open('local_quits.csv', 'r') as file:
            next(file)
            for line in file:
                date, num_quits = line.strip().split(',')
                # Since we are reading this file from an API we only want to update if there is new data.
                sql = "insert into localattritionrate (date, num_quit) values (%s, %s) ON DUPLICATE KEY UPDATE date=date;"
                values = (date, num_quits)
                cursor.execute(sql, values)

        db.commit()
        db.close()
        cursor.close()
        return

    def findQuitsByID(self, id):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql="select * from localattritionrate where id = %s"
        values = [id]
        cursor.execute(sql, values)
        result = cursor.fetchone()
        # convert datetime.date returned from mysql to string
        result['date'] = result['date'].strftime("%Y-%m-%d")
        db.close()
        cursor.close()
        return result

    def updateQuitsByID(self, values):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql="update localattritionrate set date = %s, num_quit = %s where id = %s"
        cursor.execute(sql, values)
        db.commit()
        db.close()
        cursor.close()
        return

    def createQuitsByID(self, values):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql="insert into localattritionrate (date, num_quit) values (%s, %s)"
        cursor.execute(sql, values)
        db.commit()
        db.close()
        cursor.close()
        return

    def deleteQuitsByID(self, id):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql="delete from localattritionrate where id = %s"
        values = [id]
        cursor.execute(sql, values)
        db.commit()
        db.close()
        cursor.close()
        return

    def findQuitsByDate(self, date):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql="select * from localattritionrate where date = %s"
        values = [date]
        cursor.execute(sql, values)
        result = cursor.fetchone()
        # convert datetime.date returned from mysql to string
        result['date'] = result['date'].strftime("%Y-%m-%d")
        db.close()
        cursor.close()
        return result

    def updateQuitsByDate(self, date, num_quit):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql="update localattritionrate set num_quit = %s where date = %s"
        values = [num_quit, date]
        cursor.execute(sql, values)
        db.commit()
        db.close()
        cursor.close()
        return

    def deleteQuitsByDate(self, date):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql="delete from localattritionrate where date = %s"
        values = [date]
        cursor.execute(sql, values)
        db.commit()
        db.close()
        cursor.close()
        return
    
    
    # Functions for CRUD operations on user data.
    
    
    def login(self, username, password):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql="select * from user where username = %s and password = %s"
        values = [username, password]
        cursor.execute(sql, values)
        result = cursor.fetchone()
        db.close()
        cursor.close()
        return result
    
    
    
    
    def getAllUsers(self):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql="select * from user"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return result

    def findUserByEmail(self, email):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql="select * from user where email = %s"
        values = [email]
        cursor.execute(sql, values)
        result = cursor.fetchone()
        db.close()
        cursor.close()
        return result
    
    
    def insertUser(self, username, password, email):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql="insert into user (username, password, email) values (%s, %s, %s)"
        values = [username, password, email]
        cursor.execute(sql, values)
        db.commit()
        db.close()
        cursor.close()
        return

    def updateUserByID(self, id, username, password, email):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql="update user set username = %s, password = %s, email = %s where id = %s"
        values = [username, password, email, id]
        cursor.execute(sql, values)
        db.commit()
        db.close()
        cursor.close()
        return

    def deleteUserByID(self, id):
        db = self.getConnection()
        cursor = db.cursor(dictionary=True)
        sql="delete from user where id = %s"
        values = [id]
        cursor.execute(sql, values)
        db.commit()
        db.close()
        cursor.close()
        return

dataDAO = DataDAO()




    