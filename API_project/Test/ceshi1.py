# zimu= "ABCSDEFGHIJKLMNOPQRSTUVWXYZ"
# zi= "CD"
# result = zi in zimu
# print(result)
# lat="31.113987"
# lon="121.276459"
# print(lat.split('.')[0])
import requests

class Newinsight:
    def __init__(self, test):
        self.user = test

    def list_msg(self, id):
        url = r'https://newinsight.videojj.com/backend/api/sensitive/category/list?'
        params = {'category_name': '政治类',
                  'enabled': 0,
                  'gmt_created': '2021-11-24 10:56:11',
                  'gmt_modified': '2021-11-24 10:56:11',
                  'id': 'id',
                  'level': 0,
                  'parent_id': 0,
                  }
        headers = {
            'authorization': 'eyJhbGciOiJIUzUxMiJ9'
                             '.eyJsb2dpbl91c2VyX2tleSI6IjkxMWE1OWNhLTQwNTAtNDE0YS05ZTA1LTM1OTJkZTFmMmY0YiJ9'
                             '.pI6695Bn8ugKSWK5DtuYq4jBa0UV8Dy7_CD2nvcuZGWI-UnXUeOF5lzDMprYrKjYeQHhTYCc-b4DZ3iqHW8Pbw',
            'cookie': 'UM_distinctid=17af60146da998-0108e5a55f564a-34627601-1fa400-17af60146db164; '
                      'Hm_lvt_2ede15e90c9e9195590577aefe09db08=1636363703; '
                      'Hm_lpvt_2ede15e90c9e9195590577aefe09db08=1636363703; '
                      'shenyan_token=eyJhbGciOiJIUzUxMiJ9'
                      '.eyJsb2dpbl91c2VyX2tleSI6IjkxMWE1OWNhLTQwNTAtNDE0YS05ZTA1LTM1OTJkZTFmMmY0YiJ9'
                      '.pI6695Bn8ugKSWK5DtuYq4jBa0UV8Dy7_CD2nvcuZGWI-UnXUeOF5lzDMprYrKjYeQHhTYCc-b4DZ3iqHW8Pbw',
            'sec-ch-ua-platform': 'macOS', }
        er = requests.get(url=url, params=params, headers=headers)
        return er.json()


if __name__ == '__main__':
    print(Newinsight("test").list_msg(id='48'))
