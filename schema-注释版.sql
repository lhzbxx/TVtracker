drop table if exists user;
# 用户信息表
create table user (
    id integer primary key autoincrement,
    # 编号
    username text not null,
    # 用户名
    password text not null,
    # 密码
    noticenum integer not null default 0,
    # 个人通知的数量
    notification text
    # 公共通知
);

drop table if exists tv;
# 剧集表
create table tv (
    id integer primary key autoincrement,
    # 编号
    tvname text not null,
    # 剧集名称
    episode integer not null,
    # 集数
    epname text,
    # 单集名称
    address text not null,
    # 观看地址
    type text not null
    # 源地址类型
);

drop table if exists ping;
# 更新动态表
create table ping (
    id integer primary key autoincrement,
    # 编号
    name text not null,
    # 剧集名称
    time text not null,
    # 更新时间
    episode text not null,
    # 具体集数和名称
    address text not null
    # 观看地址
);

drop table if exists discuss;
# 吐槽表
create table discuss (
    id integer primary key autoincrement,
    # 编号
    name1 text not null,
    # 发布人
    name2 text,
    # 回复人
    time integer not null,
    # 发布时间
    warning integer not null,
    # 剧透提醒
    level integer not null default 0,
    # 主评论或者子评论
    content text not null
    # 发布内容
);

drop table if exists dream;
# 心愿单
create table dream (
    id integer primary key autoincrement,
    # 编号
    name text not null,
    # 剧集名称
    link_youku text,
    # 剧集的地址
    link_iqiyi text,
    # 剧集的地址
    link_vqq text
    # 剧集的地址
);

drop table if exists tracking;
# 记录表
create table tracking (
    id integer primary key autoincrement,
    # 编号
    tvname text not null,
    # 剧集id
    userid integer not null,
    # 用户id
    epnum integer not null default 0,
    # 观看集数
    end integer not null default 0
    # 是否已经完结
);

drop table if exists notification;
# 通知表
create table notification (
    id integer primary key autoincrement,
    # 编号
    username text not null,
    # 用户名
    userid integer not null,
    # 用户id
    content integer not null default 0,
    # 通知内容
    link integer not null default 0
    # 从通知转向的链接
);