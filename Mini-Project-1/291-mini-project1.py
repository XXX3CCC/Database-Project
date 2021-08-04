from tkinter import *
import sqlite3
import tkinter.messagebox as messagebox
import datetime
import random
import sys


connection = None
cursor = None
dbPath = str(sys.argv[1])
#print(sys.argv[1])
post_id = None


class LogIn:
    #Login Window
    def __init__(self, master):
        self.root = master
        self.root.title('Login Screen')
        self.root.geometry('500x300+10+15')
        self.uid = StringVar()
        self.pwd = StringVar()
        self.window = Frame(self.root)
        self.create_window()
 
 
    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        Label(self.window, text = 'USER ID:').grid(row = 2, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.uid).grid(row = 2, column = 1, sticky = E)
        Label(self.window, text = 'PASSWORD:').grid(row = 3, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.pwd, show = '*').grid(row = 3, column = 1, sticky = E)
        Button(self.window, text='SIGN IN', width = 8, command = self.sign_in).grid(row = 4, column = 1, sticky = W, pady = 10)
        Button(self.window, text='SIGN UP', width = 8, command = self.sign_up).grid(row = 5, column = 1, sticky = W, pady = 10)
        self.window.pack()


    def sign_in(self):
        query = "SELECT uid, pwd FROM users WHERE LOWER(uid) = ?;"
        val = [self.uid.get().lower()]
        cursor.execute(query, val)
        c = cursor.fetchall()
        if len(c) == 0:
            messagebox.showerror('ERROR!', 'The user does not exist!')
        elif c[0][0].isalnum() == False or c[0][1].isalnum() == False or len(c[0][0]) != 4:
            messagebox.showerror('ERROR!', 'Invalid user!')
        else:
            us, pw = c[0]
            if us.lower() == self.uid.get().lower() and pw == self.pwd.get():
                user_id = self.uid.get().lower()
                self.window.destroy()
                SignIn(self.uid.get().lower(), self.root)
            else:
                messagebox.showwarning('ERROR!', 'The password is wrong!')


    def sign_up(self):
        self.window.destroy()
        SignUp(self.root)
 
 

class SignUp:
    #Register Window
    def __init__(self, master=None):
        self.root = master
        self.root.title('Sign Up')
        self.root.geometry('500x300')
        self.uid = StringVar()
        self.name = StringVar()
        self.city = StringVar()
        self.pwd = StringVar()
        self.window = Frame(self.root)
        self.create_window()


    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        Label(self.window, text = 'USER ID:').grid(row = 2, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.uid).grid(row = 2, column = 1, sticky = E)
        Label(self.window, text = 'USER NAME:').grid(row = 3, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.name).grid(row = 3, column = 1, sticky = E)
        Label(self.window, text = 'CITY:').grid(row = 4, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.city).grid(row = 4, column = 1, sticky = E)
        Label(self.window, text = 'PASSWORD:').grid(row = 5, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.pwd).grid(row = 5, column = 1, sticky = E)
        Button(self.window, text='SIGN IN', width = 8, command = self.sign_in).grid(row=6, column = 1, sticky=W, pady=10)
        Button(self.window, text = 'BACK', width = 8, command = self.back).grid(row = 7, column = 1, sticky = W, pady = 10)
        self.window.pack()


    def sign_in(self):
        if len(self.uid.get()) == 0 or len(self.name.get()) == 0 or len(self.city.get()) == 0 or len(self.pwd.get()) == 0:
            messagebox.showerror('ERROR!', 'The input can not be empty!')
        elif len(self.uid.get()) != 4:
            messagebox.showerror('ERROR!', 'The user id must be four characters!')
        elif self.pwd.get().isalnum() == False or self.uid.get().isalnum() == False:
            messagebox.showerror('ERROR!', 'The user id and password will only contain alphanumeric characters!')
        else:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            query = 'INSERT INTO users VALUES (?,?,?,?,?);'
            val = [self.uid.get().lower(), self.name.get().lower(), self.city.get().lower(), date, self.pwd.get()]
            try:
                cursor.execute(query, val)
                self.window.destroy()
                SignIn(self.uid.get().lower(), self.root)
            except sqlite3.IntegrityError:
                messagebox.showerror('ERROR!', 'The user already exists!')


    def back(self):
        self.window.destroy()
        LogIn(self.root)
 


