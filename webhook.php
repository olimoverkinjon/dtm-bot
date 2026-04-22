<?php
// 🚀 WEBHOOK SETUP SCRIPT
// URL: https://yoursite.com/webhook.php

require_once __DIR__ . '/config.php';

// Set webhook
$webhook_url = 'https://yoursite.com/index.php';

$data = [
    'url' => $webhook_url,
    'allowed_updates' => json_encode(['message', 'callback_query'])
];

$curl = curl_init();
curl_setopt_array($curl, [
    CURLOPT_URL => TELEGRAM_API_URL . '/setWebhook',
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => $data
]);

$response = json_decode(curl_exec($curl), true);
curl_close($curl);

echo '<pre>';
echo "Webhook URL: $webhook_url\n";
echo "Response: " . json_encode($response, JSON_PRETTY_PRINT);
echo '</pre>';

// Get webhook info
$curl = curl_init();
curl_setopt_array($curl, [
    CURLOPT_URL => TELEGRAM_API_URL . '/getWebhookInfo',
    CURLOPT_RETURNTRANSFER => true
]);

$webhook_info = json_decode(curl_exec($curl), true);
curl_close($curl);

echo "<h2>Webhook Info:</h2>";
echo '<pre>' . json_encode($webhook_info, JSON_PRETTY_PRINT) . '</pre>';
?>
