import docker
import sys

def main():
    try:
        client = docker.from_env()
        
        dust_bunnies = {
            "images": [],
            "containers": [],
            "volumes": []
        }

        # Find dangling images
        dangling_images = client.images.list(filters={"dangling": True})
        for img in dangling_images:
            dust_bunnies["images"].append(img.short_id)

        # Find exited containers
        exited_containers = client.containers.list(all=True, filters={"status": "exited"})
        for container in exited_containers:
            dust_bunnies["containers"].append(container.name)

        # Find dangling volumes
        dangling_volumes = client.volumes.list(filters={"dangling": True})
        for vol in dangling_volumes:
            dust_bunnies["volumes"].append(vol.name)

        print("✨ Welcome to the Digital Dust Bunny Sweeper! ✨")
        print("Scanning your Docker environment for forgotten bits and bobs...")
        print("-" * 50)

        total_bunnies = sum(len(v) for v in dust_bunnies.values())

        if total_bunnies == 0:
            print("🎉 Your Docker environment is sparkling clean! No digital dust bunnies found. 🎉")
        else:
            print(f"🧹 Oh dear! I've found {total_bunnies} digital dust bunnies lurking around:")
            if dust_bunnies["images"]:
                print(f"  - {len(dust_bunnies['images'])} dangling images (like forgotten socks behind the dryer):")
                for img_id in dust_bunnies["images"]:
                    print(f"    - Image ID: {img_id}")
            if dust_bunnies["containers"]:
                print(f"  - {len(dust_bunnies['containers'])} exited containers (like empty snack wrappers):")
                for name in dust_bunnies["containers"]:
                    print(f"    - Container Name: {name}")
            if dust_bunnies["volumes"]:
                print(f"  - {len(dust_bunnies['volumes'])} dangling volumes (like lost keys under the couch):")
                for vol_name in dust_bunnies["volumes"]:
                    print(f"    - Volume Name: {vol_name}")
            
            print("-" * 50)
            print("To sweep these digital dust bunnies away, run:")
            print("  docker system prune --volumes")
            print("This command will remove all stopped containers, all networks not used by at least one container,")
            print("all dangling images, and optionally all dangling volumes.")
            print("Use with caution! Always review what will be removed before confirming.")

    except Exception as e:
        print(f"🚨 Oops! The Digital Dust Bunny Sweeper encountered an error: {e}", file=sys.stderr)
        print("Make sure the Docker daemon is running and accessible (e.g., /var/run/docker.sock is mounted).", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
