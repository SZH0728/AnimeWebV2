# -*- coding:utf-8 -*-
# AUTHOR: Sun

from dataclasses import dataclass


@dataclass
class Pagination(object):
    pagination: dict[int, str]
    current: int


@dataclass
class LibraryArgs(object):
    year: int | None
    season: str | None
    vote: int | None


@dataclass
class BriefInfo(object):
    name: str  # 动画名称
    translation: str | None  # 动画译名

    description: str | None  # 动画描述信息

    detail_score: dict[str, dict[str, int | float]]  # 详细评分信息
    score: float  # 总评分
    vote: int  # 投票人数

    url: str  # 详情页面URL
    picture: str  # 封面图片URL


if __name__ == '__main__':
    pass
