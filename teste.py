__author__ = 'Denny'
from server import CrawlerServer,start
from pykondoraux import sqlquery
sql = sqlquery.SqlQuery(host='173.194.231.2',passwd='seilah123',db='ebayscraping')
def dataHandle(kwargs):
    requiriments=[
        'startprice',
        'description',
        'category',
        'quantity',
        'condition',
        'title',
        'productid',
        'picurl',
        'link']
    ok = True
    for r in requiriments:
        if not r in kwargs or kwargs[r]=='':
            ok=False
    if not ok and len(kwargs['links2add'])==0:
        print 'AHH DESGRACA!!'
        server.appendParams([kwargs['scrapParams']])
    else:
        if ok:
            query=''
            try:
                query = '''
                 replace into xaeletronics (`{c}`) values ('{v}')
                '''.format(
                    c='`,`'.join(requiriments),
                    v="','".join([
                        kwargs[i].replace("\\\'","#$%#").replace("'","\\'") \
                            .replace("#$%#","\\\'").replace('\n','')
                        for i in requiriments])
                )
                sql.exec_(query)
            except:
                print kwargs


        print 'TUDO NA BOA',kwargs
        server.scrapedsUrls.append(kwargs['link'])
        print len(server.scrapParamsQueue), len(server.scrapedsUrls)

server = CrawlerServer(3,'C:\Users\Denny\Documents\Django-Projects\webscraping\client.py',dataHandle)
links = sql.exec_("select link from xaeletronics")
server.scrapedsUrls=[i[0] for i in links]
server.appendParams([{
    'templatePath':'templates.ebayGetLinks',
    'url':  'http://www.ebay.com/sch/xa-electronics/m.html?_nkw=&_armrs=1&_ipg=&_from='
}])
start(server)