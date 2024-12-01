from aiohttp import web
import logging

logger = logging.getLogger('discord_bot')

async def health_check(request):
    """Health check endpoint for Render"""
    return web.Response(text="Bot is running!", status=200)

async def setup_webserver(port):
    """Setup a basic web server for Render deployment"""
    app = web.Application()
    app.router.add_get('/', health_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    
    try:
        await site.start()
        logger.info(f"Web server started on port {port}")
    except Exception as e:
        logger.error(f"Failed to start web server: {e}")
        raise

    return runner
