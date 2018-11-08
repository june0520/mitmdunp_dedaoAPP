from mitmproxy import ctx
import json
import pymongo
'''利用mitmdump抓取得到APP并将书籍内容保存到MongoDB数据库中'''

def response(flow):
    client = pymongo.MongoClient(host="localhost", port=27017)
    db = client['dedao']
    collection = db["books"]
    #分析数据的请求地址。Windows系统不支持mitmproxy转用Charles 分析
    url = 'https://m.igetget.com/hybrid/api/ebook/list'
    if flow.request.url.startswith(url):
        text = flow.response.text
        data = json.loads(text)
        #分析数据结构时在cmd中无法看到完整的json 数据结构可以执行mitmdump -s mitmdump_dedaoAPP.py（脚本文件名） > outfile.txt
        #将输出结果导出到本地文件，方便分析
        books = data.get('data')
        for book in books:
            data = {
                'title': book.get('bookName'),
                'cover': book.get('bookIntro'),
                'price': book.get('currentPrice')
            }
            #在cmd中输出结果
            ctx.log.info(str(data))
            #保存到数据库
            collection.insert(data)
