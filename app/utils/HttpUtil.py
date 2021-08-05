from aiohttp import ClientSession


async def send_post(url, data, **kwargs):
    async with ClientSession() as session:
        async with session.post(url, data=data, **kwargs) as res:
            return res.status, await res.json()
