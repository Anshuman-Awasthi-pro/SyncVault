import asyncio
import httpx
import time

TARGET_URL = "http://127.0.0.1:8000/api/push"
TOTAL_REQUESTS = 10000
CONCURRENCY_LIMIT = 250  # Only allow 50 concurrent requests at a time

# Create a bouncer that limits simultaneous execution
semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)

async def send_mock_commit(client: httpx.AsyncClient, task_id: int):
    is_even = task_id % 2 == 0
    filename = f"db_config_{task_id}.py" if is_even else f"utility_{task_id}.py"
    code_content = "DB_PASS='leak_123'\ndef init(): pass" if is_even else "def calculated_sum(a, b):\n    return a + b"
    username = "Animesh" if is_even else "Anshika"

    payload = [
        {
            "user": username,
            "filename": filename,
            "code": code_content
        }
    ]

    # Acquire a spot from the bouncer before firing
    async with semaphore:
        try:
            # Reduced timeout to 5.0 seconds since it should respond instantly
            response = await client.post(TARGET_URL, json=payload, timeout=5.0)
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception:
            return False

async def main():
    print(f"🚀 Initializing Load Cannon: Blasting {TOTAL_REQUESTS} files (Max {CONCURRENCY_LIMIT} parallel)...")
    
    # Configure high-performance pool boundaries
    limits = httpx.Limits(max_keepalive_connections=50, max_connections=100)
    
    start_time = time.time()
    
    async with httpx.AsyncClient(limits=limits) as client:
        tasks = [send_mock_commit(client, i) for i in range(TOTAL_REQUESTS)]
        results = await asyncio.gather(*tasks)
        
    end_time = time.time()
    
    successful_pushed = sum(1 for r in results if r)
    duration = end_time - start_time
    qps = successful_pushed / duration if duration > 0 else 0
    
    print("\n" + "="*40)
    print("🎯 LOAD TEST EXECUTION COMPLETE")
    print("="*40)
    print(f"Total Files Batched:   {TOTAL_REQUESTS}")
    print(f"Successfully Queued:   {successful_pushed}/{TOTAL_REQUESTS}")
    print(f"Total Execution Time:  {duration:.2f} seconds")
    print(f"Ingestion Throughput:  {qps:.2f} Requests/Second")
    print("="*40)

if __name__ == "__main__":
    asyncio.run(main())