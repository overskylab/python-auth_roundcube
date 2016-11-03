#!/usr/bin/python
from datetime import datetime, timedelta
import random, string, os


class Generate:
    def __init__(self):
        self.title = 'This class to generate password as your need'

    def password(self, length=6, special=0):
        if special == 1:
            chars = string.ascii_letters + string.digits + '!@#$%^&*()'
        else:
            chars = string.ascii_letters + string.digits
        random.seed = (os.urandom(1024))
        password = ''.join(random.choice(chars) for i in range(length))
        return password


class vb_script:
    user_list = []
    
    def __init__(self):
        self.title = 'This class to generate excel vb script'
        self.code = ''

    def add_user(self, username, password):
        credential = {'username': username, 'password': password}
        self.user_list.append(credential)

    def gen_script(self, priviledge):
        code = \
'''
Private Sub Workbook_Open()
    Dim Edate As Date
'''

        if priviledge == 1:
            # For postmaster
            time_result = datetime.now() + timedelta(days=+7)
        else:
            # For user
            time_result = datetime.now() + timedelta(days=+5)
        time_result = time_result.strftime("%d/%m")
        
        code += '    Edate = Format("'+time_result+'", "DD/MM")'

        code += \
'''
    If Date > Edate Then
        MsgBox ("This worksheet was valid upto " & Format(Edate, "dd-mmm") & " and will be closed")
        ActiveWorkbook.Close savechanges:=False
    End If
    If Edate - Date < 30 Then
    MsgBox ("This worksheet expires on " & Format(Edate, "dd-mmm") & " You have " & Edate - Date & " Days left ")
'''
        for i in range (len(self.user_list)):
            code += '    Range("B'+str(i+3)+'").value = "'+self.user_list[i]['username']+'"'+"\n"
            code += '    Range("C'+str(i+3)+'").value = "'+self.user_list[i]['password']+'"'+"\n"

        code += \
'''
    End If
End Sub
'''
        return code



#test = vb_script()
#test.add_user('user1','pass1')
#test.add_user('user2','pass2')
#print test.user_list
#priviledge = 0
#test.gen_script(priviledge)
#print test.code

#test = password()
#print test.generate(6)
