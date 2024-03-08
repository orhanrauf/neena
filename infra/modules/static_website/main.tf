resource "azurerm_static_site" "neena_core_static_app" {
  name                  = var.static_website_name
  resource_group_name   = var.resource_group_name
  location              = var.location
  sku_tier              = "Free"
}