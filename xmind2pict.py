# -*- coding: utf-8 -*-

import zipfile
import xml.etree.ElementTree as ET

#xmindファイル名
filename = 'sample.xmind.'

#因子をキーにして水準を格納する
dic = {}

#idをキーにして因子水準のペアを格納する。
dic2 = {}

#制約の方向
condition_list = []

def do():
    with zipfile.ZipFile(filename, 'r') as file:
        with file.open('content.xml') as f:
            c = f.read()
            root = ET.fromstring(c)

    return root

# マーカを探す
def parse(element, indent):
    indent = "+" + indent
    
    #markerrefを探す。
    for child in element:
        if child.tag == '{urn:xmind:xmap:xmlns:content:2.0}marker-refs' :
            marker_extract(element)
        elif child.tag == '{urn:xmind:xmap:xmlns:content:2.0}relationships':
            relation_extract(element) 
        else:
            parse(child, indent)


def marker_extract(element):
    tag = element.find('{urn:xmind:xmap:xmlns:content:2.0}title').text
    list = []
    children = element.find('{urn:xmind:xmap:xmlns:content:2.0}children')
    topics = children.find('{urn:xmind:xmap:xmlns:content:2.0}topics')
    for topic in topics:
        
        title = topic.find('{urn:xmind:xmap:xmlns:content:2.0}title').text
        id = topic.attrib
        dic2[id['id']] = [tag, title]
        list.append(title)
    dic[tag] = list


def relation_extract(element):
    relations= element.find('{urn:xmind:xmap:xmlns:content:2.0}relationships')
    for relation in relations:
        fromid = relation.attrib['end1']
        toid = relation.attrib['end2']
        condition_list.append([fromid, toid])


if __name__ == '__main__':

    r = do()
    parse(r, "")
    
    #要素出力
    for key in dic.keys():
        col = key + ": "
        i = 0
        for item in dic[key]:
            i = i + 1
            col = col + item
            if i != len(dic[key]):
              col = col + ","
        print (col)
 
    # 制約出力
    
    for condition in condition_list:
        from_factor = dic2[condition[0]][0]
        from_level =  dic2[condition[0]][1]
        to_factor = dic2[condition[1]][0]
        to_level =  dic2[condition[1]][1]
        print('IF [' + from_factor + '] = "' + from_level + '" THEN [' + to_factor + '] = "' + to_level + '";')

