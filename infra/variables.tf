variable "region" {
  description = "Default AWS region"
  type        = string
  default     = "us-east-2"
}

variable "account_id" {
  description = "My AWS account ID"
  type        = string
}

variable "domain" {
  default = "parsed-jobs-opensearch"
}

variable "OS_master_user_name" {
  description = "Master user name for OpenSearch"
  type        = string
}

variable "OS_master_user_password" {
  description = "Master user password for OpenSearch"
  type        = string
}