class SignIn:
    #Sign In Window
    def __init__(self, uid, master=None):
        self.root = master
        self.root.title('Welcome!')
        self.root.geometry('500x300')
        self.window = Frame(self.root)
        self.uid = uid
        self.create_window()


    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        self.diff_user()
        self.window.pack()
        
        
    def quit(self):
        self.window.destroy()
 
 
    def log_out(self):
        self.window.destroy()
        LogIn(self.root)
 
 
    def post_q(self):
        self.window.destroy()
        PostQ(self.uid, self.root)       


    def search(self):
        self.window.destroy()
        Search(self.uid, self.root)


    def diff_user(self):
        cursor.execute("SELECT r.uid FROM privileged r;")
        users = cursor.fetchall()
        uid_list = []
        for i in range(len(users)):
            uid_list.append(users[i][0].lower())
        if self.uid in uid_list:
            Button(self.window, text = 'POST QUESTION', width = 20, command = self.post_q).grid(row = 1, column = 1, sticky = W, pady = 10)
            Button(self.window, text = 'SEARCH', width = 20, command = self.search).grid(row = 2, column = 1, sticky = W, pady = 10)
            Button(self.window, text = 'GIVE BADGE', width = 20, command = self.give).grid(row = 3, column = 1, sticky = W, pady = 10)
            Button(self.window, text = 'LOG OUT', width = 20, command = self.log_out).grid(row = 4, column = 1, sticky = W, pady = 10)
            #Button(self.window, text = 'QUIT', width = 20, command = self.root.quit).grid(row = 5, column = 1, sticky = W, pady = 10)            
        else:
            Button(self.window, text = 'POST QUESTION', width = 20, command = self.post_q).grid(row = 1, column = 1, sticky = W, pady = 10)
            Button(self.window, text = 'SEARCH', width = 20, command = self.search).grid(row = 2, column = 1, sticky = W, pady = 10)
            Button(self.window, text = 'LOG OUT', width = 20, command = self.log_out).grid(row = 3, column = 1, sticky = W, pady = 10)
            #Button(self.window, text = 'QUIT', width = 20, command = self.root.quit).grid(row = 4, column = 1, sticky = W, pady = 10)            
            
            
    def give(self):
        self.window.destroy()
        GiveB(self.uid, self.root)



class GiveB:
    def __init__(self, uid, master=None):
        self.root = master
        self.root.title('Choose one user and give badge')
        self.root.geometry('500x300')
        self.window = Frame(self.root)
        self.conn = sqlite3.connect(dbPath)
        self.uid = uid
        self.uname = StringVar()
        self.bname = StringVar()
        self.create_window()
        
        
    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        Label(self.window, text = 'USER ID:').grid(row = 2, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.uname).grid(row = 2, column = 1, sticky = E)
        Label(self.window, text = 'BADGE NAME:').grid(row = 3, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.bname).grid(row = 3, column = 1, sticky = E)
        Button(self.window, text='SELECT', width = 8, command = self.confirm).grid(row=4, column = 1, sticky=W, pady=10)
        Button(self.window, text = 'BACK', width = 8, command = self.back).grid(row = 5, column =1, sticky = W, pady = 10)    
        self.window.pack()
        
        
    def back(self):
        self.window.destroy()
        SignIn(self.uid, self.root)        
    
    
    def confirm(self):
        give_date = datetime.datetime.now().strftime('%Y-%m-%d')
        chosen_user = self.uname.get().lower()
        badge_name = self.bname.get().lower()
        cursor.execute("SELECT u.uid FROM users u;")
        total_user = cursor.fetchall()
        total_uid = []
        for i in range(len(total_user)):
            total_uid.append(total_user[i][0].lower())
        if len(chosen_user) == 0 or len(badge_name) == 0:
            messagebox.showerror('ERROR!', 'The input can not be empty!')
        elif chosen_user.lower() in total_uid:
            try:
                cursor.execute('INSERT INTO ubadges VALUES (?,?,?);',(chosen_user,give_date,badge_name,))       
                messagebox.showerror('Succeeded!', 'You have given a badge to user {}!'.format(chosen_user))
                self.window.destroy()
                SignIn(self.uid,self.root)
            except sqlite3.IntegrityError:
                messagebox.showerror('ERROR!', 'This user has had a badged today!')
        else:
            messagebox.showerror('ERROR!', 'The user does not exist!')




class PostQ:
    #Post A Question Window
    def __init__(self, uid, master=None):
        self.root = master
        self.root.title('Post A Question')
        self.root.geometry('500x300')
        self.window = Frame(self.root)
        self.title = StringVar()
        self.body = StringVar()
        self.uid = uid
        self.create_window()
        

    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        Label(self.window, text = 'TITLE:').grid(row = 2, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.title).grid(row = 2, column = 1, sticky = E)
        Label(self.window, text = 'TEXTS:').grid(row = 3, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.body).grid(row = 3, column = 1, sticky = E)
        Button(self.window, text='CONFIRM', width = 8, command = self.post).grid(row = 4, column = 1, sticky = W, pady = 10)
        Button(self.window, text='BACK', width = 8, command = self.back).grid(row = 5, column = 1, sticky = W, pady = 10)
        self.window.pack()


    def back(self):
        self.window.destroy()
        SignIn(self.uid, self.root)


    def post(self):
        if len(self.title.get()) == 0 or len(self.body.get()) == 0:
            messagebox.showerror('ERROR!', 'The input can not be empty!')
        else:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            query = "SELECT pid FROM posts;"
            cursor.execute(query)
            c = cursor.fetchall()
            number = len(c)
            post_id = 'p' + '{:03d}'.format(number + 1)
            query = 'INSERT INTO posts VALUES (?,?,?,?,?);'
            val = [post_id, date, self.title.get(), self.body.get(), self.uid]
            cursor.execute(query, val)
            
            query2 = 'INSERT INTO questions VALUES (?,?);'
            theaid = None
            val2 = [post_id, theaid]
            cursor.execute(query2, val2)            
            
            self.window.destroy()
            SignIn(self.uid, self.root)
        


