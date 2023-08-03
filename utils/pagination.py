"""
self made page tool
"""
from django.utils.safestring import mark_safe

class Pagination(object):

    def __init__(self,request,queryset,search_data):
        """
        :param request: web request
        :param queryset: list of data that satisfy searching criteria
        :param search_data: web searching request
        """
        page = request.GET.get('page',"1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        self.page = page
        self.page_size = 5

        self.start = (page - 1) * self.page_size
        self.end = page * self.page_size

        self.queryset = queryset[self.start:self.end]
        self.search_data = search_data

        self.total_count = queryset.count()
        self.total_page_count, div = divmod(self.total_count,self.page_size)

        if div:
            self.total_page_count += 1

        print(self.total_count)

    def html(self):
        page_str_list = []
        plus = 5
        if self.page <= plus:
            cur = 1
            end = min(self.page + plus,self.total_page_count)
        elif self.page + plus >= self.total_page_count:
            cur = self.page - plus
            end = self.total_page_count
        else:
            cur = max(self.page - plus,1)
            end = self.page + plus
        if self.page > 1:
            prev = '<li><a href="?page={}&q={}">上一页</a></li>'.format(self.page - 1, self.search_data)
            page_str_list.append(prev)
        for i in range(cur, end + 1):
            if i == self.page:
                ele = '<li class="active"><a href="/num/list?page={}&q={}">{}</a></li>'.format(i, self.search_data, i)
            else:
                ele = '<li><a href="?page={}&q={}">{}</a></li>'.format(i, self.search_data, i)
            page_str_list.append(ele)

        if self.page < self.total_page_count:
            end = '<li><a href="?page={}&q={}">下一页</a></li>'.format(self.page + 1, self.search_data)
            page_str_list.append(end)
        searchStr = '''
            <li>
                            <form style="float:left;margin-left: -1px"method="get">
                                <input name="page" style="position: relative; float: left;display: inline-block;width: 80px;border-radius: 0;"
                                type="text" class="form-control"placeholder="page">
                                <button style="border-radius: 0" class="btn btn-default" type="submit">go</button>

                            </form>
                        </li>
            '''
        page_str_list.append(searchStr)
        page_string = mark_safe(''.join(page_str_list))
        return page_string