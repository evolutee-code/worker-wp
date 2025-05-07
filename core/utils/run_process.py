import asyncio


async def run_command(command):
    process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, _ = await process.communicate()
    return stdout.decode().strip()
