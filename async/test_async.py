import time
import asyncio
import random

async def example_coroutine(i):
    time_io_wait = random.randint(1,3)
    await asyncio.sleep(time_io_wait)   # This simulates waiting some function 
                                        # to recieve info from the internet for example
    print("example {} execyted after {} seconds".format(i,time_io_wait))

async def main():
    tasks = []
    for i in range(20):
        tasks.append(asyncio.ensure_future(example_coroutine(i)))

    await asyncio.gather(*tasks)

t0=time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
print("\nTotal time needed was {}\n".format(time.time() -t0 ) )