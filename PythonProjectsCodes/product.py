# -*- coding: utf-8 -*-
import scrapy
import json

#import pymysql

#link='http://y.soyoung.com/yuehui/shop?district_id={}&menu1_id={}&sort=13&index=0'
#cat = [10020, 10021, 10010, 10001, 10003, 10006, 10019, 10008, 10009, 10011, 10013, \
#       10023, 10022, 10015, 10012, 10007, 10017, 10018]
#large = [19, 1, 17, 9, 10, 11, 23, 18, 15, 16, 12, 22, 13, 6]
#small = [25, 27, 14, 3, 2, 556, 8, 20, 31, 7, 21, 4, 24, 28, 5, 32, 30, 33, 29, 561, 560, 34]



class Collect(object):
    
    def __init__(self, link, place_id, cat_id):
        
        
        self.link =  link.format(place_id, cat_id, '{}')

        self.place_id = place_id
        self.cat_id = cat_id
        self.collect = []
        self.df = None
        self.flag = 0 
        
        
    def __scrape(self, index):
        
        try:
            products = json.loads(requests.get(self.link.format(index), timeout=3).text)['responseData']['product_info']
            print 'O',
            
            if len(products)==0:
                try: 
                    if 0==len(json.loads(requests.get(self.link.format(index), timeout=3).text)['responseData']['product_info']):
                        print 'E',
                        self.flag = 1
                        return
                except:
                    print '?',
                    self.__scrape(index)
            

            for product in products:
                # clean field "doctor" for encoding
                s = ''
                try:
                    for d in product['doctor']:
                        for e in d.items():
                            s = s+'::'.join(e)+'--'
                    product['doctor'] = s
                except:
                    print 'D',
                
                # clean field
                try:
                    product['wei_kuan'] = '::'.join(product['wei_kuan'])
                    product['wei_kuan_list'] = '::'.join(product['wei_kuan_list'])
                except:
                    print 'W',
                    
                try:
                    product = flatten_dict(product, layers=3)
                except:
                    print 'P',
                    
                self.collect.append(product)
                
        except Exception as e:
            print e
            print 'T',
            exit(0)
            self.__scrape(index)  
            
    def main(self):
        
            
        for i in range(180):
            if not self.flag:
                self.__scrape(i)
                    
                                    
        print(len(self.collect))

        self.df = pd.DataFrame(self.collect) 
        
        try:
            col = list(self.df.columns)
            col = [col.pop(col.index('pid')), col.pop(col.index('title'))]+col
            self.df = self.df[col]
        except:
            print 'U'
        
        return self.df     
    def save(self):
        
        ct = ctime().split()
        folder= ct[2]+ct[1]+ct[-1]+'_product/'
        try:
            os.mkdir(folder)
        except:
            print 'R'
        try:
            name = "{}_{}.xlsx".format(self.place_id, self.cat_id)
            self.df.to_excel('./'+folder + name, encoding="utf-8", index=False)
            print "Save Success! for "+name
        except:
            print "Save Error"
            
        print len(os.listdir(folder)),'files scraped!'
    def __repr__(self):
        return "place: "+ str(self.place_id)+ " category: "+ str(self.cat_id)+ " scraped: "+ str(self.flag==1)
        
        


        
category = {0: u'\u5168\u90e8\u9879\u76ee',
                    10001: u'\u773c\u90e8\u6574\u5f62',
                    10003: u'\u9f3b\u90e8\u6574\u5f62',
                    10006: u'\u9762\u90e8\u8f6e\u5ed3',
                    10007: u'\u5507\u90e8\u6574\u5f62',
                    10008: u'\u80f8\u90e8\u6574\u5f62',
                    10009: u'\u7f8e\u4f53\u5851\u5f62',
                    10010: u'\u76ae\u80a4\u7f8e\u5bb9',
                    10011: u'\u6297\u8870\u6297\u521d\u8001',
                    10012: u'\u79c1\u5bc6\u6574\u5f62',
                    10013: u'\u7259\u9f7f\u7f8e\u5bb9',
                    10015: u'\u6bdb\u53d1\u79cd\u690d',
                    10017: u'\u8033\u90e8\u6574\u5f62',
                    10018: u'\u5176\u4ed6',
                    10019: u'\u81ea\u4f53\u8102\u80aa',
                    10020: u'\u73bb\u5c3f\u9178',
                    10021: u'\u8089\u6bd2\u7d20',
                    10022: u'\u6fc0\u5149\u8131\u6bdb',
                    10023: u'\u534a\u6c38\u4e45\u5986'}

