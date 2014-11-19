#-*- coding: utf-8 -*-

import sqlite3
import os
from flask import *
import time as time
from random import randint

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'database/eh.db'),
    DEBUG=True,
    # 生成秘钥
    SECRET_KEY=os.urandom(24),
    USERNAME='admin',
    PASSWORD='default'
))

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/')
def welcome():
    if session.get('logged_in'):
        return redirect(url_for('homePage'))
    else:
        return redirect(url_for('login'))

# 简化sqlite3的查询方式。
def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_l = None
    if request.method == 'POST':
        user = query_db('select * from user where username = ?', [request.form['username']], one=True)
        if user is None:
            error_l = u"用户名不存在。"
        else:
            if request.form['password'] != user['password']:
                error_l = u"密码不正确。"
            else:
                session['username'] = request.form['username']
                session['logged_in'] = True;
                return redirect(url_for('welcome'));
    return render_template("welcome.html", error_l = error_l)

# 注册。
@app.route('/register', methods=['GET', 'POST'])
def register():
    error_r = None
    if request.method == 'POST':
        user = query_db('select * from user where username = ?', [request.form['username']], one=True)
        if user is not None:
            error_r = u"用户名重复。"
        else:
            # 注册新用户。
            g.db.execute('insert into user (username, password) values (?, ?)', [request.form['username'], request.form['password']])
            g.db.commit()
            return redirect(url_for('welcome'));
    return render_template("welcome.html", error_r = error_r)

# 退出登录。
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# 主页页面。
@app.route('/home')
def homePage():
    if session.get('logged_in'):
        user = query_db('select * from user where username = ?', [session['username']], one=True)
        tracking = query_db('select tvname, epnum from tracking where userid = ?', [user['id']])
        # tracking是选取的剧集名称和集数。
        # mytv是一个list，插入的内容分别是单集、名称、观看地址和视频来源。
        mytv = []
        idlist = []
        if tracking:
            for i in tracking:
                L = query_db('select episode, epname, address, type from tv where tvname = ? order by episode ASC', [i['tvname']])
                # 按照集数的升序列出。
                tvid = query_db('select id, imgsrc from dream where name = ?', [i['tvname']], one=True)
                mytv.append(L)
                idlist.append(tvid)
        return render_template('homePage.html', user = user, zipped = zip(tracking, mytv, idlist), tracking = tracking)
    else:
        return redirect(url_for('welcome'))

# 浏览其他人的追剧。
@app.route('/view', methods=['GET'])
def viewUser():
    username = request.args.get('user', '')
    if username == '':
        return redirect(url_for('welcome'))
    user = query_db('select * from user where username = ?', [username], one=True)
    if user:
        tracking = query_db('select tvname, epnum from tracking where userid = ?', [user['id']])
        # tracking是选取的剧集名称和集数。
        # mytv是一个list，插入的内容分别是单集、名称、观看地址和视频来源。
        mytv = []
        idlist = []
        if tracking:
            for i in tracking:
                L = query_db('select episode, epname, address, type from tv where tvname = ? order by episode ASC', [i['tvname']])
                # 按照集数的升序列出。
                tvid = query_db('select id, imgsrc from dream where name = ?', [i['tvname']], one=True)
                mytv.append(L)
                idlist.append(tvid)
    else:
        return redirect(url_for('welcome'))
    return render_template('homePage.html', user = user, zipped = zip(tracking, mytv, idlist), tracking = tracking)

# 广场页面。
@app.route('/square')
def squarePage():
    if session.get('logged_in'):
        user = query_db('select * from user where username = ?', [session['username']], one=True)
        ticks = int(time.time()) - 172800
        print ticks
        # 过滤超过两天之前的剧集更新记录
        g.db.execute('delete from ping where time < ?', [ticks])
        g.db.commit()
        tv = query_db('select * from ping limit 50')
        tv.reverse()
        imglist = []
        for i in tv:
            img = query_db('select imgsrc from dream where name = ?', [i['name']], one=True)
            imglist.append(img['imgsrc'])
        return render_template('squarePage.html', user = user, tv = zip(tv, imglist))
    else:
        return redirect(url_for('welcome'))

# 吐槽页面。
@app.route('/talk')
def talkPage():
    if session.get('logged_in'):
        user = query_db('select * from user where username = ?', [session['username']], one=True)
        tracking = query_db('select tvname, epnum from tracking where userid = ?', [user['id']])
        talkList = []
        sql = 'select * from discuss where tvname = ?' + ' or tvname = ?' * (len(tracking)-1)
        talk = query_db(sql+' limit 30', [i['tvname'] for i in tracking])
        talk.reverse()
        for i in talk:
            i['time'] = delta_T(i['time'])
        talkList.append(talk)
        return render_template('talkPage.html', user = user, tracking = tracking, talkList = talkList)
    else:
        return redirect(url_for('welcome'))

