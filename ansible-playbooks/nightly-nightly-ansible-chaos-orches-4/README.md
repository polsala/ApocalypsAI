# Nightly Ansible Chaos Orchestrator

A whimsical-yet-useful Ansible playbook that orchestrates chaos engineering experiments across your infrastructure with randomized scenarios and detailed reporting.

## Features

- **Randomized Chaos Scenarios**: Network latency, packet loss, service restarts, resource exhaustion, and time manipulation
- **Whimsical Scenario Names**: "The Great Firewall of Wasteland", "The Hungry Hungry Processors", "The Time Warp Tango"
- **Detailed Reporting**: Generates comprehensive HTML reports with scenario details and system impact
- **Safe Execution**: All chaos experiments are isolated and have built-in cleanup
- **Configurable**: Easy to customize chaos scenarios and target hosts

## Requirements

- Ansible 2.10+
- Python 3.8+
- Root or sudo access on target hosts
- `tc` (traffic control) for network chaos
- `stress` for resource exhaustion

## Usage

1. Clone this repository
2. Update the `inventory` file with your target hosts
3. Customize chaos scenarios in `vars/chaos_scenarios.yml`
4. Run the playbook:

```bash
./run_chaos.sh
```

## Example Output

```
PLAY [chaos_targets] ***********************************************************

TASK [Gathering Facts] *********************************************************
ok: [server1]
ok: [server2]

TASK [chaos : Randomly select chaos scenario] **********************************
ok: [server1]
ok: [server2]

TASK [chaos : Execute network latency chaos] ***********************************
skipping: [server1]
skipping: [server2]

TASK [chaos : Execute service restart chaos] ***********************************
skipping: [server1]
skipping: [server2]

TASK [chaos : Execute resource exhaustion chaos] *******************************
skipping: [server1]
skipping: [server2]

TASK [chaos : Execute time manipulation chaos] *********************************
ok: [server1]
ok: [server2]

PLAY [chaos_targets] ***********************************************************

TASK [Gathering Facts] *********************************************************
ok: [server1]
ok: [server2]

TASK [cleanup : Remove chaos effects] ******************************************
ok: [server1]
ok: [server2]

PLAY [chaos_targets] ***********************************************************

TASK [Gathering Facts] *********************************************************
ok: [server1]
ok: [server2]

TASK [reporting : Generate chaos report] ****************************************
ok: [server1]
ok: [server2]

PLAY RECAP *********************************************************************
server1                    : ok=6    changed=0    unreachable=0    failed=0    skipped=3    rescued=0    ignored=0   
server2                    : ok=6    changed=0    unreachable=0    failed=0    skipped=3    rescued=0    ignored=0   
```

## License

MIT License - see LICENSE file for details.
