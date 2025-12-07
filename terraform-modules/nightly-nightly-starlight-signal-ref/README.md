# Nightly Starlight Signal Reflector

Deploys a serverless web endpoint that reflects incoming 'starlight signals' back to the sender, ensuring cosmic communication echoes across the digital void. This utility provides a simple, robust way to establish a reflective communication channel, useful for testing cosmic message relays or just sending echoes into the abyss.

## 🌌 Features

*   **Serverless Deployment**: Utilizes AWS Lambda and API Gateway for a highly available and scalable reflector.
*   **Signal Reflection**: Echoes any incoming HTTP request body back as part of a JSON response.
*   **Whimsical ID**: Each reflector instance gets a unique, whimsical ID for tracking its cosmic echoes.
*   **Terraform Managed**: Infrastructure-as-Code for easy deployment, updates, and teardown.

## 🚀 Deployment

This utility is a Terraform module. To deploy it, you'll need:

*   [Terraform CLI](https://www.terraform.io/downloads) (v1.0.0 or higher)
*   [AWS CLI](https://aws.amazon.com/cli/) configured with appropriate credentials.

1.  **Navigate to the module directory**:
    ```bash
    cd terraform-modules/nightly-starlight-signal-reflec/src
    ```

2.  **Initialize Terraform**:
    ```bash
    terraform init
    ```

3.  **Review the plan**:
    ```bash
    terraform plan
    ```

4.  **Apply the configuration**:
    ```bash
    terraform apply
    ```
    Confirm with `yes` when prompted.

5.  **Retrieve the API Gateway URL**:
    After successful deployment, Terraform will output the `api_gateway_url`.
    ```bash
    terraform output api_gateway_url
    ```
    This URL is your Starlight Signal Reflector endpoint.

## 📡 Usage

Once deployed, you can send HTTP requests (GET, POST, PUT, etc.) to the `api_gateway_url`. The Lambda function will capture the request body and reflect it back in a JSON response.

### Example (using `curl`):

```bash
# Replace with your actual API Gateway URL
API_URL=$(terraform output -raw api_gateway_url)

echo "Sending a starlight signal to: $API_URL"

# Send a simple text signal
curl -X POST -H "Content-Type: text/plain" -d "Hello, cosmic void!" "$API_URL"

# Send a JSON signal
curl -X POST -H "Content-Type: application/json" -d '{"source": "Earth", "message": "Echo test 1-2-3"}' "$API_URL"

# Send a GET request (body will be empty, but still reflected)
curl "$API_URL"
```

The response will be a JSON object containing a confirmation message and the `received_signal` (your original request body).

## 🗑️ Teardown

To remove all deployed resources:

1.  **Navigate to the module directory**:
    ```bash
    cd terraform-modules/nightly-starlight-signal-reflec/src
    ```

2.  **Destroy the resources**:
    ```bash
    terraform destroy
    ```
    Confirm with `yes` when prompted.

## 🧪 Testing

The utility includes a self-contained test script that uses a mocked `terraform` binary to ensure deterministic and offline validation of the module's structure and expected outputs.

To run the tests:

```bash
cd terraform-modules/nightly-starlight-signal-reflec
./tests/test_module.sh
```

**Mock rationale:** Terraform commands (`init`, `validate`, `apply`, `output`) interact with the filesystem, download providers, and potentially communicate with cloud APIs. To ensure deterministic and offline testing, the `terraform` binary is mocked. This mock simulates successful execution and predefined outputs, allowing the test script to verify the module's structure and expected behavior without actual cloud resource provisioning or network calls.
