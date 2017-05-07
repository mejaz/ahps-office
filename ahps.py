#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from time import sleep
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from dblib import make_a_connection, insert_records, \
    disconnect_database, copy_files, get_last_rollnumber, getRecords, update_records
import json
from funclib import uploadfile
from sms import sendSMS



UPLOAD_FOLDER_STUDENT_PIC = 'static/images/students'
UPLOAD_FOLDER_PARENT_PIC = 'static/images/parents'
UPLOAD_FOLDER_STAFF_PIC = 'static/images/staff'

ALLOWED_PIC_EXTNS = set(['jpeg', 'gif', 'png', 'jpg'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER_STUDENT_PIC'] = UPLOAD_FOLDER_STUDENT_PIC
app.config['UPLOAD_FOLDER_PARENT_PIC'] = UPLOAD_FOLDER_PARENT_PIC
app.config['UPLOAD_FOLDER_STAFF_PIC'] = UPLOAD_FOLDER_STAFF_PIC

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/newAdmission', methods=['GET', 'POST'])
def newAdmission():

    """ New admission """

    conn = make_a_connection()

    getClassesQuery = 'SELECT CLASSES FROM CLASS_INFO;'
    getSectionsQuery = 'SELECT SECTIONS FROM CLASS_INFO;'
    lastRnum = int(get_last_rollnumber(conn[0])) + 1
    studentStatus = "Active"

    allClasses = getRecords(conn[0], getClassesQuery)
    allSections = getRecords(conn[0], getSectionsQuery)

    allClasses = [x for x in allClasses if x[0] is not None]
    allSections = [x for x in allSections if x[0] is not None]

    

    if request.method == 'POST':

        print '1'
        # roll number

        rnum = lastRnum

        # student info

        fname = request.form['fname']
        mname = request.form['mname']
        lname = request.form['lname']

        print '2'

        sgender = request.form['sgender']
        dob = request.form['dob']

        print '3'

        sclass = request.form['class-selected']
        ssection = request.form['section-selected']

        print '4'

        status = studentStatus
        doa = request.form['doa']

        print '5'
        spic = request.files['student-pic'].filename
        # print spic

        print '6'

        # spic file
        spicFileObj = request.files['student-pic']
        spicDestPath = app.config['UPLOAD_FOLDER_STUDENT_PIC']

        # ppic file
        ppicFileObj = request.files['parent-pic']
        ppicDestPath = app.config['UPLOAD_FOLDER_PARENT_PIC']        

        # parents info

        fcname = request.form['fcname']
        foccup = request.form['foccup']

        print '7'

        mcname = request.form['mcname']
        moccup = request.form['moccup']

        print '8'

        mobPrim = request.form['mob-primary']
        mobSec = request.form['mob-secondary']

        print '9'

        email = request.form['email']
        addr = request.form['comp-addr']

        print addr

        print '10'

        allIns = []


        try:

            spicFilepath = uploadfile(rnum, spicFileObj, spicDestPath, ALLOWED_PIC_EXTNS)
            print spicFilepath[1]

            ppicFilepath = uploadfile(rnum, ppicFileObj, ppicDestPath, ALLOWED_PIC_EXTNS)
            print ppicFilepath[1]            

            # student records Insert

            insQuery = \
                """INSERT INTO STUDENT_INFO (ROLL_NUMBER, FIRST_NAME, MIDDLE_NAME, LAST_NAME, DOB, DOA, STUDENT_PICTURE, PARENT_PICTURE, STUDENT_CLASS, STUDENT_SECTION, STUDENT_STATUS, GENDER) VALUES \
                    (%d, \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\');""" \
                % (
                int(rnum),
                fname.strip(),
                mname.strip(),
                lname.strip(),
                dob,
                doa,
                spicFilepath[1].split('\\')[1],
                ppicFilepath[1].split('\\')[1],
                sclass.strip(),
                ssection.strip(),
                status.strip(),
                sgender.strip(),
                )

            print  insQuery
            insRecds = insert_records(conn[0], insQuery)
            print insRecds

            if insRecds == 0:
                allIns.append(1)
                
            # Parents records Insert
            pInsQuery = \
                """ INSERT INTO STUDENT_PARENT (ROLL_NUMBER, FATHER_NAME, MOTHER_NAME, FATHER_OCCUPATION, MOTHER_OCCUPATION) VALUES \
                    (%d, \'%s\', \'%s\', \'%s\', \'%s\'); """ \
                % (
                int(rnum),
                fcname.strip(),
                mcname.strip(),
                foccup.strip(),
                moccup.strip()
                )

            print  pInsQuery
            pinsRecds = insert_records(conn[0], pInsQuery)
            print pinsRecds

            if pinsRecds == 0:
                allIns.append(1)


            # Address insert
            addrInsQuery = \
                """ INSERT INTO STUDENT_ADDRESS (ROLL_NUMBER, STUDENT_ADDRESS) VALUES \
                    (%d, \'%s\'); """ \
                % (
                int(rnum),
                addr.strip()
                )

            print  addrInsQuery
            addrinsRecds = insert_records(conn[0], addrInsQuery)
            print addrinsRecds  

            if addrinsRecds == 0:
                allIns.append(1)

            # Contact Info insert
            cntInsQuery = \
                """ INSERT INTO STUDENT_CONTACT (ROLL_NUMBER, PRIMARY_MOB, SECONDARY_MOB, EMAIL) VALUES \
                    (%d, \'%s\', \'%s\', \'%s\'); """ \
                % (
                int(rnum),
                mobPrim.strip(),
                mobSec.strip(),
                email.strip()
                )

            print  cntInsQuery
            cntinsRecds = insert_records(conn[0], cntInsQuery)
            print cntinsRecds

            if cntinsRecds == 0:
                allIns.append(1)

        except Exception, e:

            print e
        

        # check if all insert were successfull, then commit
        if sum(allIns) == 4:
            conn[0].commit()
            print 'commit'

            flash('Saved Successfully!!')
            discDB = disconnect_database(conn[0])
            print discDB[0]        
            

        else:

            flash('Error in saving records. Please try again!!')
            discDB = disconnect_database(conn[0])
            print discDB[0]                   


        return redirect(url_for('newAdmission', classes=allClasses,
                               sections=allSections, gender=['Male',
                               'Female'], rnum=lastRnum, sts=studentStatus))
    else:

        return render_template('newAdmission.html', classes=allClasses,
                               sections=allSections, gender=['Male',
                               'Female'], rnum=lastRnum, sts=studentStatus)


@app.route('/studentSearch', methods=['GET', 'POST'])
def studentSearch():

    
    conn = make_a_connection()

    getClassesQuery = 'SELECT CLASSES FROM CLASS_INFO;'
    getSectionsQuery = 'SELECT SECTIONS FROM CLASS_INFO;'

    allClasses = getRecords(conn[0], getClassesQuery)
    allSections = getRecords(conn[0], getSectionsQuery)

    allClasses = [x for x in allClasses if x[0] is not None]
    allSections = [x for x in allSections if x[0] is not None]     
        
    if request.method == 'POST':   
        if request.form['rnum'] != "":
            rnum = request.form['rnum']

            # query by roll number

            rnumQuery = 'SELECT ROLL_NUMBER, FIRST_NAME, MIDDLE_NAME, LAST_NAME, DOB, STUDENT_CLASS, STUDENT_SECTION FROM STUDENT_INFO WHERE ROLL_NUMBER=%d;' % int(rnum)
            
            print rnumQuery            

            records = getRecords(conn[0], rnumQuery)

            print records

            return render_template('studentSearch.html', classes = allClasses, sections = allSections, records = records)

        elif (request.form['fname'] != "" or request.form['mname'] != "" or request.form['lname'] != ""):

            fname = request.form['fname']
            mname = request.form['mname']
            lname = request.form['lname']

            if (fname != "" and mname != "" and lname != ""):

                nameQuery = """ SELECT ROLL_NUMBER, FIRST_NAME, MIDDLE_NAME, LAST_NAME, DOB, STUDENT_CLASS, STUDENT_SECTION 
                FROM STUDENT_INFO 
                WHERE FIRST_NAME=\'%s\'
                AND MIDDLE_NAME=\'%s\'
                AND LAST_NAME=\'%s\'; """ % (fname, mname, lname)

                print nameQuery

            elif (fname != "" and mname != "" and lname == ""):

                nameQuery = """ SELECT ROLL_NUMBER, FIRST_NAME, MIDDLE_NAME, LAST_NAME, DOB, STUDENT_CLASS, STUDENT_SECTION 
                FROM STUDENT_INFO 
                WHERE FIRST_NAME=\'%s\'
                AND MIDDLE_NAME=\'%s\'; """ % (fname, mname)

                print nameQuery            

            elif (mname != "" and lname != "" and fname == ""):

                nameQuery = """ SELECT ROLL_NUMBER, FIRST_NAME, MIDDLE_NAME, LAST_NAME, DOB, STUDENT_CLASS, STUDENT_SECTION 
                FROM STUDENT_INFO 
                WHERE MIDDLE_NAME=\'%s\'
                AND LAST_NAME=\'%s\'; """ % (mname, lname)

                print nameQuery

            elif (fname != "" and lname != "" and mname == ""):

                nameQuery = """ SELECT ROLL_NUMBER, FIRST_NAME, MIDDLE_NAME, LAST_NAME, DOB, STUDENT_CLASS, STUDENT_SECTION 
                FROM STUDENT_INFO 
                WHERE FIRST_NAME=\'%s\'
                AND LAST_NAME=\'%s\'; """ % (fname, lname)

                print nameQuery            

            elif (fname == "" and mname == ""  and lname != ""):

                nameQuery = """ SELECT ROLL_NUMBER, FIRST_NAME, MIDDLE_NAME, LAST_NAME, DOB, STUDENT_CLASS, STUDENT_SECTION 
                FROM STUDENT_INFO 
                WHERE LAST_NAME=\'%s\'; """ % (lname, )

                print nameQuery            

            elif (mname == "" and lname == "" and fname != ""):

                nameQuery = """ SELECT ROLL_NUMBER, FIRST_NAME, MIDDLE_NAME, LAST_NAME, DOB, STUDENT_CLASS, STUDENT_SECTION 
                FROM STUDENT_INFO 
                WHERE FIRST_NAME=\'%s\'; """ % (fname, )

                print nameQuery            

            elif (lname == "" and fname == "" and mname != ""):

                nameQuery = """ SELECT ROLL_NUMBER, FIRST_NAME, MIDDLE_NAME, LAST_NAME, DOB, STUDENT_CLASS, STUDENT_SECTION 
                FROM STUDENT_INFO 
                WHERE MIDDLE_NAME=\'%s\'; """ % (mname, )

                print nameQuery      


            records = getRecords(conn[0], nameQuery).fetchall()
            discDB = disconnect_database(conn[0])
            print discDB[0]

            return render_template('studentSearch.html', classes = allClasses, sections = allSections, records = records)

        else:

            selClass = request.form['class']
            selSec = request.form['section']

            classQuery = """ SELECT ROLL_NUMBER, FIRST_NAME, MIDDLE_NAME, LAST_NAME, DOB, STUDENT_CLASS, STUDENT_SECTION 
                FROM STUDENT_INFO
                WHERE  STUDENT_CLASS = \'%s\'
                AND STUDENT_SECTION = \'%s\'; """ % (selClass, selSec)

            records = getRecords(conn[0], classQuery).fetchall()
            discDB = disconnect_database(conn[0])
            print discDB[0]

            return render_template('studentSearch.html', classes = allClasses, sections = allSections, records = records)

    return render_template('studentSearch.html', classes = allClasses, sections = allSections)


@app.route('/addStaff', methods=['GET', 'POST'])
def addStaff():

    conn = make_a_connection()

    lastIDNumQuery = 'SELECT TOP 1 STAFF_ID FROM STAFF_INFO ORDER BY STAFF_ID DESC;'

    lastIDNum = getRecords(conn[0], lastIDNumQuery).fetchall()
    newIDNum = int(lastIDNum[0][0]) + 1

    if request.method == 'POST':

        sname = request.form['staffname']
        dob = request.form['dob']
        doj = request.form['doj']
        gender = request.form['gender']
        pcont = request.form['mob-primary']
        scont = request.form['mob-secondary']
        email = request.form['email']
        addr = request.form['addr']
        sts = request.form['sts']

        # stafpic file
        stfPicFileObj = request.files['staff-pic']
        stfPicDestPath = app.config['UPLOAD_FOLDER_STAFF_PIC']        


        stafpicFilepath = uploadfile(newIDNum, stfPicFileObj, stfPicDestPath, ALLOWED_PIC_EXTNS)
        print stafpicFilepath[1]        

        staffInsertQuery = """INSERT INTO STAFF_INFO (STAFF_ID, STAFF_NAME, STAFF_GENDER, STAFF_DOB, STAFF_DOJ, STAFF_PRIMARY_CONT, STAFF_SECONDARY_CONT, STAFF_EMAIL, STAFF_ADDR, STAFF_STATUS, STAFF_PIC) VALUES \
            (\'%s\', \'%s\', \'%s\', \'%s\',\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\');""" \
                % (
                    newIDNum, 
                    sname.strip(), 
                    gender.strip(), 
                    dob.strip(), 
                    doj.strip(), 
                    pcont.strip(), 
                    scont.strip(), 
                    email.strip(), 
                    addr.strip(), 
                    sts.strip(),
                    stafpicFilepath[1].split('\\')[1]
                )

        print staffInsertQuery

        try:
            ins = insert_records(conn[0], staffInsertQuery)
            print ins

            conn[0].commit()
            print 'commit'

            disc = disconnect_database(conn[0])
            print disc[0]

            flash("Submitted Successfully!")

            return redirect(url_for('addStaff'))
                


        except Exception, e:
            print e
            discDB = disconnect_database(conn[0])
            print discDB[0]              
            flash("Submitted Successfully!")
            return redirect(url_for('addStaff'))
            




    return render_template('addStaff.html', gender=['Male', 'Female'],
        idNum = newIDNum)


@app.route('/studentSearch/getInfo/<string:rollnumber>', methods=['GET'])
def getStudentInfo(rollnumber):

    if request.method == 'GET':

        conn = make_a_connection()

        # Student Info Table
        userRecordsQuery = 'SELECT * FROM STUDENT_INFO WHERE ROLL_NUMBER=%d' % int(rollnumber)
        print userRecordsQuery
        keys = ['rollnum', 'fname', 'mname', 'lname', 'dob', 'doa', 'studpic', 'ppic', 'studclass', 'studsec', 'studsts', 'studgender']
        records = getRecords(conn[0], userRecordsQuery).fetchall()
        print records
        studentDict = dict(zip(keys, records[0]))
        print studentDict

        # Student Parent Table
        parRecordsQuery = 'SELECT * FROM STUDENT_PARENT WHERE ROLL_NUMBER=%d' % int(rollnumber)
        print parRecordsQuery
        pkeys = ['rollnum', 'fathername', 'mothername', 'fathoccp', 'mothoccup']
        precords = getRecords(conn[0], parRecordsQuery).fetchall()
        print precords
        pdict = dict(zip(pkeys, precords[0]))
        print pdict

        #student contact Table
        cntRecordsQuery = 'SELECT * FROM STUDENT_CONTACT WHERE ROLL_NUMBER=%d' % int(rollnumber)
        print cntRecordsQuery
        ckeys = ['rollnum', 'prim', 'sec', 'email']
        crecords = getRecords(conn[0], cntRecordsQuery).fetchall()
        print crecords
        cdict = dict(zip(ckeys, crecords[0]))
        print cdict

        # Student Address table
        addrRecordsQuery = 'SELECT * FROM STUDENT_ADDRESS WHERE ROLL_NUMBER=%d' % int(rollnumber)
        print addrRecordsQuery
        akeys = ['rollnum', 'studaddr']
        arecords = getRecords(conn[0], addrRecordsQuery).fetchall()
        print arecords
        adict = dict(zip(akeys, arecords[0]))
        print adict        

        discDB = disconnect_database(conn[0])
        print discDB[0]

        return render_template('studentInfo.html', studentDict=studentDict, parentDict=pdict, contDict=cdict, addDict=adict)


@app.route('/editStudentInfo/<string:rnum>', methods=['GET', 'POST'])
def editStudentInfo(rnum):

    conn = make_a_connection()

    # Get classes and section
    getClassesQuery = 'SELECT CLASSES FROM CLASS_INFO;'
    getSectionsQuery = 'SELECT SECTIONS FROM CLASS_INFO;'

    allClasses = getRecords(conn[0], getClassesQuery)
    allSections = getRecords(conn[0], getSectionsQuery)

    allClasses = [x for x in allClasses if x[0] is not None]
    allSections = [x for x in allSections if x[0] is not None]         

    if request.method == 'GET':       

        # Student Info Table
        userRecordsQuery = 'SELECT * FROM STUDENT_INFO WHERE ROLL_NUMBER=%d' % int(rnum)
        print userRecordsQuery
        keys = ['rollnum', 'fname', 'mname', 'lname', 'dob', 'doa', 'studpic', 'ppic', 'studclass', 'studsec', 'studsts', 'studgender']
        records = getRecords(conn[0], userRecordsQuery).fetchall()
        print records
        studentDict = dict(zip(keys, records[0]))
        print studentDict

        # Student Parent Table
        parRecordsQuery = 'SELECT * FROM STUDENT_PARENT WHERE ROLL_NUMBER=%d' % int(rnum)
        print parRecordsQuery
        pkeys = ['rollnum', 'fathername', 'mothername', 'fathoccp', 'mothoccup']
        precords = getRecords(conn[0], parRecordsQuery).fetchall()
        print precords
        pdict = dict(zip(pkeys, precords[0]))
        print pdict

        #student contact Table
        cntRecordsQuery = 'SELECT * FROM STUDENT_CONTACT WHERE ROLL_NUMBER=%d' % int(rnum)
        print cntRecordsQuery
        ckeys = ['rollnum', 'prim', 'sec', 'email']
        crecords = getRecords(conn[0], cntRecordsQuery).fetchall()
        print crecords
        cdict = dict(zip(ckeys, crecords[0]))
        print cdict

        # Student Address table
        addrRecordsQuery = 'SELECT * FROM STUDENT_ADDRESS WHERE ROLL_NUMBER=%d' % int(rnum)
        print addrRecordsQuery
        akeys = ['rollnum', 'studaddr']
        arecords = getRecords(conn[0], addrRecordsQuery).fetchall()
        print arecords
        adict = dict(zip(akeys, arecords[0]))
        print adict        

        discDB = disconnect_database(conn[0])
        print discDB[0]

        return render_template('editStudentInfo.html', rnum=rnum, 
            allClasses=allClasses, allSections=allSections,
            studentDict=studentDict, parentDict=pdict, 
            contDict=cdict, addDict=adict,
            gender=['Male', 'Female'])


    elif request.method == 'POST':

        print '1'
        # roll number

        rnum = rnum

        # student info

        fname = request.form['fname']
        mname = request.form['mname']
        lname = request.form['lname']

        print '2'

        sgender = request.form['sgender']
        dob = request.form['dob']

        print '3'

        sclass = request.form['class-selected']
        ssection = request.form['section-selected']

        print '4'

        status = request.form['status']
        doa = request.form['doa']

        print '5'
        spic = request.files['student-pic'].filename
        # print spic

        print '6'

        # spic file
        spicFileObj = request.files['student-pic']
        print spicFileObj.filename
        spicDestPath = app.config['UPLOAD_FOLDER_STUDENT_PIC']

        # ppic file
        ppicFileObj = request.files['parent-pic']
        ppicDestPath = app.config['UPLOAD_FOLDER_PARENT_PIC']        

        # parents info

        fcname = request.form['fcname']
        foccup = request.form['foccup']

        print '7'

        mcname = request.form['mcname']
        moccup = request.form['moccup']

        print '8'

        mobPrim = request.form['mob-primary']
        mobSec = request.form['mob-secondary']

        print '9'

        email = request.form['email']
        addr = request.form['comp-addr']

        print '10'

        allUpds = []


        try:

            if spicFileObj.filename != "":
                spicFilepath = uploadfile(rnum, spicFileObj, spicDestPath, ALLOWED_PIC_EXTNS)
                print spicFilepath[1]

                updStudPicQuery = """ UPDATE STUDENT_INFO SET STUDENT_PICTURE = \'%s\' WHERE ROLL_NUMBER = %d""" \
                    % (
                    spicFilepath[1].split('\\')[1],
                    int(rnum)
                    )

                updSPic = update_records(conn[0], updStudPicQuery)
                

            if ppicFileObj.filename != "":
                ppicFilepath = uploadfile(rnum, ppicFileObj, ppicDestPath, ALLOWED_PIC_EXTNS)
                print ppicFilepath[1]            

                updParPicQuery = """ UPDATE STUDENT_INFO SET PARENT_PICTURE = \'%s\' WHERE ROLL_NUMBER = %d""" \
                    % (
                    ppicFilepath[1].split('\\')[1],
                    int(rnum)
                    )

                updPPic = update_records(conn[0], updParPicQuery)


            # student records Insert

            updQuery = \
                """UPDATE STUDENT_INFO SET FIRST_NAME = \'%s\', MIDDLE_NAME = \'%s\', LAST_NAME = \'%s\', DOB = \'%s\', DOA = \'%s\', STUDENT_CLASS = \'%s\', STUDENT_SECTION = \'%s\', STUDENT_STATUS = \'%s\', GENDER = \'%s\' WHERE  ROLL_NUMBER = %d;""" \
                % (
                fname.strip(),
                mname.strip(),
                lname.strip(),
                dob,
                doa,
                # spicFilepath[1].split('\\')[1],
                # ppicFilepath[1].split('\\')[1],
                sclass.strip(),
                ssection.strip(),
                status.strip(),
                sgender.strip(),
                int(rnum)
                )

            print  updQuery
            updRecds = update_records(conn[0], updQuery)
            print updRecds

            if updRecds == 0:
                allUpds.append(1)
                
            # Parents records Insert
            pUpdQuery = \
                """ UPDATE STUDENT_PARENT SET FATHER_NAME = \'%s\', MOTHER_NAME = \'%s\', FATHER_OCCUPATION = \'%s\', MOTHER_OCCUPATION = \'%s\' WHERE ROLL_NUMBER = %d; """ \
                % (
                fcname.strip(),
                mcname.strip(),
                foccup.strip(),
                moccup.strip(),
                int(rnum)
                )

            print  pUpdQuery
            pUpdRecds = update_records(conn[0], pUpdQuery)
            print pUpdRecds

            if pUpdRecds == 0:
                allUpds.append(1)


            # Address insert
            addrUpdQuery = \
                """ UPDATE STUDENT_ADDRESS SET STUDENT_ADDRESS = \'%s\' WHERE ROLL_NUMBER = %d; """ \
                % (
                addr.strip(),
                int(rnum)
                )

            print  addrUpdQuery
            addrUpdRecds = update_records(conn[0], addrUpdQuery)
            print addrUpdRecds  

            if addrUpdRecds == 0:
                allUpds.append(1)

            # Contact Info insert
            cntUpdQuery = \
                """ UPDATE STUDENT_CONTACT SET PRIMARY_MOB = \'%s\', SECONDARY_MOB = \'%s\', EMAIL = \'%s\' WHERE ROLL_NUMBER = %d; """ \
                % (
                mobPrim.strip(),
                mobSec.strip(),
                email.strip(),
                int(rnum)
                )

            print  cntUpdQuery
            cntUpdRecds = update_records(conn[0], cntUpdQuery)
            print cntUpdRecds

            if cntUpdRecds == 0:
                allUpds.append(1)

        except Exception, e:

            print e
        

        # check if all insert were successfull, then commit
        if sum(allUpds) == 4:
            conn[0].commit()
            print 'commit'

            flash('Saved Successfully!!')
            discDB = disconnect_database(conn[0])
            print discDB[0]        
            

        else:

            flash('Error in updating records. Please try again!!')
            discDB = disconnect_database(conn[0])
            print discDB[0]                   


        return redirect(url_for('getStudentInfo', rollnumber=rnum))


@app.route('/sendNotice')
def sendNotice():

    conn = make_a_connection()
    print conn

    # Get classes and section
    getClassesQuery = 'SELECT CLASSES FROM CLASS_INFO;'
    
    allClasses = getRecords(conn[0], getClassesQuery).fetchall()
    allClasses = [x for x in allClasses if x[0] is not None]
    
    discDB = disconnect_database(conn[0])
    print discDB

    return render_template('sendNotice.html', classes=allClasses)


@app.route('/sendNotice/getStudentList', methods=['GET', 'POST'])
def getStudentList():

    conn = make_a_connection()
    print conn    

    if request.method == 'POST':

        allClases = request.json['classes']

        studentsDict = dict()

        for classes in allClases:

            print classes

            try:
                getInfoQuery = """SELECT si.ROLL_NUMBER, si.FIRST_NAME, si.MIDDLE_NAME, si.LAST_NAME, si.STUDENT_CLASS, SI.GENDER, sc.PRIMARY_MOB FROM \
                STUDENT_INFO AS si INNER JOIN STUDENT_CONTACT AS sc ON (si.ROLL_NUMBER = sc.ROLL_NUMBER AND si.STUDENT_STATUS = 'ACTIVE' AND si.STUDENT_CLASS = \'%s\');""" % classes

                print getInfoQuery

                getInfoRecords = getRecords(conn[0], getInfoQuery).fetchall()
                print type(getInfoRecords[0])

                getInfoRecordsArr = [list(x) for x in getInfoRecords]

                print type(getInfoRecordsArr[0])

                studentsDict[classes] = getInfoRecordsArr


            except Exception, e:

                print e


        discDB = disconnect_database(conn[0])
        print discDB        

        print studentsDict
        return json.dumps(studentsDict)


@app.route('/sendNotice/getFacultyList', methods=['GET', 'POST'])
def getFacultyList():

    conn = make_a_connection()
    print conn    

    if request.method == 'POST':

        groups = request.json['group']

        groupDict = dict()

        for group in groups:

            print group

            try:
                getInfoQuery = """ SELECT STAFF_ID, STAFF_NAME, STAFF_GENDER, STAFF_PRIMARY_CONT FROM STAFF_INFO WHERE STAFF_STATUS = 'ACTIVE'; """

                print getInfoQuery

                getInfoRecords = getRecords(conn[0], getInfoQuery).fetchall()
                print type(getInfoRecords[0])

                getInfoRecordsArr = [list(x) for x in getInfoRecords]

                print type(getInfoRecordsArr[0])

                groupDict[group] = getInfoRecordsArr


            except Exception, e:

                print e


        discDB = disconnect_database(conn[0])
        print discDB        

        print groupDict
        return json.dumps(groupDict)



@app.route('/sendNotice/sendTextAll', methods=['GET', 'POST'])
def sendTextAll():

    if request.method == 'POST':

        msg = request.json['msg']
        nmbr = "91%s" % request.json['number']

        resp = sendSMS('mohdejazsiddiqui@gmail.com', '74aa54055b30ad864d6e3fe04d69987204d91c1378cabcd6e3ca47a034d6744f', 
                str(nmbr).strip(), 'TXTLCL', msg, 'true')

        print resp

        respDict = json.loads(resp)
        print type(respDict)

        if 'errors' in respDict:

            errMsg = "%s - %s" % (respDict['status'], respDict['errors'][0]['message'])

            return json.dumps(errMsg)
        else:

            return json.dumps(respDict['status'])

    

@app.route('/staffSearch', methods=['GET', 'POST'])
def staffSearch():

    return render_template('staffSearch.html')





if __name__ == '__main__':
    app.secret_key = '123432'
    app.debug = True
    app.run(host='0.0.0.0', port=1000, threaded=True)


            