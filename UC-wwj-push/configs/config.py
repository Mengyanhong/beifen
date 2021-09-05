class HOST:
    @classmethod
    def search_fin_dev(self):
        return 'skb-dev.weiwenjia.com'

    @classmethod
    def search_fin_test(self):
        return 'skb-test.weiwenjia.com'

    @classmethod
    def search_fin(self):
        return 'skb.weiwenjia.com'
if __name__ == '__main__':
    print(HOST().search_fin())