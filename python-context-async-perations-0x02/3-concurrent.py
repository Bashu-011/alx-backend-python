import asyncio
import aiosqlite

# async function to fetch users
async def async_fetch_users():
    async with aiosqlite.connect('users.db') as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM users")
            users = await cursor.fetchall()  
            return users

# fetching users aolder than 40
async def async_fetch_older_users():
    async with aiosqlite.connect('users.db') as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM users WHERE age > 40")
            older_users = await cursor.fetchall()  
            return older_users

# main async funcion to run both functions
async def fetch_concurrently():
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    
    print("All Users:")
    print(users) 
    
    print("\nUsers older than 40:")
    #print to the terminals
    print(older_users)  

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
