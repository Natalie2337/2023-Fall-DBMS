from flask import Flask, render_template, request, flash, session, redirect, url_for, jsonify
from functools import wraps
import pymssql
import json

import connect

app = Flask(__name__, template_folder="templates")
## set a secret key, which is crucial for securely signing session cookies and other security-related functionality in Flask
app.config['SECRET_KEY'] = "123412312312312412"

#判断用户是否登录
def require_login(func):
    @wraps(func)
    def inner_func(*args, **kwargs):
        if not 'username' in session:
            flash('请先登录!', 'danger')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return inner_func

###########################################################################################
### Login
@app.route('/login', methods=['GET','POST'])  
def login():
    if request.method == 'POST':
        # 需要从request对象读取表单内容：
        username = request.form['username']
        password = request.form['password']
        print(request.form['is_admin'])

        #判断是否为管理员
        if request.form['is_admin'] == "1":
            if username == 'admin' and password == '111111': ##对用户名和密码进行判断
                session['is_admin'] = True
                session['username'] = username
            else:
                flash('用户名和密码不匹配，请重输', 'danger')
                return redirect(url_for('login'))
        else:
            if username == 'student' and password == '123456':
                session['is_admin'] = False
                session['username'] = username
            else:
                flash('用户名和密码不匹配，请重输', 'danger')
                return redirect(url_for('login'))
        flash('您好 {} !'.format(username),'success')
        return redirect(url_for("index"))
    else:
        return render_template("login.html")

#用户退出系统，删除所有session
@app.route('/logout')
@require_login
def logout():
    session.clear()
    flash('已退出!','success')
    return redirect(url_for('login'))

'''
@app.route('/', methods=['GET'])
@require_login
def index():
    ISBN =  request.args.get('ISBN')
    if ISBN:
        sql1 = f"SELECT * FROM dbo.IsbnMap WHERE ISBN LIKE '%{ISBN}%'" ##这里的{ISBN}是上面那个变量. Like模糊查询

    else:
        sql1 = f"SELECT * FROM dbo.IsbnMap"
    connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')
    cursor = connect.cursor()
    cursor.execute(sql1)
    query_result = cursor.fetchall()

    return render_template('index.html', query_result=query_result)

'''
#首页

@app.route('/', methods=['GET'])
@require_login
def index():
    ISBN = request.args.get('ISBN')
    if ISBN:
        sql1 = "SELECT * FROM dbo.IsbnMap WHERE ISBN LIKE %s"
        params = ('%' + ISBN + '%',)  # 构建参数，注意这里的拼接方式
    else:
        sql1 = "SELECT * FROM dbo.IsbnMap"
        params = None

    connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')
    cursor = connect.cursor()

    if params:
        cursor.execute(sql1, params)
    else:
        cursor.execute(sql1)

    query_result = cursor.fetchall()

    return render_template('index.html', query_result=query_result)


# ##############################################################################################

'''
## 入库查询
@app.route('/instock', methods=['GET', 'POST'])
@require_login
def queryInStockView():
    ISBN =  request.args.get('ISBN')
    if ISBN:
        sql1 = f"SELECT * FROM dbo.InStockView WHERE ISBN LIKE '%{ISBN}%'"
    else:
        sql1 = f"SELECT * FROM dbo.InStockView"
    connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')
    cursor = connect.cursor()
    cursor.execute(sql1)
    query_result = cursor.fetchall()

    return render_template('inStockView.html', query_result=query_result)  ##如果进入了if语句，则跳转到这个网页
    ## query_result是一个变量，它的值将在模板文件中被使用。这段代码的作用是将query_result的值渲染到queryDistribution.html模板中，以便在网页中显示出来。

'''