class Search:
    #Search A Post Window
    def __init__(self, uid, master=None):
        self.root = master
        self.root.title('Search A Question')
        self.root.geometry('500x300')
        self.window = Frame(self.root)
        self.keyword = StringVar()
        self.create_window()
        self.uid = uid


    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        Label(self.window, text = 'KEYWORD:').grid(row = 2, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.keyword).grid(row = 2, column = 1, sticky = E)
        Button(self.window, text='SEARCH', width = 8, command = self.done).grid(row = 3, column = 1, sticky = W, pady = 10)
        Button(self.window, text='BACK', width = 8, command = self.back).grid(row = 4, column = 1, sticky = W, pady = 10)
        self.window.pack()


    def back(self):
        self.window.destroy()
        SignIn(self.uid, self.root)
    
    
    def done(self):
        result_list = []
        pid_list = []
        return_list = []
        inp = self.keyword.get()
        keywords = inp.split(',')
        n = len(keywords)
        if len(inp) == 0:
                messagebox.showerror('ERROR!', 'The input can not be empty!')
        else:
            for i in range(len(keywords)):
                keyword = keywords[i]
                query = "SELECT p.pid FROM posts p WHERE p.title like '%'||?||'%' UNION SELECT p.pid FROM posts p WHERE p.body like '%'||?||'%' UNION SELECT p.pid FROM posts p, tags t WHERE t.pid = p.pid AND t.tag like '%'||?||'%';"
                cursor.execute(query,(keyword,keyword,keyword))
                c = cursor.fetchall()
                for k in range(len(c)):
                    result_list.append(c[k][0])
            query2 = "SELECT p.pid FROM posts p;"
            cursor.execute(query2)
            c2 = cursor.fetchall()
            for j in range(len(c2)):
                pid_list.append(c2[j][0])
            while n > 0:
                for t in range(len(pid_list)):
                    num = result_list.count(pid_list[t])
                    if num == n:
                        return_list.append(pid_list[t])
                n -= 1         
        if len(return_list) == 0:
            messagebox.showerror('ERROR!', 'No match!')
        else:
            self.window.destroy()  
            ShowResult(self.uid, return_list, self.root)            



