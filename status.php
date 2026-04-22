<!-- 🔥 TEST PAGE FOR PHP BOT -->
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DTM Bot - PHP Version</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 10px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
            width: 100%;
            padding: 40px;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }
        
        .info-box {
            background: #f5f5f5;
            border-left: 4px solid #667eea;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
        }
        
        .info-box strong {
            color: #333;
        }
        
        .info-box p {
            margin: 5px 0;
            color: #666;
            font-size: 14px;
        }
        
        .status {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 10px 0;
        }
        
        .status-icon {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }
        
        .status-icon.ok {
            background: #4CAF50;
        }
        
        .status-icon.error {
            background: #f44336;
        }
        
        .command-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            margin: 5px;
            transition: background 0.3s;
        }
        
        .command-btn:hover {
            background: #764ba2;
        }
        
        .buttons {
            margin-top: 30px;
            text-align: center;
        }
        
        .footer {
            text-align: center;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #999;
            font-size: 12px;
        }
        
        .code {
            background: #f5f5f5;
            padding: 10px;
            border-radius: 5px;
            font-family: monospace;
            color: #d63384;
            margin: 5px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 DTM Bot - PHP Version</h1>
        <p class="subtitle">Telegram User Registration Bot</p>
        
        <?php
        require_once __DIR__ . '/config.php';
        
        // Check system status
        $php_version = phpversion();
        $curl_enabled = extension_loaded('curl');
        $config_exists = file_exists(__DIR__ . '/.env');
        $api_token = !empty(API_TOKEN);
        
        echo '<div class="info-box">';
        echo '<strong>🔧 System Status:</strong>';
        echo '<div class="status">';
        echo '<span class="status-icon ok">✓</span>';
        echo '<span>PHP Version: <strong>' . $php_version . '</strong></span>';
        echo '</div>';
        
        echo '<div class="status">';
        echo '<span class="status-icon ' . ($curl_enabled ? 'ok' : 'error') . '">' . ($curl_enabled ? '✓' : '✗') . '</span>';
        echo '<span>cURL: <strong>' . ($curl_enabled ? 'Enabled' : 'Disabled') . '</strong></span>';
        echo '</div>';
        
        echo '<div class="status">';
        echo '<span class="status-icon ' . ($config_exists ? 'ok' : 'error') . '">' . ($config_exists ? '✓' : '✗') . '</span>';
        echo '<span>.env file: <strong>' . ($config_exists ? 'Found' : 'Not found') . '</strong></span>';
        echo '</div>';
        
        echo '<div class="status">';
        echo '<span class="status-icon ' . ($api_token ? 'ok' : 'error') . '">' . ($api_token ? '✓' : '✗') . '</span>';
        echo '<span>API Token: <strong>' . ($api_token ? 'Configured' : 'Not configured') . '</strong></span>';
        echo '</div>';
        
        echo '</div>';
        
        echo '<div class="info-box">';
        echo '<strong>📝 Configuration:</strong>';
        echo '<p>API Token: <span class="code">***' . substr(API_TOKEN, -10) . '</span></p>';
        echo '<p>Channel: <span class="code">' . CHANNEL_USERNAME . '</span></p>';
        echo '<p>Group ID: <span class="code">' . GROUP_ID . '</span></p>';
        echo '<p>Admin ID: <span class="code">' . ADMIN_ID . '</span></p>';
        echo '</div>';
        
        // Check webhook
        echo '<div class="info-box">';
        echo '<strong>🌐 Webhook Status:</strong>';
        
        if ($api_token) {
            $curl = curl_init();
            curl_setopt_array($curl, [
                CURLOPT_URL => TELEGRAM_API_URL . '/getWebhookInfo',
                CURLOPT_RETURNTRANSFER => true,
                CURLOPT_TIMEOUT => 5
            ]);
            
            $response = json_decode(curl_exec($curl), true);
            curl_close($curl);
            
            if ($response['ok']) {
                $webhook_url = $response['result']['url'] ?? 'Not set';
                echo '<p>Webhook URL: <span class="code">' . ($webhook_url ? $webhook_url : 'Not set') . '</span></p>';
                echo '<p>Last Error: ' . ($response['result']['last_error_message'] ?? 'None') . '</p>';
                echo '<p>Pending Updates: ' . ($response['result']['pending_update_count'] ?? 0) . '</p>';
            } else {
                echo '<p style="color: #f44336;">❌ Failed to get webhook info</p>';
            }
        } else {
            echo '<p style="color: #f44336;">❌ API Token not configured</p>';
        }
        
        echo '</div>';
        
        // Check data files
        echo '<div class="info-box">';
        echo '<strong>💾 Data Storage:</strong>';
        
        $leads_count = count(getLeads());
        echo '<p>Stored Leads: <strong>' . $leads_count . '</strong></p>';
        
        $sessions_file = __DIR__ . '/sessions.json';
        $sessions_count = file_exists($sessions_file) ? count(json_decode(file_get_contents($sessions_file), true) ?: []) : 0;
        echo '<p>Active Sessions: <strong>' . $sessions_count . '</strong></p>';
        
        echo '</div>';
        ?>
        
        <div class="buttons">
            <h3 style="margin-bottom: 15px;">🔗 Quick Links:</h3>
            <a href="webhook.php" class="command-btn">⚙️ Set Webhook</a>
            <a href="https://t.me/registan_abituriyent" class="command-btn" target="_blank">📢 Open Channel</a>
            <a href="https://t.me/<?php echo str_replace('@', '', API_TOKEN === 'demo' ? 'registan_abituriyent' : 'registan_abituriyent'); ?>" class="command-btn" target="_blank">💬 Start Bot</a>
        </div>
        
        <div class="footer">
            <p>DTM Bot - PHP Edition | Made with ❤️ for Telegram</p>
            <p>For support, visit: <a href="https://telegram.me/registan_abituriyent" target="_blank">@registan_abituriyent</a></p>
        </div>
    </div>
</body>
</html>
