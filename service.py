# -*- coding:utf-8 -*-
# AUTHOR: Sun

"""
@file service.py
@brief 服务层模块，提供数据查询和分页功能
@details 包含QueryService和PaginationService两个主要服务类，用于处理数据库查询和分页操作
"""

from typing import Iterable

from sqlalchemy import desc, and_

from model import DB, Detail, Score, Web
from constant import ENABLE_INNER_PICTURE
from data import BriefInfo, DetailInfo, Pagination


class WebIDMap(object):
    """
    @brief Web标识映射类，用于维护Web名称和ID之间的双向映射关系

    该类提供了根据Web名称查找ID或根据ID查找名称的功能，
    通过维护两个字典实现高效的双向查找。
    """

    def __init__(self, web_items: Iterable[Web] = None):
        """
        @brief 初始化WebIDMap实例

        @param web_items: 可选的Web对象迭代器，用于初始化映射关系
        """
        self._name_to_id: dict[str, str] = {}
        self._id_to_name: dict[str, str] = {}

        if web_items:
            self.flash(web_items)

    def flash(self, web_items: Iterable[Web]):
        """
        @brief 批量更新名称和ID的映射关系

        遍历Web对象列表，为每个Web对象建立名称到ID以及ID到名称的映射关系。

        @param web_items: Web对象的迭代器
        """
        for web in web_items:
            self._name_to_id[web.name] = str(web.id)
            self._id_to_name[str(web.id)] = web.name

    def get_id_by_name(self, name: str) -> str | None:
        """
        @brief 根据Web名称获取对应的ID

        @param name: Web名称
        @return: 对应的ID，如果未找到则返回None
        """
        return self._name_to_id.get(name, None)

    def get_name_by_id(self, wid: str) -> str | None:
        """
        @brief 根据Web ID获取对应的名称

        @param wid: Web ID
        @return: 对应的名称，如果未找到则返回None
        """
        return self._id_to_name.get(wid, None)


