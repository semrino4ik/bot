import asyncio
from bot_admin import main as admin_main
from bot_student import main as student_main

async def main():
    await asyncio.gather(
        admin_main(),
        student_main()
    )

if name == "__main__":
    asyncio.run(main())
