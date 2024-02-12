resource "azuread_application" "service_principal" {
  display_name = var.application_name
}

resource "azuread_service_principal" "service_principal" {
    client_id = azuread_application.service_principal.application_id
}

resource "azuread_service_principal_password" "service_principal" {
  service_principal_id = azuread_service_principal.example.id
  end_date            = var.password_end_date
}