import random
import string

import pymssql

types = ['文学','人文科学','历史地理','科普','艺术美术','小说散文','法律心理','宗教伦理']

def randIsbn() -> str :
    rand = random.randrange(0, 10000000000)
    randStr = 'ISBN' + '%010d' % rand
    return randStr

##随机生成字符串
def generate_random_string(length):
    letters = string.ascii_letters  # 包含所有大小写字母的字符串
    result = ''.join(random.choice(letters) for _ in range(length))
    return result


def randRecipient() -> str:
    randStr = generate_random_string(6)
    return randStr


def randPublisher() -> str:
    randStr = generate_random_string(6)
    return randStr


def randAuthor() -> str:
    randStr = generate_random_string(6)
    return randStr


# 连接数据库
def do_something(isbns, books, ins, outs, recipients, bookinfo):
    connect = pymssql.connect(
        server='10.222.49.41', # . 代表当前服务器
        user='sa',
        password='YoSt1KqPa0rd',
        database='TextbookSupport',
        charset='utf8',
        as_dict=True
    )
    if not connect:
        raise Exception('Connection Err')
    
    cur = connect.cursor()
    insert_template = 'INSERT INTO TextbookSupport.IsbnMap(ISBN, Publisher, Author, BookType) VALUES (%s, %s, %s, %d)'
    cur.executemany(insert_template, map(lambda i: (i[0], i[1], i[2], i[3]), bookinfo))
    connect.commit()

    # cur = connect.cursor()
    # insert_template = 'INSERT INTO TextbookSupport.TOrder(ISBN, Quantity) VALUES (%s, %d)'
    # cur.executemany(insert_template, zip(isbns, books))
    # connect.commit()

    cur = connect.cursor()
    insert_template = 'INSERT INTO TextbookSupport.InStock(ISBN, Quantity) VALUES (%s, %d)'
    cur.executemany(insert_template, map(lambda i: ( i[0] ,i[1]), ins))
    connect.commit()
    # connect.close()

### Dec22
    cur = connect.cursor()
    insert_template = 'INSERT INTO TextbookSupport.OutStock(Recipient, ISBN, Quantity) VALUES (%s, %s, %d)'
    cur.executemany(insert_template, map(lambda i: (i[0], i[1], i[2]), outs))
    connect.commit()
    connect.close()


if __name__ == '__main__':
    isbn_list = []
    random.seed(42)
    for i in range(10):
        isbn_list.append(randIsbn())

    books = []
    for i in range(10):
        books.append(random.randrange(50, 150))
    least = books.copy()
    ins = []
    for i in range(20):
        bookId = random.randrange(0, len(books))
        l = least[bookId]
        if l <= 0:
            continue
        s = random.randrange(l // 2, l * 2)
        if s == 0:
            continue
        if s > l:
            s = l + 1
        ins.append((isbn_list[bookId], s))

##Dec22
    recipient_list = []
    random.seed(40)
    for i in range(10):
        bookId = random.randrange(0, len(books))
        recipient_list.append(randRecipient())

    outs = []
    for i in range(0,10):
        bookId = random.randrange(0, len(books))
        bookNum = random.randrange(1, books[bookId])
        outs.append((recipient_list[i],isbn_list[bookId], bookNum))
    for i in range(0,10):
        bookId = randIsbn()
        bookNum = random.randrange(1, 10)
        outs.append((recipient_list[i],bookId, bookNum))


    bookinfo_list = []
    random.seed(41)
    for i in range(10):
        publisher = randPublisher()
        author = randAuthor()
        booktype = random.choice(types)
        bookinfo_list.append((isbn_list[i],publisher,author,booktype))

    print(isbn_list)
    print(ins)
    print(outs)
    do_something(isbn_list, books, ins, outs, recipient_list, bookinfo_list)

