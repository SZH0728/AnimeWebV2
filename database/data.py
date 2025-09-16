# -*- coding:utf-8 -*-
# AUTHOR: Sun

from dataclasses import dataclass
from datetime import date


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
    id: int  # 主键ID，自增

    name: str  # 动画名称
    translation: str | None  # 动画译名

    description: str | None  # 动画描述信息

    detail_score: dict[str, dict[str, int | float]]  # 详细评分信息
    score: float  # 总评分
    vote: int  # 投票人数

    url: str  # 详情页面URL
    picture: str  # 封面图片URL


@dataclass
class DetailInfo(object):
    id: int  # 主键ID，自增

    name: str  # 动画名称
    translation: str | None  # 动画译名
    all: list[str] | None  # 所有名称组成的字符串数组

    time: date | None  # 发布日期
    tag: list[str] | None  # 标签信息，以字符串数组格式存储
    description: str | None  # 动画描述信息

    url: str  # 目标网站URL
    picture: str | None  # 封面图片URL

    # 详细评分信息，存储各平台评分和投票人数，示例: {'Bangumi': [8.3, 13284], 'MyAnimeList': [8.73, 1464542]}
    detail_score: dict[str, dict[str, int | float]] | None
    score: float | None  # 总评分
    vote: int | None  # 投票人数


@dataclass
class ScoreListItem(object):
    # 详细评分信息，存储各平台评分和投票人数，示例: {'Bangumi': [8.3, 13284], 'MyAnimeList': [8.73, 1464542]}
    detail_score: dict[str, dict[str, int | float]] | None
    score: float | None  # 总评分
    vote: int | None  # 投票人数

    date: date | None  # 评分日期


if __name__ == '__main__':
    pass
