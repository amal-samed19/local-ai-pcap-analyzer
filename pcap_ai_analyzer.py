import sys
import click
import ollama
from collections import Counter
from scapy.all import rdpcap, IP, TCP, UDP, Raw
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

SYSTEM_PROMPT = """
You are a Senior Network Security Analyst and Incident Responder.
Analyze the provided packet capture summary extracted from a .pcap file.

Structure your report in Markdown using these exact headings:
1. EXECUTIVE SUMMARY: High-level overview of observed network behavior.
2. TRAFFIC ANOMALIES & POTENTIAL THREATS: Detail suspicious IPs, targeted ports, or payloads.
3. MITRE ATT&CK MAPPING: Map detected patterns to tactics/techniques (e.g., Reconnaissance, Initial Access).
4. INCIDENT RESPONSE ACTIONS: Provide concrete terminal commands or firewall steps to mitigate the findings.
"""

def extract_pcap_features(pcap_path: str) -> str:
    console.print(f"[bold cyan][*] Parsing PCAP telemetry from: {pcap_path}...[/bold cyan]")
    try:
        packets = rdpcap(pcap_path)
    except Exception as e:
        console.print(f"[bold red][!] Error reading PCAP file: {e}[/bold red]")
        sys.exit(1)

    ip_sources = Counter()
    ip_destinations = Counter()
    conversations = Counter()
    port_activity = Counter()
    payload_samples = []

    for pkt in packets:
        if IP in pkt:
            src = pkt[IP].src
            dst = pkt[IP].dst
            ip_sources[src] += 1
            ip_destinations[dst] += 1

            proto = "TCP" if TCP in pkt else ("UDP" if UDP in pkt else "OTHER")
            dport = pkt[TCP].dport if TCP in pkt else (pkt[UDP].dport if UDP in pkt else 0)

            conversations[(src, dst, proto, dport)] += 1
            port_activity[dport] += 1

            if Raw in pkt and len(payload_samples) < 5:
                raw_data = bytes(pkt[Raw].load)[:100]
                payload_samples.append(f"{src} -> {dst}:{dport} | Payload: {raw_data}")

    summary_lines = [
        f"Total Packets Analyzed: {len(packets)}",
        "\nTop Source IPs:",
        *[f"- {ip}: {count} packets" for ip, count in ip_sources.most_common(5)],
        "\nTop Targeted Destination Ports:",
        *[f"- Port {port}: {count} occurrences" for port, count in port_activity.most_common(5)],
        "\nActive Conversations:",
        *[f"- {src} -> {dst} [{proto}:{dport}]: {count} packets" for (src, dst, proto, dport), count in conversations.most_common(5)]
    ]

    if payload_samples:
        summary_lines.append("\nSample Payload Snippets:")
        summary_lines.extend([f"- {p}" for p in payload_samples])

    return "\n".join(summary_lines)

@click.command()
@click.option('--pcap', '-p', required=True, type=click.Path(exists=True), help='Path to .pcap capture file.')
@click.option('--model', '-m', default='llama3.2:3b', help='Local Ollama model.')
@click.option('--output', '-o', type=click.Path(), help='Save Markdown report to file.')
def main(pcap, model, output):
    summary_text = extract_pcap_features(pcap)
    
    console.print(f"[bold cyan][*] Sending extracted network telemetry to local LLM ({model})...[/bold cyan]\n")
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Analyze this network traffic summary:\n\n{summary_text}"}
    ]

    try:
        response = ollama.chat(model=model, messages=messages)
        report_md = response['message']['content']
    except Exception as e:
        console.print(f"[bold red][!] Ollama communication failed: {e}[/bold red]")
        sys.exit(1)

    console.print(Panel(Markdown(report_md), title="[bold green]AI Incident Response Report[/bold green]", border_style="green"))

    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(report_md)
        console.print(f"\n[bold blue][+] Analysis successfully saved to: {output}[/bold blue]")

if __name__ == '__main__':
    main()
