TEMPLATE_USERS = [
    (
        "verified@jordanenrico.com",
        "$argon2id$v=19$m=65536,t=3,p=4$FIOSFxU5dLbvAheMz2FcAQ$1sc66gbBVsUY1ZA9YT7QWQH30XOmIeVD5dXRhw3ZUHU",
        True,
        False,
        "d9ad00d8-29ac-4993-a272-ce649fb41080",
    ),
    (
        "unverified@jordanenrico.com",
        "$argon2id$v=19$m=65536,t=3,p=4$FIOSFxU5dLbvAheMz2FcAQ$1sc66gbBVsUY1ZA9YT7QWQH30XOmIeVD5dXRhw3ZUHU",
        False,
        False,
        "d9ad00d8-29ac-4993-a272-ce649fb41080",
    ),
    (
        "banned@jordanenrico.com",
        "$argon2id$v=19$m=65536,t=3,p=4$FIOSFxU5dLbvAheMz2FcAQ$1sc66gbBVsUY1ZA9YT7QWQH30XOmIeVD5dXRhw3ZUHU",
        True,
        True,
        "0b56adf8-188b-42b2-84f3-eeb5d59f3a33",
    ),
    (
        "budi@jordanenrico.com",
        "$argon2id$v=19$m=65536,t=3,p=4$FIOSFxU5dLbvAheMz2FcAQ$1sc66gbBVsUY1ZA9YT7QWQH30XOmIeVD5dXRhw3ZUHU",
        True,
        False,
        "0b56adf8-188b-42b2-84f3-eeb5d59f3a33",
    ),
]

TEMPLATE_CAPABILITIES = [
    (
        "bc2095d1-0cae-4072-85f1-5ddfc7f23542",
        "user:create",
        "Create a new user",
        "035979f1-a325-4803-869e-c698103578ed",
    ),
    (
        "3f753691-ff0b-4354-a99f-cacdae1b2535",
        "user:read",
        "Read user information",
        "035979f1-a325-4803-869e-c698103578ed",
    ),
    (
        "18d03d3b-e417-4cb0-97f3-5adb06a60f0a",
        "user:update",
        "Update user information",
        "035979f1-a325-4803-869e-c698103578ed",
    ),
    (
        "7b245ec2-f586-43e0-a979-d45ee1cd2c97",
        "user:delete",
        "Delete a user",
        "035979f1-a325-4803-869e-c698103578ed",
    ),
    (
        "aecf56da-77f1-4980-b648-7b1692114840",
        "user:reset_password",
        "Reset a user's password",
        "035979f1-a325-4803-869e-c698103578ed",
    ),
    (
        "bdbf0d89-e534-4fe5-994f-a7987124296c",
        "user:ban",
        "Ban a user",
        "035979f1-a325-4803-869e-c698103578ed",
    ),
    (
        "b98a32e9-60ec-4ac6-8132-034cf83ad075",
        "user:unban",
        "Unban a user",
        "035979f1-a325-4803-869e-c698103578ed",
    ),
    (
        "f76060a6-e6d8-42f2-bb22-c6551ff65f85",
        "chat:invoke",
        "Invoke the chat",
        "9a8063f1-e1bd-4cd0-b4ad-01b93184549e",
    ),
    (
        "2467cc1d-592d-43c2-94bd-852ba4e9cb0f",
        "ocr:extract:invoke",
        "Invoke the ocr extract",
        "f5e5be1a-e0f5-465b-bd25-c19745dbd89e",
    ),
    (
        "9e5c48d6-1632-4e2c-a474-a26c1711f913",
        "ocr:parse:invoke",
        "Invoke the ocr parse",
        "f5e5be1a-e0f5-465b-bd25-c19745dbd89e",
    ),
]

TEMPLATE_ROLES = [
    (
        "d9ad00d8-29ac-4993-a272-ce649fb41080",
        "Templar Knight",
        "The one who protects the light",
    ),
    (
        "0b56adf8-188b-42b2-84f3-eeb5d59f3a33",
        "Dark Templar",
        "The one who wields the darkness",
    ),
]

TEMPLATE_ROLE_CAPABILITIES = [
    ("d9ad00d8-29ac-4993-a272-ce649fb41080", "bc2095d1-0cae-4072-85f1-5ddfc7f23542"),
    ("d9ad00d8-29ac-4993-a272-ce649fb41080", "3f753691-ff0b-4354-a99f-cacdae1b2535"),
    ("d9ad00d8-29ac-4993-a272-ce649fb41080", "18d03d3b-e417-4cb0-97f3-5adb06a60f0a"),
    ("d9ad00d8-29ac-4993-a272-ce649fb41080", "7b245ec2-f586-43e0-a979-d45ee1cd2c97"),
    ("d9ad00d8-29ac-4993-a272-ce649fb41080", "aecf56da-77f1-4980-b648-7b1692114840"),
    ("d9ad00d8-29ac-4993-a272-ce649fb41080", "bdbf0d89-e534-4fe5-994f-a7987124296c"),
    ("d9ad00d8-29ac-4993-a272-ce649fb41080", "b98a32e9-60ec-4ac6-8132-034cf83ad075"),
    ("d9ad00d8-29ac-4993-a272-ce649fb41080", "f76060a6-e6d8-42f2-bb22-c6551ff65f85"),
    ("d9ad00d8-29ac-4993-a272-ce649fb41080", "2467cc1d-592d-43c2-94bd-852ba4e9cb0f"),
    ("d9ad00d8-29ac-4993-a272-ce649fb41080", "9e5c48d6-1632-4e2c-a474-a26c1711f913"),
    ("0b56adf8-188b-42b2-84f3-eeb5d59f3a33", "f76060a6-e6d8-42f2-bb22-c6551ff65f85"),
    ("0b56adf8-188b-42b2-84f3-eeb5d59f3a33", "2467cc1d-592d-43c2-94bd-852ba4e9cb0f"),
    ("0b56adf8-188b-42b2-84f3-eeb5d59f3a33", "9e5c48d6-1632-4e2c-a474-a26c1711f913"),
]

TEMPLATE_MENUS = [
    ("035979f1-a325-4803-869e-c698103578ed", "user", "All user-related capabilities"),
    ("9a8063f1-e1bd-4cd0-b4ad-01b93184549e", "chat", "All chat-related capabilities"),
    ("f5e5be1a-e0f5-465b-bd25-c19745dbd89e", "ocr", "All ocr-related capabilities"),
]
