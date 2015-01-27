__author__ = 'Denny'
import os,MySQLdb
env = os.getenv('SERVER_SOFTWARE')
if (env and env.startswith('Google App Engine/')):
    # Connecting from App Engine
    db = MySQLdb.connect(
        unix_socket='/cloudsql/ebayscraping:jaune',
        user='root')
else:
    # Connecting from an external network.
    # Make sure your network is whitelisted
    db = MySQLdb.connect(
        host='173.194.231.2',
        port=3306,
        user='root',
        passwd='seilah123')

cursor = db.cursor()
cursor.execute('SELECT 1 + 1')