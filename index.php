<?php
require_once __DIR__ . '/config.php';

// Get webhook data
$content = file_get_contents('php://input');
$update = json_decode($content, true);

if (!$update) {
    http_response_code(200);
    echo json_encode(['ok' => true]);
    exit;
}

// Extract update data
$message = $update['message'] ?? null;
$callback_query = $update['callback_query'] ?? null;

// ==================
// MESSAGE HANDLERS
// ==================

if ($message) {
    $user_id = $message['from']['id'];
    $chat_id = $message['chat']['id'];
    $text = $message['text'] ?? '';
    $contact = $message['contact'] ?? null;

    // 🚀 /start command
    if (substr($text, 0, 6) === '/start') {
        handleStart($user_id, $chat_id);
        exit;
    }

    // 👨‍💼 /admin command
    if (substr($text, 0, 6) === '/admin') {
        handleAdmin($user_id, $chat_id);
        exit;
    }

    // Get user session
    $session = getSession($user_id);
    $state = $session['state'] ?? null;
    $data = $session['data'] ?? [];

    // 👤 NAME state
    if ($state === 'waiting_name') {
        handleName($user_id, $chat_id, $text);
        exit;
    }

    // 📞 PHONE state (contact button)
    if ($state === 'waiting_phone' && $contact) {
        handlePhone($user_id, $chat_id, $contact['phone_number'], $data);
        exit;
    }

    // 📱 EXTRA PHONE state
    if ($state === 'waiting_extra_phone') {
        handleExtraPhone($user_id, $chat_id, $text, $data);
        exit;
    }
}

// ==================
// CALLBACK HANDLERS
// ==================

if ($callback_query) {
    $user_id = $callback_query['from']['id'];
    $callback_data = $callback_query['data'];
    $message_id = $callback_query['message']['message_id'];
    $chat_id = $callback_query['message']['chat']['id'];
    $callback_id = $callback_query['id'];

    // Check subscription callback
    if ($callback_data === 'check_sub') {
        handleCheckSub($user_id, $chat_id, $callback_id);
        exit;
    }

    // Admin - Show stats
    if ($callback_data === 'stat') {
        if ($user_id !== ADMIN_ID) {
            answerCallbackQuery($callback_id, '❌ Faqat admin uchun!', true);
            exit;
        }
        handleStats($user_id, $chat_id);
        exit;
    }

    // Admin - Show leads
    if ($callback_data === 'leads') {
        if ($user_id !== ADMIN_ID) {
            answerCallbackQuery($callback_id, '❌ Faqat admin uchun!', true);
            exit;
        }
        handleLeads($user_id, $chat_id);
        exit;
    }
}

http_response_code(200);
echo json_encode(['ok' => true]);

// ==================
// FUNCTION HANDLERS
// ==================

function handleStart($user_id, $chat_id) {
    // Check subscription
    if (!checkSubscription($user_id)) {
        $keyboard = createInlineKeyboard([
            [
                ['text' => '📢 Kanalga obuna bo\'lish', 'url' => 'https://t.me/registan_abituriyent'],
                ['text' => '✅ Tekshirish', 'callback_data' => 'check_sub']
            ]
        ]);

        sendMessage($chat_id, '❗️Avval kanalga obuna bo\'ling:', $keyboard);
        return;
    }

    // Clear session
    deleteSession($user_id);

    // Ask for name
    sendMessage($chat_id, '📝 Ism va familiyangizni kiriting:');
    saveSession($user_id, 'waiting_name');
}

function handleCheckSub($user_id, $chat_id, $callback_id) {
    if (!checkSubscription($user_id)) {
        answerCallbackQuery($callback_id, '❌ Hali obuna bo\'lmadingiz', true);
        return;
    }

    answerCallbackQuery($callback_id, '✅ Tekshirildi!', false);

    // Clear session
    deleteSession($user_id);

    // Ask for name
    sendMessage($chat_id, '📝 Ism va familiyangizni kiriting:');
    saveSession($user_id, 'waiting_name');
}

