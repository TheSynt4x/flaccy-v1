import asyncio

from app import app
from configurator import create_tables

create_tables()

if __name__ == "__main__":
    asyncio.run(app.main())