@app.route('/instock', methods=['GET', 'POST'])
@require_login
def queryInStockView():
    ISBN = request.args.get('ISBN')
    if ISBN:
        sql1 = "SELECT * FROM dbo.InStockView WHERE ISBN LIKE %s"
        params = ('%' + ISBN + '%',)
    else:
        sql1 = "SELECT * FROM dbo.InStockView"
        params = None

    connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')
    cursor = connect.cursor()

    if params:
        cursor.execute(sql1, params)
    else:
        cursor.execute(sql1)

    query_result = cursor.fetchall()

    return render_template('inStockView.html', query_result=query_result)


## 出库查询数据
@app.route('/outstock', methods=['GET', 'POST'])
@require_login
def queryOutStockView():
    ISBN =  request.args.get('ISBN')
    if ISBN:
        sql1 = f"SELECT * FROM dbo.OutStockView WHERE ISBN LIKE %s"
        params = ('%' + ISBN + '%',)
    else:
        sql1 = f"SELECT * FROM dbo.OutStockView"
        params = None
    connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')
    cursor = connect.cursor()

    if params:
        cursor.execute(sql1, params)
    else:
        cursor.execute(sql1)

    query_result = cursor.fetchall()

    return render_template('outStockView.html', query_result=query_result)  ##如果进入了if语句，则跳转到这个网页
    ## query_result是一个变量，它的值将在模板文件中被使用。这段代码的作用是将query_result的值渲染到queryDistribution.html模板中，以便在网页中显示出来。


# 订购查询
@app.route('/queryorder', methods=['GET', 'POST'])
@require_login
def queryOrder():
    ISBN =  request.args.get('ISBN')
    if ISBN and '-' not in ISBN:
        sql1 = f"SELECT * FROM dbo.TOrder WHERE ISBN LIKE '%{ISBN}%'"
    else:
        sql1 = f"SELECT * FROM dbo.TOrder"

    connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')
    cursor = connect.cursor()
    cursor.execute(sql1)
    query_result = cursor.fetchall()

    return render_template('queryOrder.html', query_result=query_result)

# 库存查询
@app.route('/remainView', methods=['GET', 'POST'])
@require_login
def remainView():
    ISBN =  request.args.get('ISBN')
    if ISBN and '-' not in ISBN:
        sql1 = f"SELECT * FROM dbo.RemainView WHERE ISBN LIKE '%{ISBN}%'"
    else:
        sql1 = f"SELECT * FROM dbo.RemainView"

    connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')
    cursor = connect.cursor()
    cursor.execute(sql1)
    query_result = cursor.fetchall()

    return render_template('remainView.html', query_result=query_result)


#########################################################################################################
## 对InStock表, OutStock表, TOrder表的操作

#添加入库记录
@app.route('/addInStock', methods=['GET', 'POST'])
@require_login
def addInStock():
    if request.method == 'POST':

        ISBN = request.form.get('isbn', '')
        Quantity = request.form.get('quantity', 0)
        connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')

        # insert
        cur = connect.cursor()
        query = f"INSERT INTO dbo.InStock (ISBN, Quantity) VALUES ('{ISBN}', {Quantity})"
        cur.execute(query)
        connect.commit()
        connect.close()

    # 显示数据库
    connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')  ##记得重新打开connection
    cur = connect.cursor()
    
    sql1 = "SELECT DISTINCT(ISBN) FROM dbo.InStockView"
    cur.execute(sql1)
    isbn_list = cur.fetchall()

    ISBN =  request.args.get('ISBN')
    if ISBN:
        query = f"SELECT * FROM dbo.InStock WHERE ISBN LIKE '%{ISBN}%'"
    else:
        query = f"SELECT * FROM dbo.InStock"
    cur.execute(query)
    query_result = cur.fetchall()
    connect.close()

    return render_template('inStock.html', query_result=query_result,isbn_list=isbn_list)


## 设置id，便于我们进行界面上的删除操作
#删除入库记录
@app.route('/delInstock/<id>', methods=['GET', 'POST'])
@require_login
def delInstock(id):
    connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')
    cur = connect.cursor()

    # 删除记录
    query = f"DELETE FROM dbo.InStock WHERE id={id}"
    cur.execute(query)

    connect.commit()
    connect.close()
    flash('删除记录成功', 'success')
    return redirect(url_for("addInStock"))

