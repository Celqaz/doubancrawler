# coding: utf-8
import database
import get_book_info

# 连接数据库
conn,cur = database.connect_database()

# s = {'rating': 8.0, 'rating_people': 10813, 'author': '[英]安吉拉·卡特', 'book_summary': '\n很久很久以前，精怪故事不光是给孩子们看的，《安吉拉·卡特的精怪故事集》就是如此。这部精彩的集子囊括了抒情故事、血腥故事、令人捧腹的故事和粗俗下流的故事，它们来自世界各地，从北极到亚洲——里面决没有昏头昏脑的公主和多愁善感的仙子；相反，我们看到的是美丽的女仆和干瘪的老太婆，狡猾的妇人和品行不端的姑娘，巫婆和接生婆，坏姨妈和怪姐妹。 这些出色的故事颂扬坚强的意志、卑鄙的欺诈、妖术与阴谋，采集它们的只可能是独一无二且令我们深深怀念的安吉拉·卡特。 最初以《悍妇精怪故事集》和《悍妇精怪故事集第二卷》的形式出版', 'author_summary': '\n安吉拉·卡特（Angela Carter, 1940-1992），出生于英国伊斯特本（Eastbourne），是英国最具独创性的作家之一，书写风格混合魔幻写实、歌德式以及女性主义。卡特著有八部小说：《魔幻玩具铺》（The Magic Toyshop ,获约翰·勒维林·里 斯奖）、《数种知觉》（获毛姆奖）、《英雄与恶徒》、《爱》、《霍夫曼博士的地狱欲望机器》、《新夏娃的激情》、《马戏团之夜》以及《明智的孩子》。三本短篇小说集：《染血之室》、《烟火：个个世俗故事》，以及《圣人与陌生人》等等。卡特的作品也深受媒体喜爱：短篇小说《与狼为伴》和《魔幻玩具铺》曾拍成电影，《马戏团之夜》和《明智的孩子》改编成舞台剧于伦敦上演，2006年更被誉为是安吉拉·卡特之年，在英伦掀起一阵卡特热潮。'}
# sid = '5993314'

# 寻找sid

bl = get_book_info.get_book_list()
total = len(bl)
print("一共"+str(total)+"本书")
n = 1 
error_log = []
for i in bl:
    print("当前进度："+str((n-1)/total*100)+"%")
    print("----正在处理第"+str(n)+"本书----")
    try:
        bookname,sid = get_book_info.get_book_sid(i)
        database.insert_sid(conn,cur,bookname,sid)
        bookdata = get_book_info.get_book_data(sid)
        database.update_book_data(conn,cur,sid,bookdata)
    except:
        error_log.append(bookname+str(n))
        print(error_log)
        continue
    n = n + 1
    print('----完╰(*°▽°*)╯成 ----')
print(error_log)

# 手动
# sid = '2119536'
# bookdata = get_book_info.get_book_data(sid)
# database.update_book_data(conn,cur,sid,bookdata)