class ShowResult:
    def __init__(self, uid, return_list, master=None):
        self.root = master
        self.root.title('SHOW THE RESULT')
        self.root.geometry('800x500')
        self.window = Frame(self.root)
        self.return_list = return_list
        self.length_list = 0
        self.select = StringVar()
        self.uid = uid
        self.c = None
        self.create_window()


    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        q_list = []
        a_list = []
        total_q = '''SELECT p.pid
                     FROM posts p, questions q
                     WHERE p.pid = q.pid'''
        cursor.execute(total_q)
        q_all = cursor.fetchall()
        for m in range(len(q_all)):
            q_list.append(q_all[m])
        total_a = '''SELECT p.pid
                     FROM posts p, answers a
                     WHERE p.pid = a.pid'''
        cursor.execute(total_a)
        a_all = cursor.fetchall()
        for n in range(len(a_all)):
            a_list.append(a_all[n])

        if len(self.return_list) > 0 and len(self.return_list) < 5:
            for i in range(len(self.return_list)):
                query_q = '''SELECT p.pid, p.pdate, p.title, p.body, p.poster, IFNULL(vote_number, '0'), IFNULL(answer_number, '0')
                           FROM posts p left outer join (SELECT p.pid as pi, COUNT(*) as vote_number
                                                          FROM posts p, votes v 
                                                          WHERE v.pid = p.pid
                                                          GROUP BY p.pid) on p.pid = pi
                                         left outer join (SELECT p.pid as ppi, COUNT(*) as answer_number
                                                          FROM posts p, answers a 
                                                          WHERE p.pid = a.qid
                                                          GROUP BY p.pid) on p.pid = ppi
                           WHERE p.pid = ?;'''         
                query_a = '''SELECT p.pid, p.pdate, p.title, p.body, p.poster, IFNULL(vote_number, '0')
                           FROM posts p left outer join (SELECT p.pid as pi, COUNT(*) as vote_number
                                                          FROM posts p, votes v 
                                                          WHERE v.pid = p.pid
                                                          GROUP BY p.pid) on p.pid = pi
                           WHERE p.pid = ?;'''
                val = [self.return_list[i]]
                no_match = 'No Match!'
                for j in range(len(q_list)):
                    if val[0] == q_list[j][0]:
                        cursor.execute(query_q, val)
                for j in range(len(a_list)):
                    if val[0] == a_list[j][0]:
                        cursor.execute(query_a, val)
                c = cursor.fetchone()  
                Label(self.window, text = c).grid(row = 2+i, sticky = W) 
            del self.return_list[0:len(self.return_list)]
            self.length_list = 0
            
        else:
            for i in range(5):
                query_q = '''SELECT p.pid, p.pdate, p.title, p.body, p.poster, IFNULL(vote_number, '0'), IFNULL(answer_number, '0')
                           FROM posts p left outer join (SELECT p.pid as pi, COUNT(*) as vote_number
                                                          FROM posts p, votes v 
                                                          WHERE v.pid = p.pid
                                                          GROUP BY p.pid) on p.pid = pi
                                         left outer join (SELECT p.pid as ppi, COUNT(*) as answer_number
                                                          FROM posts p, answers a 
                                                          WHERE p.pid = a.qid
                                                          GROUP BY p.pid) on p.pid = ppi
                           WHERE p.pid = ?;'''         
                query_a = '''SELECT p.pid, p.pdate, p.title, p.body, p.poster, IFNULL(vote_number, '0')
                           FROM posts p left outer join (SELECT p.pid as pi, COUNT(*) as vote_number
                                                          FROM posts p, votes v 
                                                          WHERE v.pid = p.pid
                                                          GROUP BY p.pid) on p.pid = pi
                           WHERE p.pid = ?;'''
                val = [self.return_list[i]]
                for j in range(len(q_list)):
                    if val[0] == q_list[j][0]:
                        cursor.execute(query_q, val)
                for j in range(len(a_list)):
                    if val[0] == a_list[j][0]:
                        cursor.execute(query_a, val)
                c = cursor.fetchone() 
                Label(self.window, text = c).grid(row = 2+i, sticky = W)
            del self.return_list[0:5] 
            self.length_list = len(self.return_list)             
            
        Label(self.window, text = 'INPUT THE SELECT PID:').grid(row = 7, sticky = W, pady = 10)       
        Entry(self.window, textvariable = self.select).grid(row = 8, sticky = W, pady = 10)
        Button(self.window, text='SELECT', width = 15, command = self.selecttheitem).grid(row = 8, sticky = E, column = 1)
        Button(self.window, text='SEARCHMORE', width = 15, command = self.searchmore).grid(row = 9, sticky = W, pady = 10)
        Button(self.window, text='BACK', width = 8, command = self.back).grid(row = 10, sticky = W, pady = 10)
        self.window.pack()


    def back(self):
        self.window.destroy()
        Search(self.uid, self.root)


    def searchmore(self):
        if self.length_list == 0:
            messagebox.showerror('ERROR!', 'No more result!')
        else:
            self.window.destroy()
            ShowResult(self.uid, self.return_list, self.root)       


    def selecttheitem(self):
        if len(self.select.get()) == 0:
            messagebox.showerror('ERROR!', 'The input can not be empty!')
        else:
            query = "SELECT p.pid FROM posts p, questions q WHERE p.pid = q.pid AND p.pid = ?;"
            val = [self.select.get()]
            cursor.execute(query, val)
            c = cursor.fetchone()
            
            query2 = "SELECT p.pid FROM posts p, answers a WHERE p.pid = a.pid AND p.pid = ?;"
            val2 = [self.select.get()]
            cursor.execute(query2, val2)
            c2 = cursor.fetchone()                
            if c == None:
                self.c = c2
                self.window.destroy()
                PerformPostAction2(self.uid, self.c, self.root)    
            else:
                self.c = c
                self.window.destroy()
                PerformPostAction(self.uid, self.c, self.root)      



