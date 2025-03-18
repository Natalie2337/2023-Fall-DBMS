import pymssql


# 连接数据库
def get_conn():
    connect = pymssql.connect(
        server='127.0.0.1', # . 代表当前服务器
        user='sa',
        password='hyh20011225',
        database='TextBookDB2',
        charset='utf8',
        as_dict=True
    )
    if connect:
        print("数据库连接成功！")
    else:
        print("链接失败！")
    return connect

if __name__ == '__main__':
    get_conn()