##　添加出库
@app.route('/addOutStock', methods=['GET', 'POST'])
@require_login
def addOutStock():
    if request.method == 'POST':
        # get values
        Recipient = request.form.get('recipient', '')
        ISBN = request.form.get('isbn', '')
        Quantity = request.form.get('quantity', 0)
        connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')
        try:
            # insert
            cur = connect.cursor()
            query = f"INSERT INTO dbo.OutStock (Recipient, ISBN, Quantity) VALUES (N'{Recipient}','{ISBN}', {Quantity})"  #### N：匹配中文
            cur.execute(query)
            connect.commit()
            connect.close()

        except pymssql.Error as e:
            error_message = str(e)
            #flash(error_message, 'danger')
            flash('库存不够！', 'danger')


    # 显示数据库
    connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')  ##记得重新打开connection
    cur = connect.cursor()
    
    sql1 = "SELECT DISTINCT(ISBN) FROM dbo.InStockView"
    cur.execute(sql1)
    isbn_list = cur.fetchall()

    ISBN =  request.args.get('ISBN')
    if ISBN:
        query = f"SELECT * FROM dbo.OutStock WHERE ISBN LIKE '%{ISBN}%'"
    else:
        query = f"SELECT * FROM dbo.OutStock"
    # query = "SELECT * FROM dbo.OutStock"
    cur.execute(query)
    query_result = cur.fetchall()
    connect.close()

    return render_template('outStock.html', query_result=query_result,isbn_list=isbn_list)

#删除出库记录
@app.route('/delOutstock/<id>', methods=['GET', 'POST'])
@require_login
def delOutstock(id):
    connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')
    cur = connect.cursor()

    # 删除记录
    query = f"DELETE FROM dbo.OutStock  WHERE id={id}"
    cur.execute(query)

    connect.commit()
    connect.close()
    flash('删除记录成功', 'success')
    return redirect(url_for("addOutStock"))


@app.route('/orderList', methods=['GET', 'POST'])
@require_login
def orderList():
    # 显示数据库
    connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')  ##记得重新打开connection
    cur = connect.cursor()
    
    isbn =  request.args.get('ISBN') ##
    status =  request.args.get('status')
    if isbn and status:
        query = f"SELECT * FROM dbo.TOrder WHERE ISBN  LIKE '%{isbn}%' AND status=N'{status}'"
    elif isbn: 
        query = f"SELECT * FROM dbo.TOrder WHERE ISBN  LIKE '%{isbn}%'"
    elif status:
        query = f"SELECT * FROM dbo.TOrder WHERE status=N'{status}'"
    else:
        query = f"SELECT * FROM dbo.TOrder"

    cur.execute(query)
    query_result = cur.fetchall()

    sql1 = "SELECT DISTINCT(ISBN) FROM dbo.InStockView"
    cur.execute(sql1)
    isbn_list = cur.fetchall()

    connect.close()

    return render_template('orderList.html', query_result=query_result,isbn_list=isbn_list)

@app.route('/addOrder', methods=['POST'])
@require_login
def addOrder():
    if request.method == 'POST':
        # get values
        ISBN = request.form.get('isbn', '')
        Quantity = request.form.get('quantity', 0)
        connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')

        # insert
        cur = connect.cursor()
        query = f"INSERT INTO dbo.TOrder(ISBN, Quantity, Status) VALUES ('{ISBN}', {Quantity},N'购买中')"
        cur.execute(query)
        connect.commit()
        connect.close()

    flash('添加一条订购记录', 'success')
    return redirect(url_for("orderList"))

