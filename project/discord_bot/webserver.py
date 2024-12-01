from aiohttp import web
import logging
import os

logger = logging.getLogger('discord_bot')

async def health_check(request):
    """Health check endpoint for Render"""
    return web.Response(text="Bot is running!", status=200)

async def setup_webserver(port):
    """Setup a basic web server for Render deployment"""
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Ensure we're binding to 0.0.0.0 and using the PORT from environment
    site = web.TCPSite(
        runner, 
        host='0.0.0.0',
        port=int(os.getenv('PORT', port))
    )
    
    try:
        await site.start()
        logger.info(f"Web server started on port {port}")
    except Exception as e:
        logger.error(f"Failed to start web server: {e}")
        raise

    return runner
