#!/bin/bash
# Solicita el primer certificado de Let's Encrypt para DOMAIN (definido en .env),
# usando nip.io como "dominio" gratuito basado en la IP publica del VPS
# (ej: DOMAIN=203.0.113.42.nip.io -> no requiere comprar ni configurar ningun DNS).
#
# Se corre UNA sola vez, desde la raiz del repo:
#   bash deploy/certbot/init-letsencrypt.sh
#
# La renovacion automatica despues de esto la hace el servicio "certbot"
# de docker-compose.yml (corre "certbot renew" cada 12h).

set -e

if [ ! -f .env ]; then
  echo "Error: corre este script desde la raiz del proyecto (no se encontro .env)."
  exit 1
fi

set -a
source .env
set +a

if [ -z "$DOMAIN" ] || [ -z "$LETSENCRYPT_EMAIL" ]; then
  echo "Error: define DOMAIN y LETSENCRYPT_EMAIL en tu .env antes de continuar."
  echo "Ejemplo: DOMAIN=203.0.113.42.nip.io  (usa la IP publica de tu VPS)"
  exit 1
fi

conf_path="./deploy/certbot/conf"
www_path="./deploy/certbot/www"
rsa_key_size=4096

mkdir -p "$conf_path/live/$DOMAIN" "$www_path"

if [ ! -e "$conf_path/options-ssl-nginx.conf" ]; then
  echo "### Escribiendo configuracion TLS recomendada ..."
  cat > "$conf_path/options-ssl-nginx.conf" <<'EOF'
ssl_session_cache shared:le_nginx_SSL:10m;
ssl_session_timeout 1440m;
ssl_session_tickets off;

ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers off;

ssl_ciphers "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384";
EOF
fi

if [ ! -e "$conf_path/ssl-dhparams.pem" ]; then
  echo "### Generando parametros Diffie-Hellman (puede tardar ~1 min) ..."
  openssl dhparam -out "$conf_path/ssl-dhparams.pem" 2048
fi

echo "### Creando certificado dummy para que nginx pueda arrancar ..."
docker compose run --rm --entrypoint "\
  openssl req -x509 -nodes -newkey rsa:$rsa_key_size -days 1 \
    -keyout '/etc/letsencrypt/live/$DOMAIN/privkey.pem' \
    -out '/etc/letsencrypt/live/$DOMAIN/fullchain.pem' \
    -subj '/CN=localhost'" certbot
echo

echo "### Levantando nginx (con el dummy) ..."
docker compose up -d nginx
echo

echo "### Borrando certificado dummy ..."
docker compose run --rm --entrypoint "\
  rm -rf /etc/letsencrypt/live/$DOMAIN && \
  rm -rf /etc/letsencrypt/archive/$DOMAIN && \
  rm -rf /etc/letsencrypt/renewal/$DOMAIN.conf" certbot
echo

echo "### Solicitando certificado real de Let's Encrypt para $DOMAIN ..."
docker compose run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    --email $LETSENCRYPT_EMAIL \
    -d $DOMAIN \
    --rsa-key-size $rsa_key_size \
    --agree-tos \
    --non-interactive" certbot
echo

echo "### Recargando nginx con el certificado real ..."
docker compose exec nginx nginx -s reload

echo
echo "Listo. Tu API deberia estar disponible en https://$DOMAIN"