class PerformPostAction:
    #Post An Action-Answer Window
    def __init__(self, uid, c, master=None):
        self.root = master
        self.root.title('Perform A Post Action')
        self.root.geometry('500x400')
        self.window = Frame(self.root)
        self.title = StringVar()
        self.body = StringVar()
        self.uid = uid
        self.c = c
        self.create_window()


    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        self.diff_user()
        self.window.pack()    


    def back(self):
        self.window.destroy()
        Search(self.uid, self.root)
        
        
    def answer(self):
        self.window.destroy()
        InputActionA(self.uid, self.c, self.root)
        
      
    def vote(self):
        vote_date = datetime.datetime.now().strftime('%Y-%m-%d')
        query = "SELECT v.vno FROM votes v WHERE v.pid = (?);"
        val = [(self.c)[0]]
        cursor.execute(query, val)
        c = cursor.fetchall()
        number = len(c)
        vote_number = number + 1
        query = 'INSERT INTO votes VALUES (?,?,?,?);'
        post_id = (self.c)[0]
        val = [post_id, vote_number, vote_date, self.uid]
        cursor.execute(query, val)        
        self.window.destroy()
        Search(self.uid, self.root)  
        
        
    def diff_user(self):
        query = "SELECT r.uid FROM privileged r;"
        cursor.execute(query)
        users = cursor.fetchall()
        uid_list = []
        for i in range(len(users)):
            uid_list.append(users[i][0].lower())
        if self.uid in uid_list:
            Button(self.window, text='ANSWER IT', width = 10, command = self.answer).grid(row = 2, column = 1, sticky = W, pady = 10)
            Button(self.window, text='VOTE IT', width = 10, command = self.vote).grid(row = 3, column = 1, sticky = W, pady = 10)           
            Button(self.window, text='MARK', width = 10, command = self.show_answer).grid(row = 4, column = 1, sticky = W, pady = 10)
            Button(self.window, text = 'ADD TAG', width = 10, command = self.add_tag).grid(row = 5, column = 1, sticky = W, pady = 10)
            Button(self.window, text = 'EDIT', width = 10, command = self.edit_post).grid(row = 6, column = 1, sticky = W, pady = 10)
            Button(self.window, text='BACK', width = 10, command = self.back).grid(row = 7, column = 1, sticky = W, pady = 10) 
        else:
            Button(self.window, text='ANSWER IT', width = 10, command = self.answer).grid(row = 2, column = 1, sticky = W, pady = 10)
            Button(self.window, text='VOTE IT', width = 10, command = self.vote).grid(row = 3, column = 1, sticky = W, pady = 10)          
            Button(self.window, text='BACK', width = 10, command = self.back).grid(row = 4, column = 1, sticky = W, pady = 10)            
            
            
    def show_answer(self):
        self.window.destroy()
        Answers(self.uid, self.c, self.root)


    def add_tag(self):
        self.window.destroy()
        AddTag(self.uid, self.c, self.root)


    def edit_post(self):
        self.window.destroy()
        EditP(self.uid, self.c, self.root)



class PerformPostAction2:
    #Post An Action-Answer Window
    def __init__(self, uid, c, master=None):
        self.root = master
        self.root.title('Perform A Post Action')
        self.root.geometry('500x300')
        self.window = Frame(self.root)
        self.title = StringVar()
        self.body = StringVar()
        self.uid = uid
        self.c = c
        self.create_window()


    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        self.diff_user()
        self.window.pack()


    def back(self):
        self.window.destroy()
        Search(self.uid, self.root)
        
        
    def vote(self):
        vote_date = datetime.datetime.now().strftime('%Y-%m-%d')
        query = "SELECT v.vno FROM votes v WHERE v.pid = (?);"
        val = [(self.c)[0]]
        cursor.execute(query, val)
        c = cursor.fetchall()
        number = len(c)
        vote_number = number + 1
        query = 'INSERT INTO votes VALUES (?,?,?,?);'
        post_id = (self.c)[0]
        val = [post_id, vote_number, vote_date, self.uid]
        cursor.execute(query, val)        
        self.window.destroy()
        Search(self.uid, self.root)               


    def diff_user(self):
        query = "SELECT r.uid FROM privileged r;"
        cursor.execute(query)
        users = cursor.fetchall()
        uid_list = []
        for i in range(len(users)):
            uid_list.append(users[i][0].lower())
        if self.uid in uid_list:
            Button(self.window, text='VOTE IT', width = 10, command = self.vote).grid(row = 2, column = 1, sticky = W, pady = 10)           
            Button(self.window, text = 'ADD TAG', width = 10, command = self.add_tag).grid(row = 3, column = 1, sticky = W, pady = 10)
            Button(self.window, text = 'EDIT', width = 10, command = self.edit_post).grid(row = 4, column = 1, sticky = W, pady = 10)
            Button(self.window, text='BACK', width = 10, command = self.back).grid(row = 5, column = 1, sticky = W, pady = 10) 
        else:
            Button(self.window, text='VOTE IT', width = 10, command = self.vote).grid(row = 2, column = 1, sticky = W, pady = 10)          
            Button(self.window, text='BACK', width = 10, command = self.back).grid(row = 3, column = 1, sticky = W, pady = 10)            
            

    def add_tag(self):
        self.window.destroy()
        AddTag(self.uid, self.c, self.root)


    def edit_post(self):
        self.window.destroy()
        EditP(self.uid, self.c, self.root)
    


