# Nightly Hopeful Quote Deployer

Deploys a single text file containing a hopeful quote to a specified directory on target hosts. Ideal for adding morale‑boosting messages to servers in a post‑apocalyptic setting.

## Variables

- `quote` (string, required): The quote to write.
- `dest_dir` (string, default: `/tmp/quotes`): Destination directory.
- `dest_file` (string, default: `quote.txt`): Filename.

## Usage

```sh
ansible-playbook -i inventory.ini src/playbook.yml -e "quote='Even in the wasteland, hope blooms.' dest_dir=/opt/morale"
```

The playbook will ensure the directory exists and write the quote to the file.

## Testing

Run the bundled test playbook:

```sh
ansible-playbook -i inventory.ini tests/test_playbook.yml
```

It will execute the deployment with a test quote and verify the file content.
