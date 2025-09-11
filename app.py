# -*- coding:utf-8 -*-
# AUTHOR: Sun

from datetime import datetime

from flask import Flask, request, url_for, abort
from flask import send_from_directory, send_file, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

from constant import DB_URI, ENABLE_INNER_PICTURE, PICTURE_PATH
from model import DB, Score
from data import LibraryArgs
from service import QueryService, PaginationService

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,  # 每次使用连接前先ping一下，检查连接是否有效
    'echo': False,  # 输出 SQL
}

DB.init_app(app)

limiter = Limiter(get_remote_address, app=app)
cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_THRESHOLD': 16})


@app.route('/')
@cache.cached(timeout=300)
def index():
    # 参数
    min_vote = 1000
    max_number = 20

    # 计算当天的评分日期
    latest_date = DB.session.query(DB.func.max(Score.date)).scalar()
    if not latest_date:
        # 无评分数据时直接返回空
        return render_template('index.html', hot_animes=[])

    # 单次联表查询：按评分倒序，限制数量
    query = QueryService.base_query()
    query = QueryService.apply_filters(query, on_date=latest_date, min_vote=min_vote)
    query = QueryService.order_by_score_desc(query)

    rows = query.limit(max_number).all()
    hot_animes = QueryService.to_brief_list(rows)

    return render_template('index.html', hot_animes=hot_animes)


@app.route('/library')
def library_default():
    time_object: datetime = datetime.now()
    year: int = time_object.year

    season: str = 'all'
    if 1 < time_object.month < 4:
        season = 'winter'
    elif 4 <= time_object.month < 7:
        season = 'spring'
    elif 7 <= time_object.month < 10:
        season = 'summer'
    elif 10 <= time_object.month < 12:
        season = 'autumn'

    return library(str(year), season)


@app.route('/library/<year>/<season>/<int:vote>')
@limiter.limit('30/minute; 2000/day')
@cache.cached(timeout=60, query_string=True)
def library(year: str = None, season: str = None, vote: int = 0):
    # 归一化参数
    if year and year.lower() == 'all':
        year = None
    if season and season.lower() == 'all':
        season = None

    if season not in ('spring', 'summer', 'autumn', 'winter', None):
        abort(400, description='Invalid season parameter')

    # year 类型转为 int 或 None（YEAR 字段对比时更稳定）
    norm_year = None
    if year:
        try:
            norm_year = int(year)
        except ValueError:
            # 非法 year，返回 400 或忽略
            abort(400, description='Invalid year parameter')

    page: int = request.args.get('page', 1, type=int)
    per_page = 20

    # 构建查询
    query = QueryService.base_query()
    query = QueryService.apply_filters(query, year=norm_year, season=season, min_vote=vote)
    query = QueryService.order_by_score_desc(query)

    rows, total_count, total_pages = PaginationService.paginate(query, page, per_page)
    anime = QueryService.to_brief_list(rows)

    # 分页链接构造器
    def build_url(p: int):
        y = year if year else 'all'
        s = season if season else 'all'
        return f'/library/{y}/{s}/{vote}?page={p}'

    pagination = PaginationService.build_pagination_links(total_pages, page, build_url)

    return render_template(
        'library.html',
        library_args=LibraryArgs(norm_year, season, vote),
        animes=anime,
        pagination=pagination
    )


@app.route('/search')
@limiter.limit('3/second; 20/minute; 2000/day')
def search():
    keyword: str = request.args.get('keyword', '').strip()
    page: int = request.args.get('page', 1, type=int)
    per_page = 20

    if not 2  <= len(keyword) <= 64:
        abort(400, description='Invalid keyword parameter')

    query = QueryService.base_query()
    query = QueryService.apply_filters(query, keyword=keyword)

    rows, total_count, total_pages = PaginationService.paginate(query, page, per_page)
    anime = QueryService.to_brief_list(rows)

    def build_url(p: int):
        return url_for('search', keyword=keyword, page=p)

    pagination = PaginationService.build_pagination_links(total_pages, page, build_url)

    return render_template(
        'search.html',
        query=keyword,
        animes=anime,
        pagination=pagination
    )

@app.route('/picture/<int:pid>')
def picture(pid: int):
    if not ENABLE_INNER_PICTURE:
        abort(404)

    return send_from_directory(PICTURE_PATH, str(pid) + '.jpg')


@app.route('/robots.txt')
def robot():
    return send_file('static/robots.txt')


if __name__ == '__main__':
    pass