class Answers:
    def __init__(self, uid, c, master=None):
        self.root = master
        self.root.title('Here Are All Answers')
        self.root.geometry('800x600')
        self.window = Frame(self.root)
        self.select = StringVar()
        self.uid = uid
        self.c = c
        self.create_window()
        
        
    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        n = 0
        answers_list = []
        query = "SELECT a.pid FROM answers a WHERE a.qid = (?);"
        quesid = self.c[0]
        val = [quesid]
        cursor.execute(query,val)
        c = cursor.fetchall()
        for i in range(len(c)):
            answers_list.append(c[i][0])
        for j in range(len(answers_list)):
            query = '''SELECT p.pid, p.pdate, p.title, p.body, p.poster, IFNULL(vote_number, '0')
                       FROM posts p left outer join (SELECT p.pid as pi, COUNT(*) as vote_number
                                                          FROM posts p, votes v 
                                                          WHERE v.pid = p.pid
                                                          GROUP BY p.pid) on p.pid = pi
                       WHERE p.pid = ?;'''
                    
            val = [answers_list[j]]
            cursor.execute(query,val)
            c2 = cursor.fetchone() 
            Label(self.window, text = c2).grid(row = 2+j, sticky = W) 
            n += 1
            
        Label(self.window, text = 'INPUT THE SELECTED ANSWER:').grid(row = 2+n, sticky = W, pady = 10)       
        Entry(self.window, textvariable = self.select).grid(row = 3+n, sticky = W, pady = 10)        
        Button(self.window, text='SELECT', width = 10, command = self.confirm).grid(row = 3 + n, sticky = E, column = 0)
        Button(self.window, text='BACK', width = 10, command = self.back).grid(row = 4 + n, sticky = E, pady = 10)        
        self.window.pack()
        
        
    def back(self):
        self.window.destroy()
        PerformPostAction(self.uid, self.c, self.root)


    def confirm(self):
        quesid = self.c[0]
        cursor.execute('SELECT q.theaid FROM questions q WHERE q.pid = (?);',(quesid,))
        c = cursor.fetchone()
        if c[0] == None:
            cursor.execute("UPDATE questions SET theaid = (?);",(self.select.get(),))
            messagebox.showerror('Succeeded!', 'You have already set it as the accepted answer of question {}!'.format(self.c[0]))            
        else:
            self.window.destroy()
            Confirm(self.uid, self.c, self.select, self.root)
  
       

class Confirm:
    def __init__(self, uid, c, select, master=None):
        self.root = master
        self.root.title('Confirm your choose')
        self.root.geometry('800x600')
        self.window = Frame(self.root)
        self.select = select
        self.uid = uid
        self.c = c
        self.create_window() 
        
        
    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)        
        Label(self.window, text = 'Are You Sure You Want To Change The Accepted Answer?').grid(row = 2, sticky = W, pady = 10)
        Button(self.window, text='CONFIRM', width = 10, command = self.yes).grid(row = 3, column = 1, sticky = W, pady = 10)
        Button(self.window, text='BACK', width = 10, command = self.back).grid(row = 4, column = 1, sticky = W, pady = 10)
        self.window.pack()
        
        
    def yes(self):
        self.window.destroy()
        Compare(self.uid, self.c, self.select, self.root)


    def back(self):
        self.window.destroy()
        Answers(self.uid, self.c, self.root)
            
   
   
class Compare:
    def __init__(self, uid, c, select, master=None):
        self.root = master
        self.root.title('Compare the two potential accepted answers')
        self.root.geometry('800x600')
        self.window = Frame(self.root)
        self.select = select
        self.uid = uid
        self.c = c
        self.create_window()
        
        
    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)        
        Label(self.window, text = 'Here are the two potential accepted answers').grid(row = 2, sticky = W, pady = 10)
        Label(self.window, text = 'The original one:').grid(row = 3, sticky = W, pady = 10)
        self.original()
        Label(self.window, text = 'The new one:').grid(row = 5, sticky = W, pady = 10)
        self.new_choice()
        Button(self.window, text='KEEP PREVIOUS', width = 15, command = self.previous).grid(row = 7, column = 1, sticky = W, pady = 10)
        Button(self.window, text='CHANGE', width = 15, command = self.change).grid(row = 8, column = 1, sticky = W, pady = 10)
        Button(self.window, text='BACK', width = 15, command = self.back).grid(row = 9, column = 1, sticky = W, pady = 10)
        self.window.pack()
        
        
    def original(self):
        cursor.execute("SELECT q.theaid FROM questions q WHERE q.pid = (?);",(self.c[0],))
        result = cursor.fetchone()
        query2 = '''SELECT p.pid, p.pdate, p.title, p.body, p.poster, IFNULL(vote_number, '0')
                 FROM posts p left outer join (SELECT p.pid as pi, COUNT(*) as vote_number
                                                FROM posts p, votes v 
                                                WHERE v.pid = p.pid
                                                GROUP BY p.pid) on p.pid = pi
                 WHERE p.pid = ?;'''       
        val2 = [result[0]]
        cursor.execute(query2,val2)
        c2 = cursor.fetchall()
        Label(self.window, text = c2).grid(row = 4, sticky = W, pady = 10)
        
        
    def new_choice(self):
        query = '''SELECT p.pid, p.pdate, p.title, p.body, p.poster, IFNULL(vote_number, '0')
                FROM posts p left outer join (SELECT p.pid as pi, COUNT(*) as vote_number
                                               FROM posts p, votes v 
                                               WHERE v.pid = p.pid
                                               GROUP BY p.pid) on p.pid = pi
                WHERE p.pid = ?;'''
        val = [self.select.get()]
        cursor.execute(query,val)
        c = cursor.fetchall()
        Label(self.window, text = c).grid(row = 6, sticky = W, pady = 10)
        
        
    def previous(self):
        messagebox.showinfo('Notification', 'You keep your original choice.') 
    
    
    def change(self):
        cursor.execute("UPDATE questions SET theaid = (?);",(self.select.get(),))
        messagebox.showinfo('Succeeded!', 'You have changed the accepted answer of question {}'.format(self.c[0]))
        self.window.destroy()
        Answers(self.uid, self.c, self.root)
        
        
    def back(self):
        self.window.destroy()
        Confirm(self.uid, self.c, self.select, self.root)
             
        


