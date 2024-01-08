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
