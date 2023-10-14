import aiohttp
import asyncio
import aiocache
import sys
import os
import json
from pprint import pprint

HEADERS = {}
GROUP = None
GROUP_SLUG = None
GROUP_DIR = None
CLASS_NUMBER = None


def parse_curl() -> None:
    """
    Parse a simple curl command into a dictionary of headers and the url
    :return: None
    """
    try:
        curl_file = open("curl.txt", 'r')
        curl_data = curl_file.read()
        curl_data = curl_data.replace("--compressed", '')
        split_headers = curl_data.split(" -H")
        for i in range(1, len(split_headers)):
            header, _, content = split_headers[i].replace(' ', '', 2).lstrip('\'').rstrip("\n \\\'").partition(":")
            HEADERS[header] = content
        global GROUP
        group_index = curl_data.find("/group/") + len("/group/")
        GROUP = curl_data[group_index: curl_data.index("/", group_index + 1)]
        curl_file.close()

    except Exception as e:
        print(e)
        exit()


async def prepare_fs() -> bool:
    global GROUP_DIR
    global CLASS_NUMBER
    GROUP_DIR = f"{os.getcwd()}/campuswire_data/{CLASS_NUMBER} ({GROUP_SLUG})"
    try:
        if not os.path.exists(GROUP_DIR):
            os.mkdir(GROUP_DIR)
            print(f"Directory 'campuswire_data/{GROUP_SLUG}' created")
        else:
            print(f"Directory 'campuswire_data/{GROUP_SLUG}' exists")
            if input("Do you want to overwrite it? (y/n): ").lower() == 'n':
                print("Abort operation...")
                return False
        return True

    except Exception as e:
        print("here")
        print(e)
        return False


def write_to_file(file_name: str, data: str | dict | tuple):
    """
    Write data to a file
    :param file_name: file name
    :param data: data to write
    :return: None
    """
    global GROUP_DIR
    try:
        with open(f"{GROUP_DIR}/{file_name}", 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(e)


async def get_group(session: aiohttp.ClientSession):
    """
    Get group information and sets GROUP_SLUG
    :param session:
    :return:
    """
    global GROUP_SLUG
    global CLASS_NUMBER
    try:
        resp = await session.get(url=f"https://api.campuswire.com/v1/group/{GROUP}")
        res = json.loads(await resp.text())
        GROUP_SLUG = res['slug']
        CLASS_NUMBER = res['classNumber'].strip('\\ \n').replace('/', '-')
        return resp.json()
    except Exception as e:
        print(e)
        return None



async def get_posts(session: aiohttp.ClientSession):
    """
    Get posts for a group
    :param session: Session
    :return: JSON
    """
    try:
        resp = await session.get(url=f"https://api.campuswire.com/v1/group/{GROUP}/posts")
        return resp.json()

    except Exception as e:
        print(e)


async def get_comments(session: aiohttp.ClientSession, post_id: str):
    """
    Get comments for a post
    :param session: Session
    :param post_id: post id
    :return: JSON
    """
    try:
        async with session.get(url=f"https://api.campuswire.com/v1/group/{GROUP}/posts/{post_id}/comments") as resp:
            res = json.loads(await resp.text())
            return {
                post_id: res
            }

    except aiohttp.ServerDisconnectedError:
        print("Server terminated the connection")

    except Exception as e:
        print(e)
        return None


async def main():
    parse_curl()
    session = aiohttp.ClientSession(headers=HEADERS)
    group = await get_group(session)

    if not await prepare_fs():
        await session.close()
        await exit()

    print("Fetching data...")

    posts = await get_posts(session)

    tasks = []
    for post in await posts:
        tasks.append(asyncio.ensure_future(get_comments(session, post['id'])))
    all_comments = await asyncio.gather(*tasks)

    comments = {}
    for comment in all_comments:
        comments.update(comment)

    _posts = await get_posts(session)
    write_to_file("group.json", await group)
    write_to_file("posts.json", await _posts)
    write_to_file("comments.json", comments)

    await session.close()


if __name__ == '__main__':
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    elif sys.platform == 'linux':
        asyncio.run(main())
