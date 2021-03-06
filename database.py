import sqlite3

# 打开数据库
def connect_database():
    try:
        print('连接数据库中')
        conn = sqlite3.connect('database/dbdb.sqlite')
        cur = conn.cursor()
        print('数据库连接成功')
    except Exception as e:
        print('!!!数据库连接失败!!!')
    return conn,cur

def insert_sid(conn,cur,bookname,sid):
    cur.execute('''INSERT OR IGNORE INTO Book_Sid(bookname, sid) VALUES(?,?)''',
                    (bookname, sid))
    conn.commit()
    print('（1/2）同步成功：'+bookname)

# s = {'rating': 8.0, 'rating_people': 10813, 'author': '[英]安吉拉·卡特', 'book_summary': '\n很久很久以前，精怪故事不光是给孩子们看的，《安吉拉·卡特的精怪故事集》就是如此。这部精彩的集子囊括了抒情故事、血腥故事、令人捧腹的故事和粗俗下流的故事，它们来自世界各地，从北极到亚洲——里面决没有昏头昏脑的公主和多愁善感的仙子；相反，我们看到的是美丽的女仆和干瘪的老太婆，狡猾的妇人和品行不端的姑娘，巫婆和接生婆，坏姨妈和怪姐妹。 这些出色的故事颂扬坚强的意志、卑鄙的欺诈、妖术与阴谋，采集它们的只可能是独一无二且令我们深深怀念的安吉拉·卡特。 最初以《悍妇精怪故事集》和《悍妇精怪故事集第二卷》的形式出版', 'author_summary': '\n安吉拉·卡特（Angela Carter, 1940-1992），出生于英国伊斯特本（Eastbourne），是英国最具独创性的作家之一，书写风格混合魔幻写实、歌德式以及女性主义。卡特著有八部小说：《魔幻玩具铺》（The Magic Toyshop ,获约翰·勒维林·里 斯奖）、《数种知觉》（获毛姆奖）、《英雄与恶徒》、《爱》、《霍夫曼博士的地狱欲望机器》、《新夏娃的激情》、《马戏团之夜》以及《明智的孩子》。三本短篇小说集：《染血之室》、《烟火：个个世俗故事》，以及《圣人与陌生人》等等。卡特的作品也深受媒体喜爱：短篇小说《与狼为伴》和《魔幻玩具铺》曾拍成电影，《马戏团之夜》和《明智的孩子》改编成舞台剧于伦敦上演，2006年更被誉为是安吉拉·卡特之年，在英伦掀起一阵卡特热潮。'}
def update_book_data(conn, cur, sid, bookdata):
    cur.execute('''UPDATE Book_Sid
                SET rating = :rating, 
                    rating_people = :rating_people, 
                    author = :author, 
                    author_summary = :author_summary, 
                    book_summary = :book_summary
                WHERE sid = :sid ''',
                {"rating":bookdata["rating"],"rating_people":bookdata["rating_people"],"author":bookdata["author"],"author_summary":bookdata["author_summary"],"book_summary":bookdata["book_summary"],"sid": sid}
    )
    conn.commit()
    print('（2/2）更新成功 ')

# insert_book_data(conn,cur,s)