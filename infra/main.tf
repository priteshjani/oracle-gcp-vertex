provider "google" {
  project = var.host_project_id
  region  = var.region
}

provider "google" {
  alias   = "service"
  project = var.service_project_id
  region  = var.region
}

# --- Shared VPC (Host Project) ---

resource "google_compute_network" "shared_network" {
  name                    = var.network_name
  auto_create_subnetworks = false
  project                 = var.host_project_id
}

resource "google_compute_subnetwork" "app_subnet" {
  name          = "app-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = var.region
  network       = google_compute_network.shared_network.self_link
  project       = var.host_project_id
}

resource "google_compute_shared_vpc_host_project" "host" {
  project = var.host_project_id
}

resource "google_compute_shared_vpc_service_project" "service" {
  host_project    = google_compute_shared_vpc_host_project.host.project
  service_project = var.service_project_id
}

# Grant permissions for the service project to use the host project's subnet
resource "google_compute_subnetwork_iam_binding" "subnet_user" {
  project    = var.host_project_id
  region     = var.region
  subnetwork = google_compute_subnetwork.app_subnet.name
  role       = "roles/compute.networkUser"

  members = [
    "serviceAccount:${var.service_project_id}@cloudservices.gserviceaccount.com",
    # Add the specific Service Account for the App Engine/Cloud Run/GCE if known
    # "serviceAccount:service-PROJECT_NUMBER@gcp-sa-api-mapper.iam.gserviceaccount.com"
  ]
}