class AddTag:
    def __init__(self, uid, c, master=None):
        self.root = master
        self.root.title('Add A Tag')
        self.root.geometry('500x300')
        self.window = Frame(self.root)
        self.uid = uid
        self.c = c
        self.ttext = StringVar()
        self.create_window()


    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        check = 'SELECT t.tag FROM tags t WHERE t.pid = ?;'
        val = [self.c[0]]
        cursor.execute(check, val)
        t_tag = cursor.fetchall()
        Label(self.window, text = 'Your tags: ').grid(row = 2, sticky = W)
        Label(self.window, text = t_tag).grid(row = 2, column = 1, sticky = E, pady = 10)
        Label(self.window, text = 'TAG:').grid(row = 3, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.ttext).grid(row = 3, column = 1, sticky = E)
        Button(self.window, text = 'CONFIRM', width = 8, command = self.add).grid(row = 4, column =1, sticky = W, pady = 10)
        Button(self.window, text = 'BACK', width = 8, command = self.back).grid(row = 5, column =1, sticky = W, pady = 10)
        self.window.pack()


    def add(self):
        if len(self.ttext.get()) == 0:
            messagebox.showerror('ERROR!', 'The input can not be empty!')
        else:
            query = 'INSERT INTO tags VALUES (?,?);'
            val = [self.c[0], self.ttext.get()]
            try:
                cursor.execute(query, val)
                messagebox.showinfo('Succeeded!', 'You add the tag successfully!')
                self.window.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror('ERROR!', 'The tag already exists!')
            
            query1 = "SELECT p.pid FROM posts p, questions q WHERE p.pid = q.pid AND p.pid = ?;"
            val1 = [self.c[0]]
            cursor.execute(query1, val1)
            c = cursor.fetchone()
            
            query2 = "SELECT p.pid FROM posts p, answers a WHERE p.pid = a.pid AND p.pid = ?;"
            val2 = [self.c[0]]
            cursor.execute(query2, val2)
            c2 = cursor.fetchone()                
            if c == None:
                self.c = c2
                self.window.destroy()
                PerformPostAction2(self.uid, self.c, self.root)    
            else:
                self.c = c
                self.window.destroy()
                PerformPostAction(self.uid, self.c, self.root)                


    def back(self):
        self.window.destroy()
        query = "SELECT p.pid FROM posts p, questions q WHERE p.pid = q.pid AND p.pid = ?;"
        val = [self.c[0]]
        cursor.execute(query, val)
        c = cursor.fetchone()
        
        query2 = "SELECT p.pid FROM posts p, answers a WHERE p.pid = a.pid AND p.pid = ?;"
        val2 = [self.c[0]]
        cursor.execute(query2, val2)
        c2 = cursor.fetchone()                
        if c == None:
            self.c = c2
            self.window.destroy()
            PerformPostAction2(self.uid, self.c, self.root)    
        else:
            self.c = c
            self.window.destroy()
            PerformPostAction(self.uid, self.c, self.root)              
        

