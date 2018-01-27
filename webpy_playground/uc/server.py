import web
import pymysql
import hashlib

web.config.debug = False
render = web.template.render('templates')

urls = (
    '/', 'Homepage',
    '/user', 'User'
)


app = web.application(urls, globals())
store = web.session.Session(app, web.session.DiskStore('sessions'))

if web.config.get('_session') is None:
    session = web.session.Session(app, store)
    web.config._session = session
else:
    session = web.config._session


class Homepage:
    def GET(self):
        return render.index()

    def POST(self):
        form = web.input()
        emailAddress = form.emailaddress.strip()
        pwdhash = hashlib.md5(form.password.encode("utf8")).hexdigest()
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='test',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        coursor = connection.cursor()
        check = coursor.execute("select * from users where email = '%s' and password = '%s'" % (emailAddress, pwdhash))

        if check:
            session.loggedin = True
            session.username = form.username
            raise web.seeother('/user')
        else:
            return "Those login details don't work."


class User:
    def GET(self):
        return 'logined'


if __name__ == "__main__":
    app.run()