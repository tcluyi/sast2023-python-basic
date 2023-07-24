import argparse
import json
import re

def parser_data():
    """
    从命令行读取用户参数
    做出如下约定：
    1. -f 为必选参数，表示输入题库文件
    ...

    :return: 参数
    """
    parser = argparse.ArgumentParser(
        prog="Word filling game",
        description="A simple game",
        allow_abbrev=True
    )

    parser.add_argument("-f", "--file", help="题库文件", required=True)
    parser.add_argument("-a", "--article", help="指定文章名", required=False)
    
    args = parser.parse_args()
    return args


def read_articles(filename):
    """
    读取题库文件

    :param filename: 题库文件名

    :return: 一个字典，题库内容
    """
    with open(filename, 'r', encoding="utf-8") as f:
        data = json.load(f)

    return data


def get_article(articlename, articles):
    for article in articles:
        if article['title'] == articlename:
            return article
    return None


def get_inputs(hints):
    """
    获取用户输入

    :param hints: 提示信息

    :return: 用户输入的单词
    """

    keys = []
    for hint in hints:
        print(f"请输入{hint}：")
        key = input()
        keys.append(key)

    return keys


def replace(article, keys):
    """
    替换文章内容

    :param article: 文章内容
    :param keys: 用户输入的单词

    :return: 替换后的文章内容

    """
    article = re.sub(r"\{\{(\d+)\}\}", lambda match: keys[int(match.group(1))-1], article)
    return article


if __name__ == "__main__":
    args = parser_data()
    data = read_articles(args.file)
    articles = data["articles"]
    article = get_article(args.article, articles)
    if article is None:
        print(f"Article {args.article} not found")
        exit()

    keys = get_inputs(article['hints'])
    new_article = replace(article['article'], keys)
    print(f"{new_article}")
    # TODO: 根据参数或随机从 articles 中选择一篇文章
    # TODO: 给出合适的输出，提示用户输入
    # TODO: 获取用户输入并进行替换
    # TODO: 给出结果



