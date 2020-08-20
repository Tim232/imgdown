from urllib.parse import urlparse
import aiofiles
import aiohttp
import asyncio


async def downloader(urls):
    for url in urls:
        parsed_url = urlparse(url)
        path = parsed_url.path
        split_path = path.split("/")

        if len(split_path) <= 2:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:

                    f = await aiofiles.open(split_path[1], mode="wb")
                    await f.write(await response.read())
                    return await f.close()


asyncio.run(downloader([]))