class EditP:
    def __init__(self, uid, c, master=None):
        self.root = master
        self.root.title('Edit Post')
        self.root.geometry('500x300')
        self.window = Frame(self.root)
        self.uid = uid
        self.c = c
        self.ptitle = StringVar()
        self.pbody = StringVar()
        self.create_window()


    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        check = 'SELECT p.title, p.body FROM posts p WHERE p.pid = ?;'
        val = [self.c[0]]
        cursor.execute(check, val)
        old_post = cursor.fetchall()
        Label(self.window, text = 'Original post: ').grid(row = 2, sticky = W)
        Label(self.window, text = old_post).grid(row = 2, column = 1, sticky = E, pady = 10)
        Label(self.window, text = 'TITLE:').grid(row = 3, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.ptitle).grid(row = 3, column = 1, sticky = E)
        Label(self.window, text = 'TEXTS:').grid(row = 4, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.pbody).grid(row = 4, column = 1, sticky = E)
        Button(self.window, text='CONFIRM', width = 10, command = self.edit).grid(row = 5, column = 1, sticky = W, pady = 10)
        Button(self.window, text='BACK', width = 10, command = self.back).grid(row = 6, column = 1, sticky = W, pady = 10)
        self.window.pack()


    def edit(self):
        if len(self.ptitle.get()) == 0 or len(self.pbody.get()) == 0:
            messagebox.showerror('ERROR!', 'The input can not be empty!')
        else:
            cursor.execute("UPDATE posts SET title = (?) WHERE pid = ?;", (self.ptitle.get(), self.c[0]))
            cursor.execute("UPDATE posts SET body = (?) WHERE pid = ?;", (self.pbody.get(), self.c[0]))
            messagebox.showinfo('Succeeded!', 'You edit the post successfully!')
            query1 = "SELECT p.pid FROM posts p, questions q WHERE p.pid = q.pid AND p.pid = ?;"
            val1 = [self.c[0]]
            cursor.execute(query1, val1)
            c = cursor.fetchone()
            
            query2 = "SELECT p.pid FROM posts p, answers a WHERE p.pid = a.pid AND p.pid = ?;"
            val2 = [self.c[0]]
            cursor.execute(query2, val2)
            c2 = cursor.fetchone()                
            if c == None:
                self.c = c2
                self.window.destroy()
                PerformPostAction2(self.uid, self.c, self.root)    
            else:
                self.c = c
                self.window.destroy() 
                PerformPostAction(self.uid, self.c, self.root)    


    def back(self):
        self.window.destroy()
        query = "SELECT p.pid FROM posts p, questions q WHERE p.pid = q.pid AND p.pid = ?;"
        val = [self.c[0]]
        cursor.execute(query, val)
        c = cursor.fetchone()
        
        query2 = "SELECT p.pid FROM posts p, answers a WHERE p.pid = a.pid AND p.pid = ?;"
        val2 = [self.c[0]]
        cursor.execute(query2, val2)
        c2 = cursor.fetchone()                
        if c == None:
            self.c = c2
            self.window.destroy()
            PerformPostAction2(self.uid, self.c, self.root)    
        else:
            self.c = c
            self.window.destroy() 
            PerformPostAction(self.uid, self.c, self.root) 

            
            
class InputActionA:
    def __init__(self, uid, qid, master=None):
        self.root = master
        self.root.title('Post An Action-Answer')
        self.root.geometry('500x300')
        self.window = Frame(self.root)
        self.title = StringVar()
        self.body = StringVar()
        self.qid = qid[0]
        self.uid = uid
        self.c = qid
        self.create_window()


    def create_window(self):
        Label(self.window).grid(row=0)
        Label(self.window).grid(row=1)
        Label(self.window, text = 'POST TITLE:').grid(row = 2, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.title).grid(row = 2, column = 1, sticky = E)
        Label(self.window, text = 'POST TEXTS:').grid(row = 3, sticky = W, pady = 10)
        Entry(self.window, textvariable = self.body).grid(row = 3, column = 1, sticky = E)
        Button(self.window, text='CONFIRM', width = 8, command = self.confirm_answer).grid(row = 4, column = 1, sticky = W, pady = 10)
        Button(self.window, text='BACK', width = 8, command = self.back).grid(row = 5, column = 1, sticky = W, pady = 10)
        self.window.pack()


    def back(self):
        self.window.destroy()
        PerformPostAction(self.uid, self.c, self.root)   
        
        
    def confirm_answer(self):
        if len(self.title.get()) == 0 or len(self.body.get()) == 0:
            messagebox.showerror('ERROR!', 'The input can not be empty!')
        else:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            query = "SELECT pid FROM posts;"
            cursor.execute(query)
            c = cursor.fetchall()
            number = len(c)
            post_id = 'p' + '{:03d}'.format(number + 1)
            query = 'INSERT INTO posts VALUES (?,?,?,?,?);'
            val = [post_id, date, self.title.get(), self.body.get(), self.uid]
            cursor.execute(query, val)
            
            query2 = 'INSERT INTO answers VALUES (?,?);'
            val2 = [post_id, self.qid]
            cursor.execute(query2, val2)
            self.window.destroy()
            Search(self.uid, self.root)  
        
        
       

if __name__ == '__main__':
    root = Tk()
    connection = sqlite3.connect(dbPath)
    cursor = connection.cursor()    
    LogIn(root)
    root.mainloop()
    connection.commit()
    connection.close()    