class QueryService(object):
    """
    @class QueryService
    @brief 数据查询服务类
    @details 提供基础的数据库三表联查、条件过滤、排序和结果转换功能
    """
    @staticmethod
    def base_query():
        """
        @brief 基础三表联结查询
        @details 连接Detail、Score、Web三张表，返回查询对象
        @return query(Detail, Score, Web) 查询对象
        """
        return (
            DB.session.query(Detail, Score, Web)
            .join(Score, Detail.id == Score.detailId)
            .join(Web, Detail.web == Web.id)
        )

    @staticmethod
    def apply_filters(query, aid: int | None=None, year: int | None=None, season: str | None=None, min_vote: int | None=None, on_date: str | None=None, keyword: str | None=None):
        """
        @brief 统一添加筛选条件
        @details 根据提供的参数对查询对象添加相应的过滤条件
        @param query 查询对象
        @param aid 详情ID过滤条件
        @param year 年份过滤条件
        @param season 季度过滤条件，可选值: 'spring','summer','autumn','winter'
        @param min_vote 最小评分过滤条件
        @param on_date 日期过滤条件
        @param keyword 关键字搜索条件，在Detail.all JSON中搜索
        @return 添加过滤条件后的查询对象
        """
        filters = []

        if aid:
            filters.append(Detail.id == aid)

        if year:
            filters.append(Detail.year == year)

        if season:
            filters.append(Detail.season == season)

        if min_vote:
            filters.append(Score.vote >= min_vote)

        if on_date:
            filters.append(Score.date == on_date)

        if keyword:
            filters.append(DB.func.json_search(Detail.all, 'one', f'%{keyword}%').is_not(None))

        if filters:
            query = query.filter(and_(*filters))

        return query

    @staticmethod
    def order_by_score_desc(query):
        """
        @brief 按评分降序排列
        @details 对查询结果按Score.score字段进行降序排序
        @param query 查询对象
        @return 排序后的查询对象
        """
        return query.order_by(desc(Score.score), desc(Score.vote))

    @staticmethod
    def count(query):
        """
        @brief 对查询结果进行计数
        @details 对已有过滤后的查询进行count操作
        @param query 查询对象
        @return int 查询结果总数
        """
        # SQLAlchemy 会生成合适的 COUNT 子查询
        return query.count()

    @staticmethod
    def set_picture_url(detail: Detail) -> str:
        # 修正 picture 构造以避免 '//' + None 的问题
        picture = ''

        # 若设置为内部图片
        if ENABLE_INNER_PICTURE:
            picture = f'/picture/{detail.id}'

        if not picture and detail.picture:
            # 若已包含协议头或双斜杠，原样使用；否则补齐协议相对 URL
            if detail.picture.startswith('http://') or detail.picture.startswith('https://') or detail.picture.startswith('//'):
                picture = detail.picture
            else:
                picture = f'//{detail.picture}'

        return picture

    @staticmethod
    def to_brief_list(rows: list[tuple[Detail, Score, Web]]) -> list[BriefInfo]:
        """
        @brief 将查询结果转换为简要信息列表
        @details 将(Detail, Score, Web)的结果集转换为BriefInfo对象列表
        @param rows (Detail, Score, Web)元组列表
        @return BriefInfo列表
        """
        result = []
        for detail, score, web in rows:
            picture = QueryService.set_picture_url(detail)

            info = BriefInfo(
                id=detail.id,

                name=detail.name,
                translation=detail.translation,

                description=detail.description,

                detail_score=score.detailScore or {},
                score=float(score.score) if score.score else 0.0,
                vote=score.vote or 0,

                url=f'/detail/{detail.id}',
                picture=picture
            )
            result.append(info)
        return result

    @staticmethod
    def to_detail_object(detail: Detail, score: Score, web: Web, map: WebIDMap) -> DetailInfo:
        """
        @brief 将Detail、Score、Web三个对象转换为DetailInfo对象
        @details 将数据库中的Detail、Score、Web三个实体对象整合转换为前端使用的DetailInfo对象
        @param detail Detail对象，包含动漫详细信息
        @param score Score对象，包含评分相关信息
        @param web Web对象，包含网站信息
        @param map WebIDMap对象，用于将Web ID转换为名称
        @return 整合后的DetailInfo对象
        """
        picture = QueryService.set_picture_url(detail)

        detail_score: dict[str, dict[str, int | float]] = {}
        for key,value in score.detailScore.items():
            detail_score[map.get_name_by_id(key)] = value

        info = DetailInfo(
            id=detail.id,

            name=detail.name,
            translation=detail.translation,
            all=detail.all,

            time=detail.time,
            tag=detail.tag,
            description=detail.description,

            url=f'https://{web.host}{web.format.format(detail.webId)}',
            picture=picture,

            detail_score=detail_score,
            score=float(score.score) if score.score else 0.0,
            vote=score.vote or 0
        )

        return info

class PaginationService(object):
    """
    @class PaginationService
    @brief 分页服务类
    @details 提供数据分页和分页链接生成功能
    """
    @staticmethod
    def paginate(query, page: int, per_page: int):
        """
        @brief 对查询结果进行分页
        @details 根据页码和每页数量对查询结果进行分页处理
        @param query 查询对象
        @param page 页码，从1开始
        @param per_page 每页显示数量
        @return tuple(items, total_count, total_pages) 分页结果元组
        """
        if page < 1:
            page = 1
        offset = (page - 1) * per_page
        total_count = QueryService.count(query)
        items = query.offset(offset).limit(per_page).all()
        total_pages = (total_count + per_page - 1) // per_page
        return items, total_count, total_pages

    @staticmethod
    def build_pagination_links(total_pages: int, current_page: int, build_url):
        """
        @brief 生成分页链接
        @details 根据总页数和当前页码生成分页链接字典
        @param total_pages 总页数
        @param current_page 当前页码
        @param build_url 可调用对象，接收页码p，返回该页链接
        @return Pagination 分页对象或None(当总页数小于等于1时)
        """
        if total_pages <= 1:
            return None

        pagination_dict = {}
        for p in range(1, total_pages + 1):
            pagination_dict[p] = build_url(p)
        return Pagination(pagination=pagination_dict, current=current_page)


if __name__ == '__main__':
    pass
