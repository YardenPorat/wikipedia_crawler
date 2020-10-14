import urllib.request


class Crawler:
    def __init__(self, url):
        self.name = 'Wikipedia Crawler'
        self.url = url
        self.url_start = 'https://en.wikipedia.org/wiki/'
        self.cleaner = ['#', 'class=', ':', '=', 'Category', '/']

    def parse(self):
        link_data = urllib.request.urlopen(self.url)
        my_file = str(link_data.read())

        # clean before start and after end
        start = my_file.index('bodyContent')
        end = my_file.index('mw-data-after-content')
        my_file = my_file[start:end]

        # split to a list
        lst = my_file.split(r'href=')
        lst2 = []
        for segment in lst:
            separator = '"'
            cutoff = self.find_2nd(segment, separator)
            lst2.append(segment[:cutoff])

        lst = []
        for page in lst2:
            separator = '/'
            cutoff = self.find_2nd(page, separator)
            page = page[cutoff + 1:]
            if any(clean in page for clean in self.cleaner):
                continue
            else:
                lst.append(page)
        print(lst)

        # put in dict
        res = {}
        for item in lst:
            res[item] = self.url_start+item

        return res

    def find_2nd(self, string, substring):
        return string.find(substring, string.find(substring) + 1)


f = Crawler("https://en.wikipedia.org/wiki/Misliya_cave")
print(f.parse())
