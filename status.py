#!/usr/bin/env python3
"""
Status and Health Check Server
Equivalent to: status.php

Provides:
- Health check endpoint
- Bot status information
- Basic HTML interface
"""

import asyncio
import os
from aiohttp import web
from datetime import datetime
import json
from pathlib import Path

from config import (
    API_TOKEN, CHANNEL_USERNAME, GROUP_ID, ADMIN_ID,
    get_leads_count, get_leads, logger
)

# Paths
PROJECT_DIR = Path(__file__).parent
LEADS_FILE = PROJECT_DIR / "leads.json"

class StatusServer:
    """Health check and status server"""
    
    def __init__(self, port: int = 8000):
        self.port = port
        self.app = web.Application()
        self.setup_routes()
    
    def setup_routes(self):
        """Setup HTTP routes"""
        self.app.router.add_get("/", self.handle_status)
        self.app.router.add_get("/health", self.handle_health)
        self.app.router.add_get("/api/stats", self.handle_stats_json)
        self.app.router.add_get("/api/leads", self.handle_leads_json)
    
    async def handle_status(self, request):
        """
        Main status page (equivalent to status.php)
        Returns HTML with bot status
        """
        leads_count = get_leads_count()
        status_emoji = "✅" if leads_count >= 0 else "❌"
        
        html = f"""<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DTM Bot - Status</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        
        .container {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
            width: 100%;
            padding: 40px;
        }}
        
        h1 {{
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
        }}
        
        .subtitle {{
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }}
        
        .info-box {{
            background: #f5f5f5;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
        }}
        
        .info-box strong {{
            color: #333;
        }}
        
        .info-box p {{
            margin: 5px 0;
            color: #666;
            font-size: 14px;
        }}
        
        .status {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 10px 0;
        }}
        
        .status-icon {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 12px;
        }}
        
        .status-icon.ok {{
            background: #4CAF50;
        }}
        
        .status-icon.error {{
            background: #f44336;
        }}
        
        .stat-item {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }}
        
        .stat-item:last-child {{
            border-bottom: none;
        }}
        
        .stat-label {{
            color: #666;
            font-weight: 500;
        }}
        
        .stat-value {{
            color: #333;
            font-weight: bold;
        }}
        
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            text-align: center;
            color: #999;
            font-size: 12px;
        }}
        
        .badge {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 12px;
            margin-left: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 DTM Bot - Python Version</h1>
        <p class="subtitle">Bot status monitoring dashboard</p>
        
        <div class="info-box">
            <div class="status">
                <span class="status-icon ok">✓</span>
                <span><strong>Bot Status:</strong> Running</span>
            </div>
            <div class="status">
                <span class="status-icon ok">✓</span>
                <span><strong>Database:</strong> Operational</span>
            </div>
        </div>
        
        <div class="info-box">
            <strong>📊 Statistics</strong>
            <div class="stat-item">
                <span class="stat-label">Total Leads</span>
                <span class="stat-value">{leads_count}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Admin ID</span>
                <span class="stat-value">{ADMIN_ID}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Channel</span>
                <span class="stat-value">{CHANNEL_USERNAME}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Last Updated</span>
                <span class="stat-value">{datetime.now().strftime('%H:%M:%S')}</span>
            </div>
        </div>
        
        <div class="info-box">
            <strong>🔗 API Endpoints</strong>
            <p>
                <code>/health</code> - Health check<br>
                <code>/api/stats</code> - Statistics (JSON)<br>
                <code>/api/leads</code> - Leads list (JSON)<br>
            </p>
        </div>
        
        <div class="info-box">
            <strong>⚙️ Configuration</strong>
            <p>
                <strong>Version:</strong> Python (aiogram)<span class="badge">v3</span><br>
                <strong>Storage:</strong> JSON Files<br>
                <strong>Mode:</strong> Polling/Webhook<br>
            </p>
        </div>
        
        <div class="footer">
            <p>🚀 DTM Bot - Telegram Lead Collection Bot</p>
            <p>Converted from PHP to Python • {datetime.now().year}</p>
        </div>
    </div>
</body>
</html>"""
        
        return web.Response(text=html, content_type='text/html')
    
    async def handle_health(self, request):
        """Health check endpoint"""
        return web.json_response({
            'status': 'ok',
            'timestamp': datetime.now().isoformat(),
            'bot': 'operational'
        })
    
    async def handle_stats_json(self, request):
        """Return statistics as JSON"""
        return web.json_response({
            'total_leads': get_leads_count(),
            'admin_id': ADMIN_ID,
            'channel': CHANNEL_USERNAME,
            'group_id': GROUP_ID,
            'timestamp': datetime.now().isoformat()
        })
    
    async def handle_leads_json(self, request):
        """Return leads as JSON (protected - add auth in production)"""
        leads = get_leads()
        return web.json_response({
            'count': len(leads),
            'leads': leads[-10:],  # Return last 10
            'timestamp': datetime.now().isoformat()
        })
    
    async def start(self):
        """Start the server"""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", self.port)
        await site.start()
        logger.info(f"✅ Status server started on http://localhost:{self.port}")
        print(f"🌐 Status dashboard: http://localhost:{self.port}")
        return runner


async def main():
    """Main entry point"""
    port = int(os.environ.get("STATUS_PORT", 8000))
    server = StatusServer(port=port)
    runner = await server.start()
    
    try:
        # Keep the server running
        while True:
            await asyncio.sleep(3600)
    except KeyboardInterrupt:
        await runner.cleanup()
        logger.info("Status server stopped")


if __name__ == "__main__":
    asyncio.run(main())
