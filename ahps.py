#!/usr/bin/python# -*- coding: utf-8 -*-from flask import Flask, render_template, url_for, request, redirect, flashfrom dblib import make_a_connection, insert_records, \    disconnect_database, copy_files, get_last_rollnumber, getRecordsapp = Flask(__name__)@app.route('/')@app.route('/index')def index():    return render_template('index.html')@app.route('/newAdmission', methods=['GET', 'POST'])def newAdmission():    conn = make_a_connection()    getClassesQuery = 'SELECT CLASSES FROM CLASS_INFO;'    getSectionsQuery = 'SELECT SECTIONS FROM CLASS_INFO;'    allClasses = getRecords(conn[0], getClassesQuery)    allSections = getRecords(conn[0], getSectionsQuery)    allClasses = [x for x in allClasses if x[0] is not None]    allSections = [x for x in allSections if x[0] is not None]        if request.method == 'POST':        # roll number        rnum = request.form['rnum']        # student info        fname = request.form['fname']        mname = request.form['mname']        lname = request.form['lname']        sgender = request.form['sgender']        dob = request.form['dob']        sclass = request.form['class-selected']        ssection = request.form['section-selected']        status = request.form['status']        doa = request.form['doa']        spic = request.form['student-pic']        # parents info        fcname = request.form['fcname']        foccup = request.form['foccup']        mcname = request.form['mcname']        moccup = request.form['moccup']        mobPrim = request.form['mob-primary']        mobSec = request.form['mob-secondary']        email = request.form['email']        addr = request.form['comp-addr']        try:            insQuery = \                """INSERT INTO STUDENT_INFO (ROLL_NUMBER, FIRST_NAME, MIDDLE_NAME, LAST_NAME, DOB, DOA, \                    STUDENT_PICTURE, STUDENT_CLASS, STUDENT_SECTION, STUDENT_STATUS, GENDER) VALUES \                    (%d, \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\');""" \                % (                int(rnum),                fname.strip(),                mname.strip(),                lname.strip(),                dob,                doa,                spic,                sclass.strip(),                ssection.strip(),                status.strip(),                sgender.strip(),                )            print  insQuery            insRecds = insert_records(conn[0], insQuery)            print insRecds            pInsQuery = \                """ INSERT INTO STUDENT_PARENT (ROLL_NUMBER, FATHER_NAME, MOTHER_NAME, FATHER_OCCUPATION, MOTHER_OCCUPATION) VALUES \                    (%d, \'%s\', \'%s\', \'%s\', \'%s\'); """ \                % (                int(rnum),                fcname.strip(),                mcname.strip(),                foccup.strip(),                moccup.strip()                )            print  pInsQuery            pinsRecds = insert_records(conn[0], pInsQuery)            print pinsRecds            addrInsQuery = \                """ INSERT INTO STUDENT_ADDRESS (ROLL_NUMBER, STUDENT_ADDRESS) VALUES \                    (%d, \'%s\'); """ \                % (                int(rnum),                addr.strip()                )            print  addrInsQuery            addrinsRecds = insert_records(conn[0], addrInsQuery)            print addrinsRecds                    cntInsQuery = \                """ INSERT INTO STUDENT_CONTACT (ROLL_NUMBER, PRIMARY_MOB, SECONDARY_MOB, EMAIL) VALUES \                    (%d, \'%s\', \'%s\', \'%s\'); """ \                % (                int(rnum),                mobPrim.strip(),                mobSec.strip(),                email.strip()                )            print  cntInsQuery            cntinsRecds = insert_records(conn[0], cntInsQuery)            print cntinsRecds            conn[0].commit()            print 'commit'            discDB = disconnect_database(conn[0])            print discDB[0]        except Exception, e:            print e                flash('Submission Successful!!')        return redirect(url_for('newAdmission'))    else:        return render_template('newAdmission.html', classes=allClasses,                               sections=allSections, gender=['Male',                               'Female'])@app.route('/studentSearch', methods=['GET', 'POST'])def studentSearch():        conn = make_a_connection()    getClassesQuery = 'SELECT CLASSES FROM CLASS_INFO;'    getSectionsQuery = 'SELECT SECTIONS FROM CLASS_INFO;'    allClasses = getRecords(conn[0], getClassesQuery)    allSections = getRecords(conn[0], getSectionsQuery)    allClasses = [x for x in allClasses if x[0] is not None]    allSections = [x for x in allSections if x[0] is not None]                 if request.method == 'POST':           if request.form['rnum'] != "":            rnum = request.form['rnum']            # query by roll number            rnumQuery = 'SELECT ROLL_NUMBER, FIRST_NAME, MIDDLE_NAME, LAST_NAME, DOB, STUDENT_CLASS, STUDENT_SECTION FROM STUDENT_INFO WHERE ROLL_NUMBER=%d;' % int(rnum)                        print rnumQuery                        records = getRecords(conn[0], rnumQuery)            print records            return render_template('studentSearch.html', classes = allClasses, sections = allSections, records = records)        elif (request.form['fname'] != "" or request.form['mname'] != "" or request.form['lname'] != ""):            fname = request.form['fname']            mname = request.form['mname']            lname = request.form['lname']            if (fname != "" and mname != "" and lname != ""):                nameQuery = """ SELECT ROLL_NUMBER, FIRST_NAME, MIDDLE_NAME, LAST_NAME, DOB, STUDENT_CLASS, STUDENT_SECTION                 FROM STUDENT_INFO                 WHERE FIRST_NAME=\'%s\'                AND MIDDLE_NAME=\'%s\'                AND LAST_NAME=\'%s\'; """ % (fname, mname, lname)                print nameQuery            elif (fname != "" and mname != "" and lname == ""):                nameQuery = """ SELECT ROLL_NUMBER, FIRST_NAME, MIDDLE_NAME, LAST_NAME, DOB, STUDENT_CLASS, STUDENT_SECTION                 FROM STUDENT_INFO                 WHERE FIRST_NAME=\'%s\'                AND MIDDLE_NAME=\'%s\'; """ % (fname, mname)                print nameQuery                        elif (mname != "" and lname != "" and fname == ""):                nameQuery = """ SELECT ROLL_NUMBER, FIRST_NAME, MIDDLE_NAME, LAST_NAME, DOB, STUDENT_CLASS, STUDENT_SECTION                 FROM STUDENT_INFO                 WHERE MIDDLE_NAME=\'%s\'                AND LAST_NAME=\'%s\'; """ % (mname, lname)                print nameQuery            elif (fname != "" and lname != "" and mname == ""):                nameQuery = """ SELECT ROLL_NUMBER, FIRST_NAME, MIDDLE_NAME, LAST_NAME, DOB, STUDENT_CLASS, STUDENT_SECTION                 FROM STUDENT_INFO                 WHERE FIRST_NAME=\'%s\'                AND LAST_NAME=\'%s\'; """ % (fname, lname)                print nameQuery                        elif (fname == "" and mname == ""  and lname != ""):                nameQuery = """ SELECT ROLL_NUMBER, FIRST_NAME, MIDDLE_NAME, LAST_NAME, DOB, STUDENT_CLASS, STUDENT_SECTION                 FROM STUDENT_INFO                 WHERE LAST_NAME=\'%s\'; """ % (lname, )                print nameQuery                        elif (mname == "" and lname == "" and fname != ""):                nameQuery = """ SELECT ROLL_NUMBER, FIRST_NAME, MIDDLE_NAME, LAST_NAME, DOB, STUDENT_CLASS, STUDENT_SECTION                 FROM STUDENT_INFO                 WHERE FIRST_NAME=\'%s\'; """ % (fname, )                print nameQuery                        elif (lname == "" and fname == "" and mname != ""):                nameQuery = """ SELECT ROLL_NUMBER, FIRST_NAME, MIDDLE_NAME, LAST_NAME, DOB, STUDENT_CLASS, STUDENT_SECTION                 FROM STUDENT_INFO                 WHERE MIDDLE_NAME=\'%s\'; """ % (mname, )                print nameQuery                  records = getRecords(conn[0], nameQuery).fetchall()            discDB = disconnect_database(conn[0])            print discDB[0]            return render_template('studentSearch.html', classes = allClasses, sections = allSections, records = records)        else:            selClass = request.form['class']            selSec = request.form['section']            classQuery = """ SELECT ROLL_NUMBER, FIRST_NAME, MIDDLE_NAME, LAST_NAME, DOB, STUDENT_CLASS, STUDENT_SECTION                 FROM STUDENT_INFO                WHERE  STUDENT_CLASS = \'%s\'                AND STUDENT_SECTION = \'%s\'; """ % (selClass, selSec)            records = getRecords(conn[0], classQuery).fetchall()            discDB = disconnect_database(conn[0])            print discDB[0]            return render_template('studentSearch.html', classes = allClasses, sections = allSections, records = records)    return render_template('studentSearch.html', classes = allClasses, sections = allSections)@app.route('/staffInfo')def staffInfo():    return render_template('staffInfo.html', gender=['Male', 'Female'])@app.route('/studentSearch/getInfo/<string:rollnumber>', methods=['GET'])def getStudentInfo(rollnumber):    if request.method == 'GET':        conn = make_a_connection()        # Student Info Table        userRecordsQuery = 'SELECT * FROM STUDENT_INFO WHERE ROLL_NUMBER=%d' % int(rollnumber)        print userRecordsQuery        keys = ['rollnum', 'fname', 'mname', 'lname', 'dob', 'doa', 'studpic', 'studclass', 'studsec', 'studsts', 'studgender']        records = getRecords(conn[0], userRecordsQuery).fetchall()        print records        studentDict = dict(zip(keys, records[0]))        print studentDict        # Student Parent Table        parRecordsQuery = 'SELECT * FROM STUDENT_PARENT WHERE ROLL_NUMBER=%d' % int(rollnumber)        print parRecordsQuery        pkeys = ['rollnum', 'fathername', 'mothername', 'fathoccp', 'mothoccup']        precords = getRecords(conn[0], parRecordsQuery).fetchall()        print precords        pdict = dict(zip(pkeys, precords[0]))        print pdict        #student contact Table        cntRecordsQuery = 'SELECT * FROM STUDENT_CONTACT WHERE ROLL_NUMBER=%d' % int(rollnumber)        print cntRecordsQuery        ckeys = ['rollnum', 'prim', 'sec', 'email']        crecords = getRecords(conn[0], cntRecordsQuery).fetchall()        print crecords        cdict = dict(zip(ckeys, crecords[0]))        print cdict        # Student Address table        addrRecordsQuery = 'SELECT * FROM STUDENT_ADDRESS WHERE ROLL_NUMBER=%d' % int(rollnumber)        print addrRecordsQuery        akeys = ['rollnum', 'studaddr']        arecords = getRecords(conn[0], addrRecordsQuery).fetchall()        print arecords        adict = dict(zip(akeys, arecords[0]))        print adict                discDB = disconnect_database(conn[0])        print discDB[0]        return render_template('studentInfo.html', studentDict=studentDict, parentDict=pdict, contDict=cdict, addDict=adict)if __name__ == '__main__':    app.secret_key = '123432'    app.debug = True    app.run(port=1000)            