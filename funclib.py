
import os
from werkzeug.utils import secure_filename

def uploadfile(rollNumber, fileObj, destPath, extns):

    """ Upload file and allowed extensions """

    # Check if the file extension is Allowed
    myAllowedFile = fileObj.filename.rsplit('.', 1)[1] in extns

    print myAllowedFile
    print fileObj

    if fileObj and myAllowedFile:

        # filename to be saved with
        saveFilename = ".".join([str(rollNumber), str(fileObj.filename.rsplit('.', 1)[1])])
        print saveFilename

        try:

            filepath = os.path.join(destPath, saveFilename)
            fileObj.save(filepath)

            print "uploaded"

            return [0, filepath]

        except Exception, e:
            
            return[1, e]
    else:
        return [1, 'File extension not allowed!!']