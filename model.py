# -*- coding:utf-8 -*-
# AUTHOR: Sun

# -*- coding:utf-8 -*-
# AUTHOR: Sun

from dataclasses import dataclass

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import YEAR, TINYINT


DB = SQLAlchemy()
Base = DB.Model


class Detail(DB.Model):
    __tablename__ = 'detail'

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)  # 主键ID，自增

    name = DB.Column(DB.String(64), nullable=False)  # 动画名称
    translation = DB.Column(DB.String(64))  # 动画译名
    all = DB.Column(DB.JSON)  # 所有名称组成的JSON字符串数组

    year = DB.Column(YEAR)  # 发布年份
    season = DB.Column(DB.Enum('spring', 'summer', 'autumn', 'winter'))  # 发布季节

    time = DB.Column(DB.Date)  # 发布日期
    tag = DB.Column(DB.JSON)  # 标签信息，以JSON字符串数组格式存储
    description = DB.Column(DB.Text)  # 动画描述信息

    web = DB.Column(TINYINT)  # 来源网站ID
    webId = DB.Column(DB.Integer)  # 在来源网站的ID

    picture = DB.Column(DB.String(128))  # 封面图片URL

    # 添加索引
    __table_args__ = (
        DB.Index('index_year_season', 'year', 'season'),
    )


class Score(DB.Model):
    __tablename__ = 'score'

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)  # 主键ID，自增
    detailId = DB.Column(DB.Integer)  # 关联的Detail表ID

    detailScore = DB.Column(DB.JSON)  # 详细评分信息，以JSON格式存储
    score = DB.Column(DB.DECIMAL(4, 2))  # 总评分
    vote = DB.Column(DB.Integer)  # 投票人数

    date = DB.Column(DB.Date)  # 评分日期


class Web(DB.Model):
    __tablename__ = 'web'

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)  # 主键ID，自增

    name = DB.Column(DB.String(16))  # 网站名称
    host = DB.Column(DB.String(16))  # 网站主机地址

    format = DB.Column(DB.String(16))  # 网站URL格式

    priority = DB.Column(TINYINT)  # 网站优先级


class Cache(DB.Model):
    __tablename__ = 'cache'

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)  # 主键ID，自增

    name = DB.Column(DB.String(64))  # 动画名称
    translation = DB.Column(DB.String(64))  # 动画译名
    all = DB.Column(DB.JSON)  # 所有相关信息的JSON格式存储

    year = DB.Column(YEAR)  # 发布年份
    season = DB.Column(DB.Enum('spring', 'summer', 'autumn', 'winter'))  # 发布季节

    time = DB.Column(DB.Date)  # 发布日期
    tag = DB.Column(DB.JSON)  # 标签信息，以JSON格式存储
    description = DB.Column(DB.Text)  # 动画描述信息

    score = DB.Column(DB.DECIMAL(4, 2))  # 评分
    vote = DB.Column(DB.Integer)  # 投票人数
    date = DB.Column(DB.Date, nullable=False)  # 缓存日期

    web = DB.Column(TINYINT)  # 来源网站ID
    webId = DB.Column(DB.Integer)  # 在来源网站的ID

    picture = DB.Column(DB.String(128))  # 封面图片URL


if __name__ == '__main__':
    pass
