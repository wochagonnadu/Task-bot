import asyncio
import asyncpg
from src.config import get_config

async def create_schema():
    config = get_config()
    # Convert SQLAlchemy URL to asyncpg format
    db_url = config.database_url.replace('postgresql+asyncpg://', 'postgresql://')
    
    try:
        conn = await asyncpg.connect(db_url)
        # Create schema if it doesn't exist
        await conn.execute('CREATE SCHEMA IF NOT EXISTS public;')
        print("Schema created successfully")
        await conn.close()
    except Exception as e:
        print(f"Error creating schema: {e}")

if __name__ == "__main__":
    asyncio.run(create_schema())