city = {1: u'\u5317\u4eac\u5e02',
                2: u'\u5929\u6d25\u5e02',
                9: u'\u4e0a\u6d77\u5e02',
                22: u'\u91cd\u5e86\u5e02',
                34: u'\u6fb3\u95e8\u7279\u522b\u884c\u653f\u533a',
                73: u'\u77f3\u5bb6\u5e84\u5e02',
                74: u'\u5510\u5c71\u5e02',
                75: u'\u79e6\u7687\u5c9b\u5e02',
                76: u'\u90af\u90f8\u5e02',
                77: u'\u90a2\u53f0\u5e02',
                78: u'\u4fdd\u5b9a\u5e02',
                79: u'\u5f20\u5bb6\u53e3\u5e02',
                80: u'\u627f\u5fb7\u5e02',
                81: u'\u8861\u6c34\u5e02',
                82: u'\u5eca\u574a\u5e02',
                83: u'\u6ca7\u5dde\u5e02',
                84: u'\u592a\u539f\u5e02',
                85: u'\u5927\u540c\u5e02',
                87: u'\u957f\u6cbb\u5e02',
                88: u'\u664b\u57ce\u5e02',
                90: u'\u664b\u4e2d\u5e02',
                91: u'\u8fd0\u57ce\u5e02',
                95: u'\u547c\u548c\u6d69\u7279\u5e02',
                96: u'\u5305\u5934\u5e02',
                98: u'\u8d64\u5cf0\u5e02',
                100: u'\u9102\u5c14\u591a\u65af\u5e02',
                107: u'\u6c88\u9633\u5e02',
                108: u'\u5927\u8fde\u5e02',
                109: u'\u978d\u5c71\u5e02',
                112: u'\u4e39\u4e1c\u5e02',
                113: u'\u9526\u5dde\u5e02',
                121: u'\u957f\u6625\u5e02',
                122: u'\u5409\u6797\u5e02',
                127: u'\u677e\u539f\u5e02',
                130: u'\u54c8\u5c14\u6ee8\u5e02',
                137: u'\u4f73\u6728\u65af\u5e02',
                139: u'\u7261\u4e39\u6c5f\u5e02',
                162: u'\u5357\u4eac\u5e02',
                163: u'\u65e0\u9521\u5e02',
                164: u'\u5f90\u5dde\u5e02',
                165: u'\u5e38\u5dde\u5e02',
                166: u'\u82cf\u5dde\u5e02',
                167: u'\u5357\u901a\u5e02',
                168: u'\u8fde\u4e91\u6e2f\u5e02',
                169: u'\u6dee\u5b89\u5e02',
                170: u'\u76d0\u57ce\u5e02',
                171: u'\u626c\u5dde\u5e02',
                172: u'\u9547\u6c5f\u5e02',
                173: u'\u6cf0\u5dde\u5e02',
                175: u'\u676d\u5dde\u5e02',
                176: u'\u5b81\u6ce2\u5e02',
                177: u'\u6e29\u5dde\u5e02',
                178: u'\u5609\u5174\u5e02',
                179: u'\u6e56\u5dde\u5e02',
                180: u'\u7ecd\u5174\u5e02',
                181: u'\u821f\u5c71\u5e02',
                182: u'\u8862\u5dde\u5e02',
                183: u'\u91d1\u534e\u5e02',
                184: u'\u53f0\u5dde\u5e02',
                186: u'\u5408\u80a5\u5e02',
                187: u'\u829c\u6e56\u5e02',
                188: u'\u868c\u57e0\u5e02',
                189: u'\u6dee\u5357\u5e02',
                190: u'\u9a6c\u978d\u5c71\u5e02',
                191: u'\u6dee\u5317\u5e02',
                193: u'\u5b89\u5e86\u5e02',
                195: u'\u6ec1\u5dde\u5e02',
                196: u'\u961c\u9633\u5e02',
                197: u'\u5bbf\u5dde\u5e02',
                199: u'\u516d\u5b89\u5e02',
                200: u'\u4eb3\u5dde\u5e02',
                201: u'\u6c60\u5dde\u5e02',
                203: u'\u798f\u5dde\u5e02',
                204: u'\u53a6\u95e8\u5e02',
                205: u'\u8386\u7530\u5e02',
                206: u'\u4e09\u660e\u5e02',
                207: u'\u6cc9\u5dde\u5e02',
                208: u'\u6f33\u5dde\u5e02',
                209: u'\u5357\u5e73\u5e02',
                210: u'\u9f99\u5ca9\u5e02',
                211: u'\u5b81\u5fb7\u5e02',
                212: u'\u5357\u660c\u5e02',
                214: u'\u840d\u4e61\u5e02',
                215: u'\u4e5d\u6c5f\u5e02',
                217: u'\u9e70\u6f6d\u5e02',
                218: u'\u8d63\u5dde\u5e02',
                219: u'\u5409\u5b89\u5e02',
                220: u'\u5b9c\u6625\u5e02',
                221: u'\u629a\u5dde\u5e02',
                222: u'\u4e0a\u9976\u5e02',
                223: u'\u6d4e\u5357\u5e02',
                224: u'\u9752\u5c9b\u5e02',
                225: u'\u6dc4\u535a\u5e02',
                226: u'\u67a3\u5e84\u5e02',
                227: u'\u4e1c\u8425\u5e02',
                228: u'\u70df\u53f0\u5e02',
                229: u'\u6f4d\u574a\u5e02',
                230: u'\u6d4e\u5b81\u5e02',
                231: u'\u6cf0\u5b89\u5e02',
                232: u'\u5a01\u6d77\u5e02',
                233: u'\u65e5\u7167\u5e02',
                235: u'\u4e34\u6c82\u5e02',
                236: u'\u5fb7\u5dde\u5e02',
                237: u'\u804a\u57ce\u5e02',
                239: u'\u83cf\u6cfd\u5e02',
                240: u'\u90d1\u5dde\u5e02',
                241: u'\u5f00\u5c01\u5e02',
                242: u'\u6d1b\u9633\u5e02',
                243: u'\u5e73\u9876\u5c71\u5e02',
                244: u'\u5b89\u9633\u5e02',
                246: u'\u65b0\u4e61\u5e02',
                247: u'\u7126\u4f5c\u5e02',
                248: u'\u6fee\u9633\u5e02',
                249: u'\u8bb8\u660c\u5e02',
                250: u'\u6f2f\u6cb3\u5e02',
                252: u'\u5357\u9633\u5e02',
                253: u'\u5546\u4e18\u5e02',
                254: u'\u4fe1\u9633\u5e02',
                256: u'\u9a7b\u9a6c\u5e97\u5e02',
                258: u'\u6b66\u6c49\u5e02',
                259: u'\u9ec4\u77f3\u5e02',
                260: u'\u5341\u5830\u5e02',
                261: u'\u5b9c\u660c\u5e02',
                262: u'\u8944\u6a0a\u5e02',
                263: u'\u9102\u5dde\u5e02',
                264: u'\u8346\u95e8\u5e02',
                265: u'\u5b5d\u611f\u5e02',
                266: u'\u8346\u5dde\u5e02',
                268: u'\u54b8\u5b81\u5e02',
                270: u'\u6069\u65bd\u571f\u5bb6\u65cf\u82d7\u65cf\u81ea\u6cbb\u5dde',
                271: u'\u4ed9\u6843\u5e02',
                272: u'\u6f5c\u6c5f\u5e02',
                273: u'\u5929\u95e8\u5e02',
                275: u'\u957f\u6c99\u5e02',
                276: u'\u682a\u6d32\u5e02',
                277: u'\u6e58\u6f6d\u5e02',
                278: u'\u8861\u9633\u5e02',
                279: u'\u90b5\u9633\u5e02',
                280: u'\u5cb3\u9633\u5e02',
                281: u'\u5e38\u5fb7\u5e02',
                283: u'\u76ca\u9633\u5e02',
                284: u'\u90f4\u5dde\u5e02',
                285: u'\u6c38\u5dde\u5e02',
                286: u'\u6000\u5316\u5e02',
                287: u'\u5a04\u5e95\u5e02',
                289: u'\u5e7f\u5dde\u5e02',
                290: u'\u97f6\u5173\u5e02',
                291: u'\u6df1\u5733\u5e02',
                292: u'\u73e0\u6d77\u5e02',
                293: u'\u6c55\u5934\u5e02',
                294: u'\u4f5b\u5c71\u5e02',
                295: u'\u6c5f\u95e8\u5e02',
                296: u'\u6e5b\u6c5f\u5e02',
                297: u'\u8302\u540d\u5e02',
                298: u'\u8087\u5e86\u5e02',
                299: u'\u60e0\u5dde\u5e02',
                301: u'\u6c55\u5c3e\u5e02',
                302: u'\u6cb3\u6e90\u5e02',
                304: u'\u6e05\u8fdc\u5e02',
                305: u'\u4e1c\u839e\u5e02',
                306: u'\u4e2d\u5c71\u5e02',
                310: u'\u5357\u5b81\u5e02',
                311: u'\u67f3\u5dde\u5e02',
                312: u'\u6842\u6797\u5e02',
                313: u'\u68a7\u5dde\u5e02',
                314: u'\u5317\u6d77\u5e02',
                318: u'\u7389\u6797\u5e02',
                324: u'\u6d77\u53e3\u5e02',
                325: u'\u4e09\u4e9a\u5e02',
                385: u'\u6210\u90fd\u5e02',
                386: u'\u81ea\u8d21\u5e02',
                387: u'\u6500\u679d\u82b1\u5e02',
                388: u'\u6cf8\u5dde\u5e02',
                389: u'\u5fb7\u9633\u5e02',
                390: u'\u7ef5\u9633\u5e02',
                392: u'\u9042\u5b81\u5e02',
                393: u'\u5185\u6c5f\u5e02',
                394: u'\u4e50\u5c71\u5e02',
                395: u'\u5357\u5145\u5e02',
                397: u'\u5b9c\u5bbe\u5e02',
                398: u'\u5e7f\u5b89\u5e02',
                399: u'\u8fbe\u5dde\u5e02',
                400: u'\u96c5\u5b89\u5e02',
                402: u'\u8d44\u9633\u5e02',
                406: u'\u8d35\u9633\u5e02',
                407: u'\u516d\u76d8\u6c34\u5e02',
                408: u'\u9075\u4e49\u5e02',
                410: u'\u94dc\u4ec1\u5730\u533a',
                414: u'\u9ed4\u5357\u5e03\u4f9d\u65cf\u82d7\u65cf\u81ea\u6cbb\u5dde',
                415: u'\u6606\u660e\u5e02',
                416: u'\u66f2\u9756\u5e02',
                419: u'\u662d\u901a\u5e02',
                424: u'\u7ea2\u6cb3\u54c8\u5c3c\u65cf\u5f5d\u65cf\u81ea\u6cbb\u5dde',
                427: u'\u5927\u7406\u767d\u65cf\u81ea\u6cbb\u5dde',
                438: u'\u897f\u5b89\u5e02',
                440: u'\u5b9d\u9e21\u5e02',
                441: u'\u54b8\u9633\u5e02',
                444: u'\u6c49\u4e2d\u5e02',
                446: u'\u5b89\u5eb7\u5e02',
                448: u'\u5170\u5dde\u5e02',
                462: u'\u897f\u5b81\u5e02',
                470: u'\u94f6\u5ddd\u5e02',
                475: u'\u4e4c\u9c81\u6728\u9f50\u5e02',
                478: u'\u54c8\u5bc6\u5730\u533a',
                493: u'\u53f0\u5317\u5e02',
                494: u'\u9ad8\u96c4\u5e02',
                496: u'\u53f0\u4e2d\u5e02',
                498: u'\u65b0\u7af9\u5e02',
                500: u'\u53f0\u5317\u53bf',
                502: u'\u6843\u56ed\u53bf',
                510: u'\u53f0\u5357\u53bf',
                516: u'\u4e2d\u897f\u533a',
                518: u'\u4e5d\u9f99\u57ce\u533a',
                523: u'\u6e7e\u4ed4\u533a',
                524: u'\u6cb9\u5c16\u65fa\u533a',
                556: u'\u97e9\u56fd',
                557: u'\u65b0\u52a0\u5761',
                560: u'\u6cf0\u56fd',
                561: u'\u65e5\u672c',
                45068: u'\u8944\u9633\u5e02',
                45070: u'\u65b0\u5317\u5e02'}
        
        
