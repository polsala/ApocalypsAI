import yaml
import random
import argparse

def generate_chaos_compose(num_services=3, network_latency=50, network_loss=5, resource_cpu=0.5, resource_memory=128):
    """Generates a chaotic docker-compose.yml file.

    Args:
        num_services (int): The number of application services to generate.
        network_latency (int): Base network latency in ms.
        network_loss (int): Packet loss percentage.
        resource_cpu (float): CPU cores to allocate per service.
        resource_memory (int): Memory in MB to allocate per service.

    Returns:
        dict: A dictionary representing the docker-compose.yml content.
    """
    services = {
        "chaos_network": {
            "image": "alpine",
            "command": "sleep infinity",
            "networks": {
                "chaos_net": {
                    "aliases": ["chaos_net_alias"]
                }
            },
            "deploy": {
                "resources": {
                    "limits": {
                        "cpus": str(resource_cpu * num_services),
                        "memory": f"{resource_memory * num_services}M"
                    }
                }
            }
        }
    }

    app_services = {}
    for i in range(1, num_services + 1):
        service_name = f"app_service_{i}"
        chaos_service_name = f"chaos_for_{service_name}"
        app_services[service_name] = {
            "image": "nginx:alpine", # Placeholder image
            "container_name": service_name,
            "networks": {
                "chaos_net": {
                    "aliases": [f"{service_name}_alias"]
                }
            },
            "deploy": {
                "resources": {
                    "limits": {
                        "cpus": str(resource_cpu),
                        "memory": f"{resource_memory}M"
                    }
                }
            },
            "depends_on": {
                chaos_service_name: {
                    "condition": "service_started"
                }
            }
        }
        services[chaos_service_name] = {
            "image": "alpine/socat", # For network manipulation
            "container_name": chaos_service_name,
            "command": f"TCP-LISTEN:80,fork TCP-RECV:1000000 TCP-SEND:1000000",
            "network_mode": f"service:{service_name}",
            "cap_add": ["NET_ADMIN"],
            "volumes": ["/lib/modules:/lib/modules"],
            "depends_on": {
                service_name: {
                    "condition": "service_started"
                }
            },
            "entrypoint": "/bin/sh -c 'apk add --no-cache iproute2 tc && tc qdisc add dev eth0 root netem delay {latency}ms {latency_variation}ms distribution normal loss {loss}% {loss_variation}% && exec /usr/bin/socat TCP-LISTEN:80,fork TCP-RECV:1000000 TCP-SEND:1000000'"
        }
        # Injecting random variations for more chaos
        latency_variation = random.randint(0, network_latency // 2)
        loss_variation = random.randint(0, network_loss // 2)
        services[chaos_service_name]["entrypoint"] = services[chaos_service_name]["entrypoint"].format(
            latency=network_latency,
            latency_variation=latency_variation,
            loss=network_loss,
            loss_variation=loss_variation
        )

    services.update(app_services)

    return {
        "version": "3.8",
        "services": services,
        "networks": {
            "chaos_net": {
                "driver": "bridge"
            }
        }
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate chaotic Docker Compose files.")
    parser.add_argument("--services", type=int, default=3, help="Number of application services.")
    parser.add_argument("--network-latency", type=int, default=50, help="Base network latency in ms.")
    parser.add_argument("--network-loss", type=int, default=5, help="Packet loss percentage.")
    parser.add_argument("--resource-cpu", type=float, default=0.5, help="CPU cores to allocate per service.")
    parser.add_argument("--resource-memory", type=int, default=128, help="Memory in MB to allocate per service.")
    parser.add_argument("--output", type=str, default="docker-compose.yml", help="Output filename.")

    args = parser.parse_args()

    compose_config = generate_chaos_compose(
        num_services=args.services,
        network_latency=args.network_latency,
        network_loss=args.network_loss,
        resource_cpu=args.resource_cpu,
        resource_memory=args.resource_memory
    )

    with open(args.output, "w") as f:
        yaml.dump(compose_config, f, indent=2)

    print(f"Generated chaotic compose file: {args.output}")
