import requests
import re
import asyncio
import aiohttp
import datetime

class Plates():
    __slots__ = ("valid_plates","unavailable")
    def __init__(self,valid_plates=[],unavailable=[]):
        self.valid_plates = valid_plates
        self.unavailable = unavailable


plates = Plates()

async def check_plate(plate):
    start_time = datetime.datetime.now()
    url = "https://dmvcivls-wselfservice.ct.gov/Registration/VerifyRegistration"
    payload=f'__RequestVerificationToken=8F43Emt0porF1DTEAEfztYGVBzYYRNLst2JmArB9L_9VcXH-2bIvBUR-IFXpqSWNpfhJ__Hs1ziI_5716Rdfg-96k947LYhYQYgq0CZl3k6owiNQEXxBw2bXY8NPrDuomi7DzEB6tnXICWaf_8y3m60_AVch00qzMmFq0KWCxoY1&PlateNumber={plate}&PlateClassID=25&submitButton=Continue'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'ctsessionlanguage=en_US; googtrans=/auto/en; __RequestVerificationToken=GTWaGqmfWXdvnM3o_dC5QAdbI39wdUor4aMp1tPQ3ZQ7D20lGrM0wxfmlLoEsbQO6NqInQr50zrPu5HdX_bHGLORomjRAUWbaVXGs6L0p5KCfKH9XXk1Lge84F7MiqBatB_FGClbMduCnsfHE-XZaQ2; DMVCT=!eZL1xEPdrSmNvAj0/iQQWXMMxA4+KvHxMJ0QS1f21pTe02hYbtBvv7aVrAtnsp0EgwWxg4CGA6eEbXY=; akavpau_wr=1670977885~id=b1197c5405ad49ead6cf008adb2456ec; ASP.NET_SessionId=yntlcm2fomjz1fasnt1ibhcs; akavpau_wr=1670977911~id=3da8303269cb4c2cde3efe63a8d312dc'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=payload) as response:
            valid = len(re.findall("Registration not found. Please check the information you entered and try again.",await response.text()))
            if valid == 0:
                plates.valid_plates.append(plate)
            else:
                plates.unavailable.append(plate)

    task = asyncio.current_task()
    elapsed_time = datetime.datetime.now() - start_time
    print(f"Task {task.get_name()} completed in {elapsed_time.total_seconds()} seconds.")

async def check_plates():
    names = []
    with open ("input/names.txt") as file:
        for name in file:
            names.append(name)
    tasks = [asyncio.create_task(check_plate(name)) for name in names]
    await asyncio.gather(*tasks)


def main():
    asyncio.run(check_plates())
    with open ("output/valid.txt","w") as file:
        for valid_plate in plates.valid_plates:
            file.writelines(valid_plate)
    with open ("output/invalid.txt","w") as file:
        for unavailable in plates.unavailable:
            file.writelines(unavailable)


if __name__ == "__main__":
    main()

