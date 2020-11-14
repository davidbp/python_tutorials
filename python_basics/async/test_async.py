import time
import asyncio
import random

async def example_coroutine(i):
    time_io_wait = 3
    await asyncio.sleep(time_io_wait)   
    
async def main():
    tasks = []
    t0 = time.time()
    for i in range(5):
        print(f'time passed after iter {i} is {time.time()-t0}')
        tasks.append(asyncio.ensure_future(example_coroutine(i)))

    await asyncio.gather(*tasks)

t0=time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
print("\nTotal time needed was {}\n".format(time.time() -t0 ) )