function handleName($user_id, $chat_id, $name) {
    // Save name and ask for phone
    $session = getSession($user_id);
    $session['data']['name'] = htmlspecialchars($name);

    $keyboard = createReplyKeyboard([
        [['text' => '📱 Raqamni yuborish', 'request_contact' => true]]
    ]);

    sendMessage($chat_id, '📞 Telefon raqamingizni yuboring:', $keyboard);
    saveSession($user_id, 'waiting_phone', $session['data']);
}

function handlePhone($user_id, $chat_id, $phone, $data) {
    // Save phone and ask for extra phone
    $data['phone'] = $phone;

    sendMessage($chat_id, '📱 Qo\'shimcha raqam kiriting:', removeKeyboard());
    saveSession($user_id, 'waiting_extra_phone', $data);
}

function handleExtraPhone($user_id, $chat_id, $extra_phone, $data) {
    $extra_phone = trim($extra_phone);

    // Validate: Only digits
    if (!ctype_digit($extra_phone)) {
        sendMessage($chat_id, '❌ Faqat raqam kiriting! (masalan: 901234567)');
        return;
    }

    // Validate: Length
    if (strlen($extra_phone) < 7) {
        sendMessage($chat_id, '❌ Raqam juda qisqa!');
        return;
    }

    // Save lead
    addLead($data['name'], $data['phone'], $extra_phone);

    // Send notification to group
    $text = "🧾 <b>Yangi LID</b>\n\n"
        . "👤 <b>Ism:</b> " . htmlspecialchars($data['name']) . "\n"
        . "📞 <b>Asosiy:</b> " . htmlspecialchars($data['phone']) . "\n"
        . "📱 <b>Qo'shimcha:</b> " . htmlspecialchars($extra_phone) . "\n\n"
        . "📍 <b>Manba:</b> Telegram bot";

    sendMessage(GROUP_ID, $text);

    // Confirm to user
    sendMessage($chat_id, '✅ Ro\'yxatdan o\'tdingiz! Tez orada administratorlarimiz siz bilan bog\'lanishadi.');

    // Clear session
    deleteSession($user_id);
}

function handleAdmin($user_id, $chat_id) {
    if ($user_id !== ADMIN_ID) {
        return;
    }

    $keyboard = createInlineKeyboard([
        [
            ['text' => '📊 Statistika', 'callback_data' => 'stat'],
            ['text' => '📥 Oxirgi lidlar', 'callback_data' => 'leads']
        ]
    ]);

    sendMessage($chat_id, '👨‍💼 Admin panel:', $keyboard);
}

function handleStats($user_id, $chat_id) {
    $leads = getLeads();
    $count = count($leads);

    sendMessage($chat_id, "📊 <b>Jami lidlar:</b> <code>$count</code>");
}

function handleLeads($user_id, $chat_id) {
    $leads = getLeads();

    if (empty($leads)) {
        sendMessage($chat_id, '❌ Hozircha lid yo\'q');
        return;
    }

    // Get last 5 leads
    $recent_leads = array_slice($leads, -5);

    $text = "📥 <b>Oxirgi lidlar:</b>\n\n";

    foreach ($recent_leads as $lead) {
        $text .= "👤 " . htmlspecialchars($lead['name']) 
            . " | 📞 " . htmlspecialchars($lead['phone']) 
            . " | 📱 " . htmlspecialchars($lead['extra']) 
            . "\n";
    }

    sendMessage($chat_id, $text);
}

function answerCallbackQuery($callback_id, $text, $show_alert = false) {
    $data = [
        'callback_query_id' => $callback_id,
        'text' => $text,
        'show_alert' => $show_alert ? 'true' : 'false'
    ];

    $curl = curl_init();
    curl_setopt_array($curl, [
        CURLOPT_URL => TELEGRAM_API_URL . '/answerCallbackQuery',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => $data
    ]);

    curl_exec($curl);
    curl_close($curl);
}
?>
