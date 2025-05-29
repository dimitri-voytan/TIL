import asyncio
import aiohttp
import time
import json
from concurrent.futures import ThreadPoolExecutor

async def make_request(session, url, payload):
    try:
        start_time = time.time()
        async with session.post(url, json=payload) as response:
            await response.json()
            return time.time() - start_time, response.status
    except Exception as e:
        return None, str(e)

async def stress_test(url, payload, concurrent_requests=50, total_requests=100):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(total_requests):
            task = make_request(session, url, payload)
            tasks.append(task)
            
            if len(tasks) >= concurrent_requests:
                results = await asyncio.gather(*tasks)
                tasks = []
                # Process results
                for duration, status in results:
                    if duration:
                        print(f"Request completed in {duration:.2f}s, Status: {status}")

# Usage
payload = {
    "model": "HuggingFaceTB/SmolLM-1.7B",
    "prompt": "Once upon a time,",
    "max_tokens": 512,
    "temperature": 0.5
}

asyncio.run(stress_test("http://localhost:8000/v1/completions", payload))