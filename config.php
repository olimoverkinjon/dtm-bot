<?php
// 🔥 CONFIGURATION
define('API_TOKEN', getenv('API_TOKEN') ?: '8516827967:AAHDYsWDsYrsM3HBna24ceonbpM9a8zb_Yw');
define('CHANNEL_USERNAME', getenv('CHANNEL_USERNAME') ?: '@registan_abituriyent');
define('GROUP_ID', getenv('GROUP_ID') ?: -1003890628671);
define('ADMIN_ID', getenv('ADMIN_ID') ?: 6653845419);

// Database
define('LEADS_FILE', __DIR__ . '/leads.json');

// Telegram API
define('TELEGRAM_API_URL', 'https://api.telegram.org/bot' . API_TOKEN);

// Helper: Get leads from JSON file
function getLeads() {
    if (file_exists(LEADS_FILE)) {
        return json_decode(file_get_contents(LEADS_FILE), true) ?: [];
    }
    return [];
}

// Helper: Save leads to JSON file
function saveLeads($leads) {
    file_put_contents(LEADS_FILE, json_encode($leads, JSON_PRETTY_PRINT));
}

// Helper: Add lead
function addLead($name, $phone, $extra_phone) {
    $leads = getLeads();
    $leads[] = [
        'name' => $name,
        'phone' => $phone,
        'extra' => $extra_phone,
        'timestamp' => date('Y-m-d H:i:s')
    ];
    saveLeads($leads);
}

// Helper: Send Telegram message
function sendMessage($chat_id, $text, $reply_markup = null) {
    $data = [
        'chat_id' => $chat_id,
        'text' => $text,
        'parse_mode' => 'HTML'
    ];

    if ($reply_markup) {
        $data['reply_markup'] = json_encode($reply_markup);
    }

    $curl = curl_init();
    curl_setopt_array($curl, [
        CURLOPT_URL => TELEGRAM_API_URL . '/sendMessage',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => $data
    ]);

    return curl_exec($curl);
}

// Helper: Check channel subscription
function checkSubscription($user_id) {
    $curl = curl_init();
    curl_setopt_array($curl, [
        CURLOPT_URL => TELEGRAM_API_URL . '/getChatMember?chat_id=' . urlencode(CHANNEL_USERNAME) . '&user_id=' . $user_id,
        CURLOPT_RETURNTRANSFER => true
    ]);

    $response = json_decode(curl_exec($curl), true);
    curl_close($curl);

    if (!isset($response['result']['status'])) {
        return false;
    }

    $status = $response['result']['status'];
    return in_array($status, ['member', 'administrator', 'creator']);
}

// Helper: Get or create session
function getSession($user_id) {
    $sessions_file = __DIR__ . '/sessions.json';
    $sessions = file_exists($sessions_file) ? json_decode(file_get_contents($sessions_file), true) : [];

    return $sessions[$user_id] ?? [];
}

// Helper: Save session
function saveSession($user_id, $state, $data = []) {
    $sessions_file = __DIR__ . '/sessions.json';
    $sessions = file_exists($sessions_file) ? json_decode(file_get_contents($sessions_file), true) : [];

    $sessions[$user_id] = [
        'state' => $state,
        'data' => $data
    ];

    file_put_contents($sessions_file, json_encode($sessions, JSON_PRETTY_PRINT));
}

// Helper: Delete session
function deleteSession($user_id) {
    $sessions_file = __DIR__ . '/sessions.json';
    $sessions = file_exists($sessions_file) ? json_decode(file_get_contents($sessions_file), true) : [];

    unset($sessions[$user_id]);
    file_put_contents($sessions_file, json_encode($sessions, JSON_PRETTY_PRINT));
}

// Helper: Create inline keyboard
function createInlineKeyboard($buttons) {
    return [
        'inline_keyboard' => [$buttons]
    ];
}

// Helper: Create reply keyboard
function createReplyKeyboard($buttons) {
    return [
        'keyboard' => [$buttons],
        'resize_keyboard' => true,
        'one_time_keyboard' => false
    ];
}

// Helper: Remove keyboard
function removeKeyboard() {
    return [
        'remove_keyboard' => true
    ];
}
?>
