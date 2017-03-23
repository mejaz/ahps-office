import pyodbc
import os
from shutil import copyfile

def make_a_connection():
	""" Connects to MS Access DB """

	curr_dir = os.getcwd()

	db_file = "%s\%s" % (curr_dir, "AHPSDB.accdb", )

	conn_str = 'Driver={Microsoft Access Driver (*.mdb, *.accdb)};Dbq=%s;Uid=Admin;Pwd=Hp@1986;' % \
					(db_file,)

	try:
		conn = pyodbc.connect(conn_str)
		return [conn, 0]
	except Exception, e:
		return [str(e), 1]

def disconnect_database(objConn):
	""" Closes the DB """
	
	try:
		objConn.close()
		return [0, 0]
	except Exception, e:
		return [str(e), 1]


def insert_records(connObj, sql_stmt):
	""" Inserts records into table name """

	try:
		cur = connObj.cursor()
		cur.execute(sql_stmt)
		return 0
	except Exception, e:
		return str(e)

def copy_files(sourceFile, destinationFile, fileType):
	""" Copies files from Source to Destination """

	cwd = os.getcwd()
	folderPath = "%s\%s" % (str(cwd), fileType)

	if os.path.exists(folderPath) != True:
		os.makedirs(folderPath)

	try:
		copyfile('%s' % str(sourceFile), '%s\%s' % (folderPath, str(destinationFile), ))
		return 0

	except Exception, e:
		return str(e)

def get_last_rollnumber(connObj):
	""" Retrieves the roll number that was added last to the Database """

	try:
		cur = connObj.cursor()
		rows = cur.execute('SELECT TOP 1 ROLL_NUMBER FROM STUDENT_INFO ORDER BY ROLL_NUMBER DESC;').fetchall()

		return rows[0][0]

	except Exception, e:

		return str(e)

def getRecords(connObj, searchQuery):

	try:
		cur = connObj.cursor()
		rows = cur.execute(searchQuery)

		return rows
	except Exception, e:
		return e
	
# i = copy_files('C:\Users\msiddiq1\Documents\Test-Python\Project Scratch\\a.txt', 'c.txt')
# print i

# getClassesQuery = 'SELECT CLASSES FROM CLASS_INFO;'
# getSectionsQuery = 'SELECT SECTIONS FROM CLASS_INFO;'


# conn = make_a_connection()

# print conn


# r = getRecords(conn[0], getClassesQuery)

# for x in r:
# 	print x