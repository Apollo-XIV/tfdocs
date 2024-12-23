
# Cloudflare pointing toward load balancer
data "cloudflare_zone" "crease_sh" {
  name = "crease.sh"
}

resource "tls_private_key" "https" {
  algorithm = "RSA"
}

resource "tls_cert_request" "https" {
  private_key_pem = tls_private_key.https.private_key_pem

  subject {
    common_name  = ""
    organization = "TFDocs"
  }
}

resource "cloudflare_origin_ca_certificate" "https" {
  csr = tls_cert_request.https.cert_request_pem
  hostnames = [
    "tfdocs.${data.cloudflare_zone.crease_sh.name}"
  ]
  request_type = "origin-rsa"
}

resource "aws_acm_certificate" "cloudflare_origin" {
  private_key      = tls_private_key.https.private_key_pem
  certificate_body = cloudflare_origin_ca_certificate.https.certificate
}

resource "cloudflare_record" "lb" {
  // forwards traffic from the tfdocs subdomain to the lb CNAME
  zone_id = data.cloudflare_zone.crease_sh.id
  name    = "tfdocs"
  content = aws_lb.entrypoint.dns_name
  type    = "CNAME"
  proxied = true
}
