import subprocess

def run_text_metrics_docker(text):
    try:
        # Escape text to pass safely into the command
        escaped_text = text.replace('"', '{{quotes}}').replace('!', '{{exclamation}}') \
            .replace('\n', '{{enter}}').replace('#', '{{sharp}}') \
            .replace('&', '{{ampersand}}').replace('%', '{{percent}}') \
            .replace('$', '{{dollar}}')
        
        # Build Docker command
        command = [
            "docker", "run", "--rm", "--link", "pgs_cohmetrix:pgs_cohmetrix",
            "-v", "/home/daniel/Downloads/nilcmetrix:/opt/text_metrics",
            "cohmetrix:focal", "bash", "-c",
            f"python3 run_min.py \"{escaped_text}\""
        ]
        
        # Run the Docker container
        result = subprocess.run(command, text=True, capture_output=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)
        raise


def parse_metrics_output(output):
    # Extract metrics from the Docker output
    metrics = {}
    content = output.split("++")[1].strip()
    pairs = content.split(",")
    for pair in pairs:
        if ":" in pair:
            key, value = pair.split(":")
            metrics[key] = value
    return metrics
