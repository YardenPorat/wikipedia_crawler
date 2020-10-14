import requests


class Crawler:
    NAME = 'Wikipedia Crawler'
    URL_START = 'https://en.wikipedia.org/wiki/'
    CLEANER = ['#', 'class=', ':', '=', 'Category', '/']

    def __init__(self, url):
        self.url = url

    @staticmethod
    def get_page_content(url):
        response = requests.get(url)
        return response.text

    @staticmethod
    def cut_relevant_part(content):
        # clean before start and after end
        start = content.index('bodyContent')
        end = content.index('mw-data-after-content')
        return content[start:end]

    def extract_refs(self, content):

        lst = content.split(r'href=')
        lst2 = []
        HREF_SEPARATOR = '"'

        for segment in lst:
            cutoff = self.find_2nd(segment, HREF_SEPARATOR)
            lst2.append(segment[:cutoff])

        lst = []

        URL_SEPARATOR = '/'
        for page in lst2:
            cutoff = self.find_2nd(page, URL_SEPARATOR)
            page = page[cutoff + 1:]
            if any(clean in page for clean in self.CLEANER):
                continue
            else:
                lst.append(page)
        return lst

    def insert_to_dict(self, refs):
        # put in dict
        res = {}
        for item in refs:
            res[item] = self.URL_START + item
        return res

    def parse(self):
        print(f'{self.NAME} started!')
        content = self.get_page_content(self.url)
        topic_body_content = self.cut_relevant_part(content)
        refs = self.extract_refs(topic_body_content)
        res = self.insert_to_dict(refs)

        print(f'{self.NAME} finished!')
        return res

    @staticmethod
    def find_2nd(string, substring):
        return string.find(substring, string.find(substring) + 1)


if __name__ == '__main__':
    f = Crawler("https://en.wikipedia.org/wiki/Misliya_cave")
    print(f.parse())
