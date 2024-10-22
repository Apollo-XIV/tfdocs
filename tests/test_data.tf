terraform {
  required_providers {
    # local = {
    # source = "hashicorp/local"
    # }
    # time = {
    # source = "hashicorp/time"
    # }
    aws = {
      source = "hashicorp/aws"
    }
    gcp = {
      source = "hashicorp/google"
    }
    azure = {
      source = "hashicorp/azurerm"
    }
  }
}
