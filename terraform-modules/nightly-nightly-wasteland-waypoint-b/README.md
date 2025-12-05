# Wasteland Waypoint Beacon

## 📡 Signal Detected: Deploy Your Own Digital Waypoint 📡

This Terraform module allows you to deploy a highly available, static content website (your "waypoint beacon") using AWS S3 for storage and AWS CloudFront for global content delivery. In the vast digital wasteland, sometimes all you need is a simple, resilient signal to let others know you're out there.

### Features

*   **Static Website Hosting**: Leverages AWS S3 for cost-effective and scalable static content storage.
*   **Global Content Delivery**: Utilizes AWS CloudFront CDN for low-latency access and high availability worldwide.
*   **Secure Access**: Configures CloudFront Origin Access Control (OAC) for secure access to the S3 bucket, preventing direct public access.
*   **Customizable Content**: Easily deploy your own `index.html` or other static files.

### Usage

To use this module, include it in your Terraform configuration and provide the necessary variables.

1.  **Create a `main.tf` file** (e.g., in a new directory `my-waypoint-deployment/`):

    ```terraform
    module "waypoint_beacon" {
      source = "./path/to/nightly-wasteland-waypoint-beacon/src" # Adjust this path

      bucket_name       = "my-unique-waypoint-bucket-12345"
      region            = "us-east-1"
      content_file_path = "./waypoint_content/index.html" # Path to your local index.html
    }

    output "waypoint_url" {
      description = "The URL of the deployed CloudFront distribution."
      value       = module.waypoint_beacon.cloudfront_domain_name
    }

    output "s3_static_website_endpoint" {
      description = "The S3 static website endpoint (for direct S3 access, not recommended for public use)."
      value       = module.waypoint_beacon.s3_bucket_endpoint
    }
    ```

2.  **Create your static content file** (e.g., `my-waypoint-deployment/waypoint_content/index.html`):

    ```html
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Wasteland Waypoint</title>
        <style>
            body { font-family: monospace; background-color: #1a1a1a; color: #00ff00; text-align: center; padding-top: 50px; }
            h1 { font-size: 3em; text-shadow: 0 0 10px #00ff00; }
            p { font-size: 1.2em; }
            .ascii-art { white-space: pre; font-size: 0.8em; margin: 20px auto; max-width: 600px; }
        </style>
    </head>
    <body>
        <h1>📡 My Wasteland Waypoint Beacon 📡</h1>
        <p>This is my signal. Are you out there?</p>
        <div class="ascii-art">
            <pre>
  _  _  _
 | || || |
 | || || |
 | || || |
 |_||_||_|
 /_______
 \_______/
  |     |
  |_____|
            </pre>
        </div>
        <p>Status: ACTIVE</p>
        <p>Last Updated: <span id="timestamp"></span></p>
        <script>
            document.getElementById('timestamp').innerText = new Date().toLocaleString();
        </script>
    </body>
    </html>
    ```

3.  **Initialize and Apply Terraform**:

    ```bash
    cd my-waypoint-deployment/
    terraform init
    terraform apply
    ```

    Confirm the changes when prompted.

### Inputs

| Name              | Description                                        | Type     | Default | Required |
| :---------------- | :------------------------------------------------- | :------- | :------ | :------- |
| `bucket_name`     | The name for the S3 bucket to store static content. | `string` | n/a     | yes      |
| `region`          | The AWS region to deploy resources in.             | `string` | n/a     | yes      |
| `content_file_path` | The local path to the `index.html` file to upload. | `string` | n/a     | yes      |

### Outputs

| Name                       | Description                                      |
| :------------------------- | :----------------------------------------------- |
| `s3_bucket_endpoint`       | The S3 static website endpoint URL.              |
| `cloudfront_domain_name`   | The domain name of the deployed CloudFront distribution. |

### Requirements

*   Terraform CLI (>= 1.0.0)
*   AWS Provider (>= 5.0)
*   Configured AWS credentials (e.g., via `~/.aws/credentials` or environment variables)
