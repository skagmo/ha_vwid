import libvwid
import aiohttp
import asyncio
import logging
import time

async def main():
    logging.basicConfig(level=logging.INFO)

    async with aiohttp.ClientSession() as session:
        w = libvwid.vwid(session)
        w.set_vin("...")
        w.set_credentials("mail@example.com", "secret")

        while(1):
            data = await w.get_status()
            if (data):
                print (data['data'])
            time.sleep(600)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