@app.route('/confirmOrder/<id>', methods=['GET', 'POST'])
@require_login
def confirmOrder(id):
    connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')
    cur = connect.cursor()
    
    sql1 = f"SELECT * FROM dbo.TOrder WHERE TOrder.id={id}"
    cur.execute(sql1)
    record = cur.fetchall()

    # 更改状态
    query = f"UPDATE dbo.TOrder SET status = N'已入库' WHERE TOrder.id={id}"
    cur.execute(query)

    # 入库操作
    sql2 = f"INSERT INTO dbo.InStock (ISBN, Quantity) VALUES ('{record[0][1]}', {record[0][2]})"
    cur.execute(sql2)

    connect.commit()
    connect.close()

    flash('确认入库成功', 'success')
    return redirect(url_for("orderList"))

@app.route('/deleteOrder/<id>', methods=['GET', 'POST'])
@require_login
def deleteOrder(id):
    connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')
    cur = connect.cursor()

    # 删除记录
    query = f"DELETE FROM dbo.TOrder WHERE TOrder.id={id}"
    cur.execute(query)

    connect.commit()
    connect.close()
    flash('删除记录成功', 'success')
    return redirect(url_for("orderList"))


#####################################################################对书籍信息的操作

@app.route('/manageBook', methods=['GET'])
@require_login
def manageBook():
    isbn =  request.args.get('isbn')
    title = request.args.get('title')

    ##输入isbn号或者书籍名称可以查询书
    if isbn and title:
        sql1 = f"SELECT * FROM dbo.IsbnMap WHERE ISBN LIKE '%{isbn}%' and Title LIKE N'%{title}%'"
    elif isbn:
        sql1 = f"SELECT * FROM dbo.IsbnMap WHERE ISBN LIKE '%{isbn}%'"
    elif title:
        sql1 = f"SELECT * FROM dbo.IsbnMap WHERE Title LIKE N'%{title}%'"
    else:
        sql1 = f"SELECT * FROM dbo.IsbnMap"

    connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')
    cursor = connect.cursor()
    cursor.execute(sql1)
    query_result = cursor.fetchall()

    return render_template('manageBook.html', query_result=query_result)

'''
##增加一本书的名字
@app.route('/addBookinfo', methods=['POST'])
@require_login
def addBookinfo():
    connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')
    cur = connect.cursor()

    if request.method == "POST":
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        publisher = request.form.get('publisher')
        author = request.form.get('author')
        booktype = request.form.get('booktype')
        price = request.form.get('price')

        # 插入记录
        query = f"INSERT INTO dbo.IsbnMap (ISBN, Title, Publisher, Author, BookType, Price) VALUES ( N'{isbn}', N'{title}', N'{publisher}', N'{author}', N'{booktype}','{price}')"
        cur.execute(query)

        connect.commit()
        connect.close()
        flash('插入记录成功', 'success')
        return redirect(url_for("manageBook"))  ##
'''


##增加一本书的名字
@app.route('/addBookinfo', methods=['POST'])
@require_login
def addBookinfo():

    ##加上对ISBN号限制的trigger:
    try:
        connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')
        cur = connect.cursor()

        if request.method == "POST":
            isbn = request.form.get('isbn')
            title = request.form.get('title')
            publisher = request.form.get('publisher')
            author = request.form.get('author')
            booktype = request.form.get('booktype')
            price = request.form.get('price')

            # 插入记录
            query = f"INSERT INTO dbo.IsbnMap (ISBN, Title, Publisher, Author, BookType, Price) VALUES ( N'{isbn}', N'{title}', N'{publisher}', N'{author}', N'{booktype}','{price}')"
            cur.execute(query)

            connect.commit()
            connect.close()
            flash('插入记录成功', 'success')
    except pymssql.Error as e:
        error_message = str(e)
        flash('ISBN格式不匹配', 'danger')
        #return jsonify({'success': False, 'error': error_message})
    return redirect(url_for("manageBook"))

