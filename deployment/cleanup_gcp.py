"""
GCP Cleanup Script for Content Creation Studio
===============================================
This script provides a comprehensive cleanup of all GCP resources
created by the deployment scripts.

Usage:
    python deployment/cleanup_gcp.py [--all] [--dry-run] [--force]

Options:
    --all       Delete all resources including service account and storage bucket
    --dry-run   Show what would be deleted without actually deleting
    --force     Skip confirmation prompts

Resources cleaned up:
    1. Cloud Run service
    2. Agent Engine deployment
    3. Docker images in Artifact Registry
    4. Service Account (with --all flag)
    5. Cloud Storage bucket (with --all flag)

Prerequisites:
    - Authenticated via `gcloud auth application-default login`
    - Environment variables set in .env file
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import vertexai
from vertexai import agent_engines

# Load environment variables
load_dotenv()

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(message):
    """Print a formatted header."""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{message}{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")

def print_success(message):
    """Print a success message."""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_warning(message):
    """Print a warning message."""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_error(message):
    """Print an error message."""
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_info(message):
    """Print an info message."""
    print(f"{Colors.CYAN}ℹ️  {message}{Colors.END}")

def run_command(cmd, check=True, capture_output=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=check,
            capture_output=capture_output,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def confirm(message, force=False):
    """Ask for user confirmation."""
    if force:
        return True

    response = input(f"{Colors.YELLOW}{message} (yes/no): {Colors.END}").strip().lower()
    return response in ['yes', 'y']

class GCPCleaner:
    """Handles cleanup of GCP resources."""

    def __init__(self, dry_run=False, force=False):
        """Initialize the cleaner with configuration."""
        self.dry_run = dry_run
        self.force = force

        # Load configuration from environment
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        self.region = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        self.service_name = os.getenv("SERVICE_NAME", "content-studio")
        self.agent_resource_name = os.getenv("AGENT_ENGINE_RESOURCE_NAME")

        # Bucket configuration
        bucket_env = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET", "")
        self.bucket_name = bucket_env.replace("gs://", "") if bucket_env else f"{self.project_id}-content-studio"

        # Service account configuration
        self.service_account_name = "content-studio-sa"
        self.service_account_email = f"{self.service_account_name}@{self.project_id}.iam.gserviceaccount.com"

        # Repository configuration
        self.repo_name = "content-studio"

        # Validate required configuration
        if not self.project_id:
            print_error("GOOGLE_CLOUD_PROJECT not set in environment")
            sys.exit(1)

    def print_config(self):
        """Print the current configuration."""
        print_header("GCP Cleanup Configuration")
        print(f"  Project ID: {self.project_id}")
        print(f"  Region: {self.region}")
        print(f"  Service Name: {self.service_name}")
        print(f"  Storage Bucket: gs://{self.bucket_name}")
        print(f"  Service Account: {self.service_account_email}")
        print(f"  Repository: {self.repo_name}")
        if self.agent_resource_name:
            print(f"  Agent Engine: {self.agent_resource_name}")

        if self.dry_run:
            print_warning("\n🔍 DRY RUN MODE - No resources will be deleted")

    def delete_cloud_run_service(self):
        """Delete the Cloud Run service."""
        print_header("Deleting Cloud Run Service")

        # Check if service exists
        check_cmd = f"gcloud run services describe {self.service_name} --region={self.region} --project={self.project_id}"
        exists, _, _ = run_command(check_cmd, check=False)

        if not exists:
            print_info(f"Cloud Run service '{self.service_name}' not found (already deleted or never created)")
            return

        if self.dry_run:
            print_info(f"Would delete Cloud Run service: {self.service_name}")
            return

        # Delete service
        cmd = f"gcloud run services delete {self.service_name} --region={self.region} --project={self.project_id} --quiet"
        success, _, error = run_command(cmd)

        if success:
            print_success(f"Cloud Run service '{self.service_name}' deleted")
        else:
            print_error(f"Failed to delete Cloud Run service: {error}")

    def delete_agent_engine(self):
        """Delete the Agent Engine deployment."""
        print_header("Deleting Agent Engine")

        if not self.agent_resource_name:
            print_info("AGENT_ENGINE_RESOURCE_NAME not set (skipping Agent Engine cleanup)")
            return

        if self.dry_run:
            print_info(f"Would delete Agent Engine: {self.agent_resource_name}")
            return

        try:
            # Initialize Vertex AI
            vertexai.init(
                project=self.project_id,
                location=self.region
            )

            # Get and delete the agent
            print(f"🗑️  Deleting Agent Engine: {self.agent_resource_name}")
            remote_app = agent_engines.get(self.agent_resource_name)
            remote_app.delete(force=True)

            print_success("Agent Engine deleted successfully")

        except Exception as e:
            print_error(f"Failed to delete Agent Engine: {str(e)}")
            print_info("You may need to delete it manually from the Cloud Console")

    def delete_docker_images(self):
        """Delete Docker images from Artifact Registry."""
        print_header("Deleting Docker Images")

        # Check if repository exists
        check_cmd = f"gcloud artifacts repositories describe {self.repo_name} --location={self.region} --project={self.project_id}"
        exists, _, _ = run_command(check_cmd, check=False)

        if not exists:
            print_info(f"Artifact Registry repository '{self.repo_name}' not found")
            return

        # List images
        list_cmd = f"gcloud artifacts docker images list {self.region}-docker.pkg.dev/{self.project_id}/{self.repo_name} --format='value(package)'"
        success, images_output, _ = run_command(list_cmd, check=False)

        if not success or not images_output.strip():
            print_info("No Docker images found in repository")
        else:
            images = [img.strip() for img in images_output.strip().split('\n') if img.strip()]

            if self.dry_run:
                print_info(f"Would delete {len(images)} Docker images:")
                for image in images:
                    print(f"    - {image}")
            else:
                print(f"🗑️  Deleting {len(images)} Docker images...")
                for image in images:
                    delete_cmd = f"gcloud artifacts docker images delete {image} --delete-tags --quiet"
                    success, _, _ = run_command(delete_cmd, check=False)
                    if success:
                        print(f"    ✓ Deleted: {image}")
                    else:
                        print_warning(f"    Failed to delete: {image}")

                print_success("Docker images cleanup completed")

        # Ask about deleting the repository
        if not self.dry_run:
            if confirm(f"Delete Artifact Registry repository '{self.repo_name}'?", self.force):
                delete_repo_cmd = f"gcloud artifacts repositories delete {self.repo_name} --location={self.region} --project={self.project_id} --quiet"
                success, _, _ = run_command(delete_repo_cmd)
                if success:
                    print_success("Artifact Registry repository deleted")
                else:
                    print_error("Failed to delete repository")
            else:
                print_info("Keeping Artifact Registry repository")

    def delete_service_account(self):
        """Delete the service account."""
        print_header("Deleting Service Account")

        # Check if service account exists
        check_cmd = f"gcloud iam service-accounts describe {self.service_account_email} --project={self.project_id}"
        exists, _, _ = run_command(check_cmd, check=False)

        if not exists:
            print_info("Service account not found (already deleted or never created)")
            return

        if self.dry_run:
            print_info(f"Would delete service account: {self.service_account_email}")
            return

        if not confirm(f"Delete service account '{self.service_account_email}'?", self.force):
            print_info("Keeping service account")
            return

        # Remove IAM policy bindings
        roles = [
            "roles/aiplatform.user",
            "roles/run.invoker",
            "roles/storage.objectViewer",
            "roles/logging.logWriter"
        ]

        print("🗑️  Removing IAM policy bindings...")
        for role in roles:
            cmd = f"gcloud projects remove-iam-policy-binding {self.project_id} --member='serviceAccount:{self.service_account_email}' --role='{role}' --quiet"
            run_command(cmd, check=False)

        # Delete service account
        delete_cmd = f"gcloud iam service-accounts delete {self.service_account_email} --project={self.project_id} --quiet"
        success, _, _ = run_command(delete_cmd)

        if success:
            print_success("Service account deleted")
        else:
            print_error("Failed to delete service account")

    def delete_storage_bucket(self):
        """Delete the Cloud Storage bucket."""
        print_header("Deleting Cloud Storage Bucket")

        # Check if bucket exists
        check_cmd = f"gsutil ls -b gs://{self.bucket_name}"
        exists, _, _ = run_command(check_cmd, check=False)

        if not exists:
            print_info(f"Storage bucket 'gs://{self.bucket_name}' not found")
            return

        if self.dry_run:
            print_info(f"Would delete storage bucket: gs://{self.bucket_name}")
            return

        print_warning("This will delete ALL files in the bucket!")
        if not confirm(f"Delete storage bucket 'gs://{self.bucket_name}'?", self.force):
            print_info("Keeping storage bucket")
            return

        # Delete bucket and contents
        delete_cmd = f"gsutil -m rm -r gs://{self.bucket_name}"
        success, _, _ = run_command(delete_cmd)

        if success:
            print_success("Storage bucket deleted")
        else:
            print_error("Failed to delete storage bucket")

    def cleanup_all(self, include_optional=False):
        """Run all cleanup operations."""
        self.print_config()

        if not self.dry_run and not self.force:
            print_warning("\nThis will DELETE the following resources:")
            print("  1. Cloud Run service")
            print("  2. Agent Engine deployment")
            print("  3. Docker images in Artifact Registry")
            if include_optional:
                print("  4. Service Account")
                print("  5. Cloud Storage Bucket")
            print("\n⚠️  This action CANNOT be undone!\n")

            if not confirm("Are you sure you want to proceed?", self.force):
                print_error("Cleanup cancelled")
                sys.exit(0)

        # Core resources (always deleted)
        self.delete_cloud_run_service()
        self.delete_agent_engine()
        self.delete_docker_images()

        # Optional resources (only with --all flag)
        if include_optional:
            self.delete_service_account()
            self.delete_storage_bucket()

        # Print summary
        print_header("Cleanup Complete!")
        print_success("All cleanup operations completed")

        if not include_optional:
            print_info("\nOptional resources were kept:")
            print(f"  - Service Account: {self.service_account_email}")
            print(f"  - Storage Bucket: gs://{self.bucket_name}")
            print("\nRun with --all flag to delete these as well")

        print("\n💡 Note: The following may still exist:")
        print("  - Enabled APIs (these don't cost money)")
        print("  - Cloud Build history")
        print("  - Cloud Logging entries")
        print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Clean up GCP resources for Content Creation Studio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Delete all resources including service account and storage bucket"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without actually deleting"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Skip confirmation prompts"
    )

    args = parser.parse_args()

    # Create cleaner instance
    cleaner = GCPCleaner(dry_run=args.dry_run, force=args.force)

    # Run cleanup
    try:
        cleaner.cleanup_all(include_optional=args.all)
    except KeyboardInterrupt:
        print_error("\nCleanup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Cleanup failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
