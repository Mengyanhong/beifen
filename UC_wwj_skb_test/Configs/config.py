class HOST:
    @classmethod
    def search_fin_dev(self):
        return 'skb-dev.weiwenjia.com'
    @classmethod
    def search_fin_test(self):
        return 'skb-test.weiwenjia.com'
    @classmethod
    def search_fin_staging(self):
        return 'skb-staging.weiwenjia.com'
    @property
    def search_fin(self):
        return 'skb.weiwenjia.com'
if __name__ == '__main__':
    a= HOST.search_fin_test()
    print(a)