output "application_id" {
  value       = azuread_application.service_principal.application_id
  description = "The Application ID of the created Azure AD application."
}

output "service_principal_id" {
  value       = azuread_service_principal.service_principal.id
  description = "The ID of the created service principal."
}

output "service_principal_password" {
  value       = azuread_service_principal_password.service_principal.value
  description = "The password of the created service principal."
}
