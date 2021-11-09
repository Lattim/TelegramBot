Для того, чтобы прочитать подробную инструкцию по само подписным сертификатам переходи - https://core.telegram.org/bots/webhooks#a-self-signed-certificate

Я испоьзовал вот такую команду в OpenSSL: openssl req -newkey rsa:2048 -sha256 -nodes -keyout ssl_private.key -x509 -days 365 -out ssl_cert.pem -subj "/C="страна"/ST="Город"/L="Город"/O="здесь писал никнейм"/CN="апи сервера""

Создаеются файлы:
1. ssl_private.key - приватный ключ
2. ssl_cert.pem - публичный ключ

Файлы надо положить в папку SSL.
