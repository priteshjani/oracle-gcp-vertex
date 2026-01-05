variable "host_project_id" {
  description = "The ID of the host project where Shared VPC and Oracle DB reside"
  type        = string
}

variable "service_project_id" {
  description = "The ID of the service project where the application resides"
  type        = string
}

variable "region" {
  description = "The GCP region for resources"
  type        = string
  default     = "us-central1"
}

variable "network_name" {
  description = "The name of the Shared VPC network"
  type        = string
  default     = "retail-shared-vpc"
}

variable "oracle_cidr_range" {
  description = "CIDR range for the Oracle Database peering"
  type        = string
  default     = "10.1.0.0/24"
}
