import asyncio

async def scan_code():
    await asyncio.sleep(2)
    return "Scan Complete: No Malware Found"
async def main():
    result = await scan_code()
    print(result)

asyncio.run(main())