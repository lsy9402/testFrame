from aiohttp import ClientSession


async def send_post(url, json, **kwargs):
    async with ClientSession() as session:
        async with session.post(url, json=json, **kwargs) as res:
            return res.status, await res.json()
