# 🛡️ Local AI Threat Intelligence & PCAP Summarizer

A privacy-focused, 100% offline network security analysis tool powered by **Scapy**, **Ollama**, and **Llama 3.2**. 

This application parses raw packet captures (`.pcap`), extracts structured telemetry features (IP traffic volume, top destination ports, active TCP/UDP conversations, and raw payload snippets), and transmits the telemetry to a locally hosted LLM to generate professional SOC incident response reports.

---

## ✨ Features

- **🔒 100% Offline & Private:** Zero cloud dependencies or external API calls. Network packet telemetry never leaves your local system.
- **⚡ Automated Telemetry Parsing:** Utilizes Scapy to aggregate network flows, top source/destination IPs, targeted ports, and suspicious payload samples.
- **🧠 Local AI Security Analyst:** Leverages Ollama and `llama3.2:3b` to triage potential anomalies, map activity to MITRE ATT&CK techniques, and recommend concrete remediation commands.
- **💻 Rich Terminal Output:** Rendered directly in your terminal using formatted Markdown panels and styled color outputs.
- **📄 Exportable Reports:** Automatically exports formatted Markdown reports (`threat_report.md`) for incident logging and documentation.

---

## 🏗️ Architecture Pipeline

```
┌──────────────────┐      ┌────────────────────────┐      ┌─────────────────────────┐
│ Raw Capture File │ ───> │ Scapy Telemetry Engine │ ───> │ Local Ollama (Llama 3.2)│
│  (*.pcap)        │      │ (Feature Extraction)   │      │ (Offline Threat Triage) │
└──────────────────┘      └────────────────────────┘      └─────────────────────────┘
                                                                       │
                                                                       ▼
                                                          ┌─────────────────────────┐
                                                          │ SOC Incident Report     │
                                                          │ (Console & Markdown)    │
                                                          └─────────────────────────┘
```

---

## 🚀 Quickstart Guide

### Prerequisites

- **OS:** Linux or WSL2 (Ubuntu recommended)
- **Python:** Python 3.10+
- **Ollama:** Download and install from [ollama.com](https://ollama.com)

### 1. Clone the Repository
```bash
git clone https://github.com/amal-samed19/local-ai-pcap-analyzer.git
cd local-ai-pcap-analyzer
```

### 2. Set Up Virtual Environment & Dependencies
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required Python dependencies
pip install -r requirements.txt
```

### 3. Pull the Local Model
Ensure Ollama is running, then pull the lightweight Llama 3.2 3B model:
```bash
ollama pull llama3.2:3b
```

---

## 🛠️ Usage

### Step 1: Generate Test Traffic (Optional)
Generate a sample `.pcap` capture file containing synthetic benign traffic and anomaly bursts:
```bash
python3 generate_sample_pcap.py
```

### Step 2: Run the Threat Analyzer
Execute the AI security analyzer against any `.pcap` file:
```bash
python3 pcap_ai_analyzer.py -p sample_traffic.pcap -o threat_report.md
```

### Command Options
- `-p, --pcap`: **(Required)** Path to the input `.pcap` file.
- `-m, --model`: Local Ollama model tag (Default: `llama3.2:3b`).
- `-o, --output`: Optional output path to save the generated Markdown report.

---

## 📋 Sample Output Report Structure

The generated security reports follow a structured SOC incident triage format:

1. **EXECUTIVE SUMMARY:** High-level overview of observed network behavior and protocol distribution.
2. **TRAFFIC ANOMALIES & POTENTIAL THREATS:** Detailed breakdown of suspicious IP activity, abnormal port targeted scanning, and payload snippets.
3. **MITRE ATT&CK MAPPING:** Relevant tactics and techniques (e.g., Reconnaissance [T1595], Initial Access [T1190]).
4. **INCIDENT RESPONSE ACTIONS:** Actionable CLI mitigation commands (e.g., `iptables` rules, firewall blocks, service restarts).

---

## 🧰 Tech Stack

- **Language:** Python 3.12
- **Network Telemetry:** [Scapy](https://scapy.net/)
- **Local AI Engine:** [Ollama](https://ollama.com/) / [Llama 3.2](https://ai.meta.com/llama/)
- **CLI Framework & UI:** [Click](https://click.palletsprojects.com/), [Rich](https://rich.readthedocs.io/)

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.
