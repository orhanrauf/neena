variable "application_name" {
  type        = string
  description = "The display name of the Azure AD application."
}

variable "password_end_date" {
  type        = string
  description = "The end date until which the password is valid."
  default     = "2299-12-30T23:00:00Z" # Far in the future, adjust as needed.
}