# 时间差，输入时间戳，根据当前时间计算出时间差，并输出字符串。
def delta_T(t):
    d1 = time.gmtime()
    d2 = time.gmtime(t)
    s = ''
    if d1.tm_year - d2.tm_year == 0:
        if d1.tm_mon - d2.tm_mon == 0:
            if d1.tm_mday - d2.tm_mday == 0:
                if d1.tm_hour - d2.tm_hour == 0:
                    if d1.tm_min - d2.tm_min == 0:
                        s = str(d1.tm_sec-d2.tm_sec)+u'秒前'
                    else:
                        s = str(d1.tm_min-d2.tm_min)+u'分钟前'
                else:
                    s = str(d1.tm_hour-d2.tm_hour)+u'小时前'
            else:
                s = str(d1.tm_mday-d2.tm_mday)+u'天前'
        else:
            s = str(d1.tm_mon-d2.tm_mon)+u'月前'
    else:
        s = str(d1.tm_year-d2.tm_year)+u'年前'
    return s

# 搜索框。
@app.route('/hint', methods=['GET'])
def hint():
    tv = None
    user = None
    str = '%' + request.args.get('str', '') + '%'
    if str:
        tv = query_db('select name from dream where name like ? or enname like ? limit 5', [str, str])
        user = query_db('select username from user where username like ? limit 5', [str])
    result = {'tv': tv, 'user': user}
    return jsonify(result)

# 添加剧集。
@app.route('/addTV', methods=['GET'])
def addTV():
    if session.get('logged_in'):
        tvname = request.args.get('tv', '')
        userid = query_db('select id from user where username = ?', [session['username']], one=True)
        if query_db('select id from tracking where tvname = ? and userid = ?', [tvname, userid['id']], one=True):
            pass
        else:
            g.db.execute('insert into tracking (tvname, userid) values (?, ?)', [tvname, userid['id']])
            g.db.commit()
    return redirect(url_for('welcome'))

# 提交吐槽。
@app.route('/postTalk', methods=['POST'])
def postTalk():
    if session.get('logged_in'):
        tvname = request.form['tv']
        content = request.form['content']
        ticks = int(time.time())
        userid = query_db('select id from user where username = ?', [session['username']], one=True)
        warning = query_db('select epnum from tracking where userid = ? and tvname = ?', [userid['id'], tvname], one=True)
        g.db.execute('insert into discuss (tvname, name1, time, warning, content) values (?, ?, ?, ?, ?)', [tvname, session['username'], ticks, warning['epnum'], content])
        g.db.commit()
        return redirect(url_for('talkPage'))
    else:
        return redirect(url_for('welcome'))

# 删除剧集。
@app.route('/removeTV', methods=['GET'])
def removeTV():
    if session.get('logged_in'):
        tvname = request.args.get('tv', '')
        userid = query_db('select id from user where username = ?', [session['username']], one=True)
        g.db.execute('delete from tracking where tvname = ? and userid = ?', [tvname, userid['id']])
        g.db.commit()
    return redirect(url_for('welcome'))

# 更新追剧记录。
@app.route('/updateTV', methods=['GET'])
def updateTV():
    if session.get('logged_in'):
        tvname = request.args.get('tv', '')
        episode = request.args.get('ep', 0)
        userid = query_db('select id from user where username = ?', [session['username']], one=True)
        g.db.execute('update tracking set epnum = ? where tvname = ? and userid = ?', [episode, tvname, userid['id']])
        g.db.commit()
    return redirect(url_for('welcome'))

@app.route('/test/<username>')
def show_user_profile(username):
    return '你好 %s' % username

@app.route('/test/<int:post_id>')
def show_post(post_id):
    return '你投送了 %d' % post_id

@app.route('/refresh')
def refresh():
    if session.get('logged_in'):
        user = query_db('select noticenum, notification from user where username = ?', [session['username']], one=True)
        if user['notification']:
            notifications = user['notification'].split('###')
        else:
            notifications = ['空', ''];
        js = {"num": user["noticenum"], "value": notifications[len(notifications)-2]}
        return jsonify(js)
    else:
        return redirect(url_for('welcome'));

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404

if __name__ == "__main__":
    app.run(debug=True)