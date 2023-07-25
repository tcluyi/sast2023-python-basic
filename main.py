import argparse
import json
import re
import random
import os

history = {}
history['articles'] = []

def load():
    if os.path.getsize("history.json") == 0:
        return

    global history
    history = read_articles("history.json")
    

def parser_data():
    """
    从命令行读取用户参数
    做出如下约定：
    1. -f/--file 为必选参数，表示输入题库文件
    2. -a/--article 为可选参数，表示指定的文章名
    3. -c/--clear 为可选参数， 表示是否清空保存的历史记录
    :return: 参数
    """
    parser = argparse.ArgumentParser(
        prog="Word filling game",
        description="A simple game",
        allow_abbrev=True
    )

    parser.add_argument("-f", "--file", help="题库文件", required=True)
    parser.add_argument("-a", "--article", help="指定文章名", required=False)
    parser.add_argument("-c", "--clear", help="清空历史记录", required=False)
    try:
        args = parser.parse_args()
    except SystemExit:
        print("参数错误,请重新输入命令行参数")
        exit()

    return args


def read_articles(filename):
    """
    读取题库文件

    :param filename: 题库文件名

    :return: 一个字典，题库内容
    """
    try:
        with open(filename, 'r', encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("文件未找到,请检查文件路径")
        exit()
    except IOError:
        print("文件读取错误")
        exit()
    except UnicodeDecodeError:
        print("文件编码错误")
        exit()
    except json.JSONDecodeError:
        print("JSON解码错误")
        exit()
    except Exception as e:
        print("未知错误：", str(e))
        exit()

    return data


def get_article(articlename, articles):
    if articlename is None:
        return articles[random.randint(0, len(articles) - 1)]

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


def save(article):
    '''
    将得到的文章保存在history.json中
    :param article: 得到的文章内容
    '''
    global history
    history['articles'].append(article)
    json.dump(history, open("history.json", 'w'), ensure_ascii=False, indent=4)

if __name__ == "__main__":
    args = parser_data()
    if args.clear is None or args.clear == "off":
        load()
    elif args.clear != "on":
        print("参数错误，请重新输入命令行参数")
        exit()

    data = read_articles(args.file)
    articles = data["articles"]
    article = get_article(args.article, articles)
    if article is None:
        print(f"Article {args.article} not found")
        exit()

    keys = get_inputs(article['hints'])
    new_article = {}
    new_article['title'] = article['title']
    new_article['article'] = replace(article['article'], keys)
    save(new_article)
    print(f"title: {new_article['title']}")
    print(f"article: {new_article['article']}")
    # TODO: 根据参数或随机从 articles 中选择一篇文章
    # TODO: 给出合适的输出，提示用户输入
    # TODO: 获取用户输入并进行替换
    # TODO: 给出结果