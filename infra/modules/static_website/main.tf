resource "azurerm_static_site" "neena_core_static_app" {
  name                  = var.static_website_name
  resource_group_name   = var.resource_group_name
  location              = var.location
  sku_tier              = "Free"
}

resource "azurerm_static_site_custom_domain" "custom_domain" {
  static_site_id  = azurerm_static_site.neena_core_static_app.id
  domain_name     = var.domain_name
  validation_type = "dns-txt-token"
}