#
# Written by ChatGPT
#
import asyncio
import json
import aiohttp

# Function to check a single subreddit and return its status
async def check_subreddit(session, subreddit):
    async with session.get(f"https://old.reddit.com/{subreddit}.json") as response:
        print(subreddit, response.status)
        if response.status == 200:
            return (subreddit, False)
        elif response.status == 403:
            return (subreddit, True)
        else:
            print(subreddit, response.status, response.json())
            return (subreddit, False)

# Load the list of subreddits from a JSON file
with open("subreddits.json", "r") as f:
    subreddits = json.load(f)

# Use asyncio to check the subreddits in parallel
async def main():
    async with aiohttp.ClientSession(headers={"User-agent": "Mozilla/5.0"}) as session:
        tasks = []
        for subreddit, private in subreddits.items():
            if private:
                continue
            task = asyncio.create_task(check_subreddit(session, subreddit))
            tasks.append(task)
            if len(tasks) == 100:
                results = await asyncio.gather(*tasks)
                for result in results:
                    subreddit, status = result
                    subreddits[subreddit] = status
                with open("subreddits.json", "w") as f:
                    json.dump(subreddits, f, indent=2)
                tasks = []
        if tasks:
            results = await asyncio.gather(*tasks)
            for result in results:
                subreddit, status = result
                subreddits[subreddit] = status
            with open("subreddits.json", "w") as f:
                json.dump(subreddits, f, indent=2)

# Run the main coroutine
asyncio.run(main())
