#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2017/11/23

class Pagination(object):
    """
    分页功能实现
    """

    def __init__(self, current_page, all_count, base_url, query_params, per_page=10, pager_page_count=11):
        """
        :param current_page: 当前页
        :param all_count: 数据总条数
        :param base_url: 分页的url
        :param query_params: 查询的参数，QueryDict.urlencode() # /arya/app01/userinfo/?q=web&page=5
        :param per_page: 每页显示的数据条数
        :param pager_page_count: 每页显示的页码数量
        """
        try:
            self.current_page = int(current_page)
            if self.current_page <= 0:
                raise Exception()
        except Exception as e:
            self.current_page = 1

        self.per_page = per_page
        self.all_count = all_count
        self.base_url = base_url
        self.query_params = query_params
        self.pager_page_count = pager_page_count
        pager_count, b = divmod(all_count, per_page)
        if b != 0:
            pager_count += 1
        self.pager_count = pager_count

        # 页码
        half_pager_page_count = int(pager_page_count / 2)
        self.half_pager_page_count = half_pager_page_count

    @property
    def start(self):
        """
        数据库获取值的起始索引位置
        :return:
        """
        return (self.current_page - 1) * self.per_page

    @property
    def end(self):
        """
        数据库获取值的结束索引位置
        :return:
        """
        return self.current_page * self.per_page

    def page_html(self):
        """
        渲染的HTML页码
        :return:
        """
        if self.pager_count < self.pager_page_count:
            pager_start = 1
            pager_end = self.pager_count
        else:
            # 数据较多，页码超过11，最少110条
            if self.current_page <= self.half_pager_page_count:
                pager_start = 1
                pager_end = self.pager_page_count
            else:
                # 如果当前页+5 > 总页码
                if (self.current_page + self.half_pager_page_count) > self.pager_count:
                    pager_start = self.pager_count - self.pager_page_count + 1
                    pager_end = self.pager_count
                else:
                    pager_start = self.current_page - self.half_pager_page_count
                    pager_end = self.current_page + self.half_pager_page_count

        page_list = []
        # 上一页
        if self.current_page <= 1:
            prev = '<li class="disabled"><a href="#" aria-label="Previous">上一页</a></li>'
        else:
            # prev = '<a href="%s?page=%s">上一页</a>' % (self.base_url, self.current_page - 1,)
            self.query_params['page'] = self.current_page - 1
            prev = '<li><a href="{base_url}?{params}" aria-label="Previous">上一页</a></li>'.format(
                    base_url=self.base_url, params=self.query_params.urlencode())
        page_list.append(prev)

        # 当前页
        for i in range(pager_start, pager_end + 1):
            self.query_params['page'] = i
            if self.current_page == i:
                tpl = '<li class="active"><a href="{base_url}?{params}">{num}</a></li>'.format(base_url=self.base_url,
                                                                                               params=self.query_params.urlencode(),
                                                                                               num=i)
            else:
                tpl = '<li><a href="{base_url}?{params}">{num}</a></li>'.format(base_url=self.base_url,
                                                                                params=self.query_params.urlencode(),
                                                                                num=i)
            page_list.append(tpl)

        # 下一页
        if self.current_page >= self.pager_count:
            # nex = '<a href="#">下一页</a>'
            nex = '<li class="disabled"><a href="#" aria-label="Next">下一页</a></li>'
        else:
            # nex = '<a href="%s?page=%s">下一页</a>' % (self.base_url, self.current_page + 1,)
            self.query_params['page'] = self.current_page + 1
            nex = '<li><a href="{base_url}?{params}" aria-label="Next">下一页</a></li>'.format(
                    base_url=self.base_url, params=self.query_params.urlencode())
        page_list.append(nex)
        page_str = "".join(page_list)
        return page_str
