# import time
import time

import urllib3, pytest
# from API_project.Configs.Config_Info import User_Config
from API_project.Configs.search_Api import search
# from API_project.conftest import ES
# import requests, pytest, os
from elasticsearch import Elasticsearch

urllib3.disable_warnings()

ES = Elasticsearch('es-cn-tl3280yva0001mwg8.public.elasticsearch.aliyuncs.com:9200',  # 最新地址，prod
                   http_auth=('mengyanhong', 'Aa123456'))
EStest = Elasticsearch('es-cn-i7m27x1em002z5u9d.public.elasticsearch.aliyuncs.com:9200',  # 最新地址，prod
                        http_auth=('tester', 'tester_Aa123456'))
es_client = Elasticsearch('es-cn-i7m27x1em002z5u9d.public.elasticsearch.aliyuncs.com:9200', #最新地址，test
                          http_auth=('tester', 'tester_Aa123456'))
HOST = "lxcrm"  # 设置测试环境 test:测试环境，staging:回归环境，lxcrm:正式环境
skb_search_configs = search(HOST)
pids = [
  "20f4f961949b35555952ad05014cfe17",
  "d6d48355d9924eb9a5b7016fb9a555b9",
  "b97eb186fd8d0d35641ff10813b968ce",
  "9d519640bda9c0936c00e757edf72341",
  "d7eff4932c1c8bbf3ce4718f2cac9f47",
  "6789253d4df7c5c838b2bf9eb9e0cef7",
  "6b4ada4388b5b8c08a09ea55c02bc739",
  "d11526837a250000947e24eca3e363da",
  "4f6ffe0f327b23c180be960230cbe5c3",
  "f60cb4c3819124bbf8d063e28202f4c8",
  "313e38596f17f81224601c18f559d68a",
  "8e6a02dc1896269343847c0959abf472",
  "526e1ba58e369761a7389a18c7d7bcb2",
  "22e5ae10f250214ccbbd15708a36e4b3",
  "221187c94636776243bff97d92d36b5c",
  "f81625969c4ce5f0b59f862673886078",
  "38b1b3f0344886daf2ec2179ea6a03ab",
  "5186ca6a985578cb4fc3f4a16f748520",
  "e5376fe088259044c36ee0778f840050",
  "51b3dceb5538d871c7f7c0f19537fc30",
  "d891a3fe09a039b055cf2919b277b69e",
  "83e750df9ebbf42c66688ae904b07b87",
  "d44b4a9fdd8f116338b8a3e661e93481",
  "d2cd188d8b27760ec8253b29e31fead7",
  "6bb3269673ac9068ba48f5eb02c29f5d",
  "ceeae640b09a69dc76853e6d8302cf30",
  "14ebc23935cd84347fcaebe78c58eca1",
  "7f48976826d511dd977e4498914f7ba4",
  "257cc018a9e5051096fa9ada8f1d5ab0",
  "9cd6ebe074441fa5070977fbf26f16b9",
  "12b3a5298c9f2aba9b7a60465debddac",
  "b352e1077d59f734dcc038bd2b2b6745",
  "917b39daac5c7a9dfe74823e3db11fbe",
  "399a2f3025e01276ae0e375dd2428f4e",
  "1ed80d7db5072e7d3202fe0c51128e42",
  "1779b12972a4ea6ba2475c2d45cb3f37",
  "ffca317629aa8cef7f8d212516bd59e2",
  "ec3c40a823e3c3276843b4edd43fdda9",
  "6982cac6a22ba9c0cb4996f7b5c3ee5e",
  "afe3b734cd6de34dde334010cea14b72",
  "6206c51f5bdd07eb987437e316d0c095",
  "d8b395cb3b835c0b46d9a0bc11e3d74b",
  "015abcf517c900ffea5bb588916afa00",
  "67b2be5339006040830c4a3bcacd1a2c",
  "26bc36b6cd3060c0d4c31b175ee9dee7",
  "924cc637120d331e06f5c2ca1d4922e2",
  "147d4c5607ddec392bc7a65484b450e6",
  "87f52d73c1cc0eba77d91001dc6b4b54",
  "b5f538e96c25e77909562fcab53b3cb9",
  "1793fdcbd65e32d0b04ca7281536d79e",
  "4bbb151b60925456e93a3f09692f0940",
  "f11bd4e23c454ee621802ddc1b64d2af",
  "d6eaea81d9a1f1a4704b03e703c38b17",
  "d56d4a3cae338dff27410d11b7915442",
  "a93320cd5870f7ba6b0ae3345b302847",
  "6c64d6f379ff70996739208a12dfc6d0",
  "ba2a2ddcade80fcfa88bb1fe047cf753",
  "94a3f6f2931dc27de50ace28aa66dd07",
  "7a0ffcf4e910b6aa311831174e2acff7",
  "cc6d72b6f8102d83d90e824a946f54ed",
  "1c0fc50b89933b2756922e7f62799fcd",
  "b617cb2aed05be6f7908cfec41c3e7a7",
  "e9eccdb186aba1dbc25dddedecd919a4",
  "97d704c5c5b079fa205f1c49f14c0655",
  "7436271d70247f7167032cb3c01a9805",
  "fa2a18f2d2005bf7e00c24d04af83a74",
  "c1fe737b2b2aa935bb620e13d9ccdf8b",
  "7b9a4af3e4ee2bc196a546ad1248b3c1",
  "483be78478801acaf31944adef7f9b14",
  "db8d8da07f602f22744b36491b3e7df7",
  "3246b7d45c897eeb2a03a75a8dafec7f",
  "000360545ae5bbd94770d0cdaf659af2",
  "5dbaff6ce075902559d7dacf246e2852",
  "9748280a5c6c57958f9ce3609d0328bc",
  "ccc7bb53a1e48ffcb1812bd2f207c408",
  "ef9c66fd5ad8ff76f3a855ccd731d479",
  "a8ac63416ed92b72252b6ca7dac0bd93",
  "bf8831060668b407b00653c11e7d84ad",
  "73406cec7cbe5274f5a2e6fedfd0dd6a",
  "befba391db1956959088e1bd08551d39",
  "8a520ece47f182d0e05b691cba4bbf3e",
  "5728177656c9a9b70d29c3cf931ab128",
  "7e998861731fede3abcba6d009ab658b",
  "3b1ca01bc81d8327823236c08afe7f42",
  "ad06f6af2e270d35a1451c1eeda20257",
  "fa60af73d2b227bb135b05f4054c41c8",
  "db1c033bf47ef82b710fe5bb85fa61d5",
  "607c0f1c7e9d28a3ed56933cfc52b48c",
  "fb45dd6edc65de7ba5a3d56a6054cbb9",
  "c54ed0e7dbdba3eeda17e7e467353906",
  "96e8b8f3df3f876d1749bccac799bfa1",
  "293405e2d85205c85a562608ba58550e",
  "63bc67f0d53ecb940473f04e88f383da",
  "f5b50476c823522f4d6ee23de5412e43",
  "49db4c7beb3800162331619df8189a07",
  "c70e17d79addff403999eb50e09a2356",
  "6fc0f23e3363fd8c996d8b77021ac585",
  "c2236072935cd8ed554546b7dc769ab5",
  "8f200c18b8b5c9a7984a0ed63a97ac85",
  "a59a23f22494a04367829ebf326a73ae"
]
shoppids = [
  "76737494",
  "8851693",
  "124935987",
  "68524646",
  "1575575266",
  "1452631999",
  "627005263",
  "122787802",
  "99954858",
  "49427586",
  "6860632",
  "80017969",
  "682816899",
  "981648208",
  "125366059",
  "1197422509",
  "68271623",
  "96475760",
  "1816994229",
  "10580072",
  "121482884",
  "1727363877",
  "131404933",
  "113957395",
  "527309753",
  "1502547507",
  "40116523",
  "68791965",
  "22588890",
  "795300008",
  "127605302",
  "69396716",
  "731476520",
  "98885617",
  "123373283",
  "823658911",
  "131325826",
  "64974342",
  "13713656",
  "9498075",
  "63269593",
  "1273087510",
  "65141551",
  "1820193922",
  "40647833",
  "1599235772",
  "58576217",
  "40343236",
  "69714442",
  "65847207",
  "66042570",
  "27168298",
  "961342101",
  "66732292",
  "126306849",
  "1100602214",
  "8436432",
  "528924420",
  "1065262043",
  "65581216",
  "32475736",
  "72353730",
  "69523608",
  "5229233",
  "32326294",
  "745452287",
  "1045772028",
  "72310504",
  "124957564",
  "39937361",
  "111794900",
  "124981425",
  "1791754567",
  "66715208",
  "120028110",
  "131867163",
  "1857920704",
  "125387354",
  "112003540",
  "103427649",
  "1810641893",
  "68822716",
  "5698522",
  "126546219",
  "68222541",
  "132615595",
  "5698701",
  "125768157",
  "5432489",
  "128587486",
  "123601380",
  "1205036331",
  "57021516",
  "5345731",
  "19273036",
  "1201323180",
  "1570499173",
  "93184835",
  "106766785",
  "629697086"
]
oid = "11603425"
class Test_clues_sync:
    @pytest.mark.parametrize("oid", [oid])
    @pytest.mark.parametrize("pid", pids[:0:-1])
    @pytest.mark.parametrize("indexs", ["company_info_prod"])  # "company_info_prod","shop_info_prod"
    def test_Es_search_clues(self, pid, oid, indexs):
        time.sleep(1)
        # if indexs == "shop_info_prod":
        #     es_result = EStest.get(index=indexs, id=pid)['_source']
        # else:
        es_result = ES.get(index=indexs, id=pid)['_source']
        # if oid not in es_result["transferredClueOrgsNonProd"]:
        #     print("转线索失败，oid,{},pid,{}".format(oid, pid))
        # if oid not in es_result["unfoldedOrgsNonProd"]:
        #     print("查看失败，oid,{},pid,{}".format(oid, pid))
        # assert oid in es_result["transferredClueOrgsNonProd"]
        # assert oid in es_result["unfoldedOrgsNonProd"]
        if oid not in es_result["transferredClueOrgs"]:
            print("转线索失败，oid,{},pid,{}".format(oid, pid))
        if oid not in es_result["unfoldedOrgs"]:
            print("查看失败，oid,{},pid,{}".format(oid, pid))
        assert oid in es_result["transferredClueOrgs"]
        assert oid in es_result["unfoldedOrgs"]

    @pytest.mark.parametrize("oid", [oid])
    @pytest.mark.parametrize("pid", shoppids[:50:])
    @pytest.mark.parametrize("indexs", ["shop_info_prod"])  # "company_info_prod","shop_info_prod"
    def test_Es_search_shopclues(self, pid, oid, indexs):
        time.sleep(1)
        # if indexs == "shop_info_prod":
        #     es_result = EStest.get(index=indexs, id=pid)['_source']
        # else:
        es_result = ES.get(index=indexs, id=pid)['_source']
        # if oid not in es_result["transferredClueOrgsNonProd"]:
        #     print("转线索失败，oid,{},pid,{}".format(oid, pid))
        # if oid not in es_result["unfoldedOrgsNonProd"]:
        #     print("查看失败，oid,{},pid,{}".format(oid, pid))
        # assert oid in es_result["transferredClueOrgsNonProd"]
        # assert oid in es_result["unfoldedOrgsNonProd"]
        if oid not in es_result["transferredClueOrgs"]:
            print("转线索失败，oid,{},pid,{}".format(oid, pid))
        if oid not in es_result["unfoldedOrgs"]:
            print("查看失败，oid,{},pid,{}".format(oid, pid))
        assert oid in es_result["transferredClueOrgs"]
        assert oid in es_result["unfoldedOrgs"]

# if __name__ == '__main__':
#     print(Test_search().contacts_num_search(pid="af7d4ceeec233412790bad11f9016be1", entName="广州旭众食品机械有限公司"))
