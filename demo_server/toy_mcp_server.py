# toy_mcp_server.py - Echo Privacy Bot tools (single file version)
import asyncio
import random
import datetime
from fastmcp import FastMCP
import structlog

logger = structlog.get_logger(__name__)

# Server settings
TOY_SERVER_NAME = 'Echo Privacy Tools'
TOY_SERVER_VERSION = '1.0.0'
TOY_SERVER_DESCRIPTION = 'Privacy-first utility tools for Echo Privacy Bot'
TOY_SERVER_PORT = 8901

mcp = FastMCP(
    name=TOY_SERVER_NAME,
    version=TOY_SERVER_VERSION,
    instructions=TOY_SERVER_DESCRIPTION,
)

# === YOUR 3 CUSTOM TOOLS ===
@mcp.tool()
async def calculator(operation: str, a: float, b: float) -> str:
    """Simple calculator: add, subtract, multiply, divide"""
    if operation == "add":
        return str(a + b)
    elif operation == "subtract":
        return str(a - b)
    elif operation == "multiply":
        return str(a * b)
    elif operation == "divide":
        return str(a / b) if b != 0 else "Cannot divide by zero"
    return "Unknown operation. Use: add, subtract, multiply, or divide"

@mcp.tool()
async def get_current_time() -> str:
    """Returns current time in UTC"""
    now = datetime.datetime.now(datetime.UTC)
    return now.strftime("%Y-%m-%d %H:%M:%S UTC")

@mcp.tool()
async def privacy_check() -> str:
    """Privacy reminder that matches Gianni’s brand"""
    return "✅ Echo Privacy Bot respects your privacy 100%. No data is sent to third-party servers except your own Supabase instance that you fully control."

# === ORIGINAL DEMO TOOLS (kept for safety) ===
@mcp.tool()
async def add(a: int, b: int) -> int:
    '''Adds two integers together.'''
    return a + b

@mcp.tool()
async def magic_8_ball(question: str = 'Your question') -> str:
    '''Consult the Magic 8-Ball.'''
    answers = ['It is certain.', 'Yes – definitely.', 'Outlook good.', 'Very doubtful.']
    return random.choice(answers)

async def main():
    logger.info(f'Starting {TOY_SERVER_NAME} on port {TOY_SERVER_PORT}...')
    await mcp.run_async(
        transport='streamable-http',
        host='127.0.0.1',
        port=TOY_SERVER_PORT
    )

if __name__ == '__main__':
    asyncio.run(main())