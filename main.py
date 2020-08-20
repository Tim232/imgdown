from urllib.parse import urlparse
import aiofiles
import aiohttp
import asyncio
import praw
import os


reddit = praw.Reddit(
    client_id="giTo1WhRJaqN1Q",
    client_secret="RdzlJ3yyZBdheqcIAq0tM59HSlw",
    user_agent="AgentHa",
)

def links(limit=10):
    print(limit)
    hentai = reddit.subreddit("futanari").hot(limit=limit)
    submissions = [x for x in hentai]

    list = []

    for submission in submissions:
        if submission.url.startswith("http"):  # and "i.redd.it" in submission.url:
            list.append(submission.url)
            # print(list)
        else:
            print(submission.url)
    print(list)
    return list


async def down(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    split_path = path.split("/")

    if len(split_path) <= 2:
        # async with sem:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:

                f = await aiofiles.open("downloads/" + split_path[1], mode="wb")
                await f.write(await response.read())
                return await f.close()
    else:
        return print(path)

if __name__ == "__main__":
    if not os.path.isdir("~/downloads"): os.mkdir('downloads')
    limit = int(input("개수 (Default as 10) : "))
    list = links(limit)

    error = []
    for url in list:
        try:
            asyncio.run(down(url))
        except:
            error.append(url)
    print(error)