'''
@app.route('/addBookinfo', methods=['POST'])
@require_login
def addBookinfo():
    try:
        connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')
        cur = connect.cursor()

        if request.method == "POST":
            isbn = request.form.get('isbn')
            title = request.form.get('title')
            publisher = request.form.get('publisher')
            author = request.form.get('author')
            booktype = request.form.get('booktype')
            price = request.form.get('price')

            query = f"INSERT INTO dbo.IsbnMap (ISBN, Title, Publisher, Author, BookType, Price) VALUES ( N'{isbn}', N'{title}', N'{publisher}', N'{author}', N'{booktype}','{price}')"
            cur.execute(query)

            connect.commit()
            connect.close()

            return jsonify({'success': True})  # Successful insertion

    except pymssql.Error as e:
        error_message = str(e)
        return jsonify({'success': False, 'error': error_message})  # Failed insertion

    return jsonify({'success': False, 'error': 'Unknown error'})  # Catch-all failure


@app.route('/addBook', methods=['POST'])
def add_book():
    result = addBookinfo()
    return result
'''

'''
@app.route('/editBookinfo/<id>', methods=['GET', 'POST'])
@require_login
def editBookinfo(id):
    connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')
    cur = connect.cursor()

    if request.method == "POST":
        #isbn = request.form.get('isbn')
        publisher = request.form.get('publisher')
        author = request.form.get('author')
        booktype = request.form.get('booktype')
        price = request.form.get('price')

        # 更改记录 (不修改书名和ISBN)
        query = f"UPDATE dbo.IsbnMap SET Publisher = N'{publisher}', Author=N'{author}', BookType=N'{booktype}', Price='{price}' WHERE id={id}"
        cur.execute(query)

        connect.commit()
        connect.close()
        flash('更改记录成功', 'success')
        return redirect(url_for("manageBook"))
    else:
        query =  f"SELECT * FROM dbo.IsbnMap WHERE id={id}" 
        cur.execute(query)
        result = cur.fetchall()
        return render_template("editBookinfo.html", record=result[0])


@app.route('/delBookinfo/<id>', methods=['GET', 'POST'])
@require_login
def delBookinfo(id):
    connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')
    cur = connect.cursor()

    # 按序号删除记录
    query = f"DELETE FROM dbo.IsbnMap WHERE IsbnMap.id=@{id}"
    cur.execute(query)

    connect.commit()
    connect.close()
    flash('删除记录成功', 'success')
    return redirect(url_for("manageBook"))
'''

@app.route('/editBookinfo/<isbn>', methods=['GET', 'POST'])
@require_login
def editBookinfo(isbn):
    connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')
    cur = connect.cursor()

    if request.method == "POST":
        #isbn = request.form.get('isbn')
        publisher = request.form.get('publisher')
        author = request.form.get('author')
        booktype = request.form.get('booktype')
        price = request.form.get('price')

        # 更改记录 (不修改书名和ISBN)
        query = f"UPDATE dbo.IsbnMap SET Publisher = N'{publisher}', Author=N'{author}', BookType=N'{booktype}', Price='{price}' WHERE ISBN='{isbn}'"
        cur.execute(query)

        connect.commit()
        connect.close()
        flash('更改记录成功', 'success')
        return redirect(url_for("manageBook"))
    else:
        query =  f"SELECT * FROM dbo.IsbnMap WHERE ISBN='{isbn}'"
        cur.execute(query)
        result = cur.fetchall()
        return render_template("editBookinfo.html", record=result[0])


@app.route('/delBookinfo/<isbn>', methods=['GET', 'POST'])
@require_login
def delBookinfo(isbn):
    connect = pymssql.connect('localhost', 'sa', 'hyh20011225', 'TextbookDB2')
    cur = connect.cursor()

    # 按序号删除记录
    query = f"DELETE FROM dbo.IsbnMap WHERE IsbnMap.ISBN='{isbn}'"
    cur.execute(query)

    connect.commit()
    connect.close()
    flash('删除记录成功', 'success')
    return redirect(url_for("manageBook"))


if __name__ == '__main__':
    app.run()

