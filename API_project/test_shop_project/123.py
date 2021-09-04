# @Time : 2021/8/19 11:44
# @Author : 孟艳红
# @File : 123.py
def test_e(ES):
    ES = ES
    print(ES)
    try:
        es_result = ES.get(index="shop_info_prod", id=1065324918973120)['_source']
    except :
        es_result = None
    print(es_result)