class ProductSpider(scrapy.Spider):
    name = 'product'
    allowed_domains = ['soyoung.com']
 

    custom_settings = {
        'ITEM_PIPELINES': {
            'research.pipelines.DuplicatesProduct': 100
        }
    }
    

    
    link='http://y.soyoung.com/yuehui/shop?district_id={}&menu1_id={}&sort=13&index=0'
    

    
    cat = [10020, 10021, 10010, 10001, 10003, 10006, 10019, 10008, 10009, 10011, 10013, \
           10023, 10022, 10015, 10012, 10007, 10017, 10018]
    large = [19, 1, 17, 9, 10, 11, 23, 18, 15, 16, 12, 22, 13, 6]
    small = [25, 27, 14, 3, 2, 556, 8, 20, 31, 7, 21, 4, 24, 28, 5, 32, 30, 33, 29, 561, 560, 34]    
    
    place = [186, 187, 188, 189, 190, 191, 193, 195, 196, 197, 199, 200, 201, 34, 1, 22, 203, 204, 205, 206, 207, 208, 209, 210, 211, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 301, 302, 304, 305, 306, 310, 311, 312, 313, 314, 318, 406, 407, 408, 410, 414, 448, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 130, 137, 139, 240, 241, 242, 243, 244, 246, 247, 248, 249, 250, 252, 253, 254, 256, 258, 259, 260, 261, 262, 263, 264, 265, 266, 268, 270, 271, 272, 273, 45068, 275, 276, 277, 278, 279, 280, 281, 283, 284, 285, 286, 287, 324, 325, 556, 557, 560, 561, 121, 122, 127, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 212, 214, 215, 217, 218, 219, 220, 221, 222, 107, 108, 109, 112, 113, 95, 96, 98, 100, 470, 462, 84, 85, 87, 88, 90, 91, 9, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 235, 236, 237, 239, 385, 386, 387, 388, 389, 390, 392, 393, 394, 395, 397, 398, 399, 400, 402, 438, 440, 441, 444, 446, 2, 493, 494, 496, 498, 500, 502, 510, 45070, 475, 478, 516, 518, 523, 524, 415, 416, 419, 424, 427, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184]
    
    
    swim = []

    #for i in small:
    #    swim.append(link.format(i, 0))

    for p in place:
        for c in cat:
            swim.append(link.format(p, c))      
    
    start_urls = swim
    print name, 'newest version, transverse all', len(start_urls)

    def parse(self, response):
        unitext = response.body_as_unicode()
        dic = json.loads(unitext)['responseData']
        
        flag = int(dic['has_more'])
        tol = int(dic['total'])

        base_url = response.url.split('index=')
        page = int(base_url[-1])
        
        coll = base_url[0].split('district_id=')[-1].split('&')
        district_id = coll[0]
        cat_id = coll[1].split('menu1_id=')[-1]
        
        cat_name = category[int(cat_id)]
        dis_name = city[int(district_id)]
        
        if tol==0:
            print dis_name, cat_name, 'no data'
            return
        
        products = dic['product_info']
        
        
        seq=0

        
        
        for product in products:
            seq+=1
            product['page_sequence']= page
            product['rank_sequence']= seq
            product['district_id'] = district_id
            product['cat_id'] = cat_id
            
            product['category'] = cat_name
            product['district_name'] = dis_name
            yield product        
        
        if flag:
            
            yield scrapy.Request(url = base_url[0] +'index='+ str(page+1), callback = self.parse)
            
            

