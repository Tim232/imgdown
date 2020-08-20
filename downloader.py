redditclientid = input("Reddit Client Id : ")
redditclientsecret = input("Reddit Client Secret : ")
subreddit = input("Exisiting SubReddit : ")

print("Checking Modules...")

print("Importing Internal Modules...")
import asyncio
import os
from urllib.parse import urlparse
print("Imported Internal Modules!")

print("Importing External Modules...")

try: import aiofiles
except ModuleNotFoundError: 
    print("aiofiles not found. Installing...")
    os.system('python -m pip install -U aiofiles==0.5.0')
    import aiofiles

try: import aiohttp
except ModuleNotFoundError: 
    print("aiohttp not found. Installing...")
    os.system('python -m pip install -U aiohttp==3.6.2')
    import aiohttp

try: import praw
except ModuleNotFoundError: 
    print("praw not found. Installing...")
    os.system('python -m pip install -U praw==7.1.0')
    import praw
    
print("Imported External Modules!")

reddit = praw.Reddit(
    client_id=redditclientid, client_secret=redditclientsecret, user_agent="Random",
)


def links(limit=100):
    print(limit)
    hot = reddit.subreddit(subreddit).hot(limit=limit)
    submissions = [x for x in hot]

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
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:

                f = await aiofiles.open("downloads/" + split_path[1], mode="wb")
                await f.write(await response.read())
                return await f.close()
    else:
        return print(path)


print("Checking whether 'downloads' folder exists...")
if not os.path.isdir("~/downloads"):
    print("Creating 'downloads' folder...")
    os.mkdir("downloads")
    print("Created!")
print("Checked!")

limit = int(input("How much images? (Default as 100) : "))
list = links(limit)

print("May take a while...")

error = []
for url in list:
    try:
        asyncio.run(down(url))
    except:
        error.append(url)
print(error)

input("Press any key to close this console.")