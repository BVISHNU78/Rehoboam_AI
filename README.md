# Rehoboam_AI

**Rehoboam_AI** is an AI-powered **Open Source Intelligence (OSINT) prediction system** designed to gather real-time intelligence from the open web and generate strategic insights, forecasts, and risk assessments.

The system uses **SearXNG meta-search** to collect information from multiple sources and analyzes it using **local AI models via Ollama**.

---

# Overview

Rehoboam_AI combines **OSINT data collection with local AI analysis** to create an automated intelligence pipeline.

Core technologies:

* **SearXNG** – Meta-search engine for OSINT data collection
* **Ollama** – Local AI model runtime
* **LLM Models** – Event analysis, summarization, and forecasting
* **OSINT Collector** – Automated intelligence gathering
* **Prediction Engine** – Risk scoring and trend analysis

---

# Features

* 🌐 Multi-source OSINT data aggregation
* 🔎 Real-time intelligence gathering
* 🧠 AI-powered event analysis
* 📊 Risk scoring and predictive insights
* 🔐 Privacy-friendly search via SearXNG
* 🖥️ Local AI processing using Ollama
* ⚙️ Modular and extensible architecture

---

# System Architecture

```id="m9ny3c"
User / Analyst
      │
      ▼
Rehoboam_AI Engine
      │
      ├── AI Analysis (Ollama LLM)
      │
      ▼
OSINT Data Collector
      │
      ▼
SearXNG Meta Search API
      │
      ▼
Open Web Sources
(News, Blogs, Forums, Public Data)
```
https://ollama.com/library/qwen2.5:3b
---

# Why SearXNG

SearXNG is used as the **OSINT search engine layer** because it:

* Aggregates results from multiple search engines
* Provides a powerful JSON API
* Can be self-hosted
* Supports automated data collection
* Protects user privacy

Official repository:

https://github.com/searxng/searxng

---

# Installing SearXNG

## Install Docker

```bash id="a0zv51"
sudo apt update
sudo apt install docker.io docker-compose -y
```

---

## Clone SearXNG

```bash id="p1q6ne"
git clone https://github.com/searxng/searxng.git
cd searxng
```

---

## Start SearXNG

```bash id="x1lqpl"
docker compose up -d
```

Access the instance:

```id="azq2ft"
http://localhost:8080
```

---

# Installing Ollama

Ollama is used to run **local large language models** for intelligence analysis.

## Install Ollama

Linux / Mac:

```bash id="7j9qak"
curl -fsSL https://ollama.com/install.sh | sh
```

Check installation:

```bash id="er2tf5"
ollama --version
```

---

# Download AI Models

Example models:

```bash id="9w8k3p"
ollama pull llama3
ollama pull mistral
ollama pull phi3
```

Run a model:

```bash id="s4t91g"
ollama run llama3
```

---

# Using Ollama with Python

Example AI analysis module:

```python id="48m8ok"
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def analyze_osint(text):

    payload = {
        "model": "llama3",
        "prompt": f"Analyze the following intelligence report and identify risks:\n{text}",
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    return response.json()["response"]


report = "Military tensions increasing near disputed border regions."

analysis = analyze_osint(report)

print(analysis)
```

---

# Using SearXNG for OSINT Search

Example query:

```id="u6m3ze"
http://localhost:8080/search?q=geopolitical+tension&format=json
```
<img width="1920" height="1032" alt="Screenshot 2026-03-19 160939" src="https://github.com/user-attachments/assets/96cdcd95-1584-4cd7-b671-c0b696d14f7f" />


Returned fields:

* title
* url
* content
* engine
* publishedDate

---

# OSINT Intelligence Pipeline

1. AI generates intelligence queries
2. SearXNG collects search results
3. Data extraction and filtering
4. AI analysis via Ollama models
5. Event classification
6. Risk scoring
7. Prediction generation

---

# Example Intelligence Queries

```id="q82td4"
cyber attack infrastructure
military escalation europe
political instability africa
energy supply disruption
economic sanctions impact
```

---
# User Interface

Rehoboam_AI includes a **custom graphical user interface built with Tkinter** for interacting with the OSINT intelligence system.

The UI allows analysts to:

* Enter intelligence search queries
* Trigger OSINT collection from SearXNG
* Run AI analysis using Ollama models
* View summarized intelligence reports
* Monitor predictions and risk assessments

Tkinter was chosen because it:

* Is lightweight and built into Python
* Works on Linux, Windows, and macOS
* Requires no additional web server
* Enables rapid UI development

---

# Tkinter Interface Features

The custom interface includes:

* 🔎 OSINT search panel
* 🧠 AI analysis button
* 📊 Intelligence output viewer
* 📜 Search result viewer
* ⚙️ Model selection (Ollama)

---

# Example Tkinter UI Structure

```python
import tkinter as tk
from tkinter import scrolledtext

def run_analysis():
    query = search_entry.get()
    output_box.insert(tk.END, f"Running OSINT analysis for: {query}\n")

root = tk.Tk()
root.title("Rehoboam_AI")

search_entry = tk.Entry(root, width=50)
search_entry.pack()

run_button = tk.Button(root, text="Analyze", command=run_analysis)
run_button.pack()

output_box = scrolledtext.ScrolledText(root, width=80, height=20)
output_box.pack()

root.mainloop()
```

---

# Running the UI

Start the Rehoboam_AI interface:

```bash
python main.py
```

The Tkinter dashboard will open and allow you to interact with the system.

---

# UI Workflow

```
User Input
   │
   ▼
Tkinter Interface
   │
   ├── Query OSINT (SearXNG)
   │
   ├── AI Analysis (Ollama)
   │
   ▼
Intelligence Results Display
```

<img width="1920" height="1032" alt="Screenshot 2026-03-19 160823" src="https://github.com/user-attachments/assets/6f266ca8-7a82-46c6-b98e-8c40e50cd763" />

---

# Future UI Improvements

Planned UI enhancements include:

* Interactive dashboards
* Risk visualization graphs
* Intelligence timeline view
* Dark mode interface
* Export intelligence reports

# Security Recommendations

* Deploy behind **NGINX reverse proxy**
* Implement **rate limiting**
* Validate external sources
* Monitor logs and API requests
* Run AI models locally for privacy

---

# Future Development

Planned improvements:

* Autonomous AI intelligence agents
* Event clustering and timeline analysis
* Geopolitical forecasting models
* Real-time alert system
* Geospatial intelligence mapping
* Multi-model AI analysis

---

# Contributing

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Submit a pull request

---



# 🐧 Running with Podman (Docker Alternative)

This project is fully compatible with **Podman**, a daemon-less container engine.

Podman can be used as a drop-in replacement for Docker on:

* Linux
* Windows (WSL2)
* macOS

---

## 🚀 Run SearXNG using Podman

```bash
podman run -d \
  --name searxng \
  -p 8080:8080 \
  docker.io/searxng/searxng
```

Open:

```
http://localhost:8080
```

---

## 🤖 Enable Ollama Integration (Podman)

Copy default configuration:

```bash
podman cp searxng:/etc/searxng .
```

Edit:

```
searxng/settings.yml
```

Add AI provider:

```yaml
ai:
  enabled: true
  provider: ollama
  ollama:
    url: http://host.containers.internal:11434
    model: llama3
```

Restart container:

```bash
podman restart searxng
```

---
Overview

SearXNG is an open-source, privacy-respecting meta search engine that aggregates results from multiple search providers without tracking users. It is a community-driven fork of the original Searx project, designed for better performance, maintainability, and extensibility.

Key Features

🔐 Privacy-first search (no tracking, no profiling)

🌐 Aggregates results from multiple search engines

⚙ Highly configurable and extensible

🚀 Self-hostable (Docker / Podman / native)

🤖 Supports AI integration (e.g., Ollama, OpenAI)

🧩 Plugin-based architecture

📡 Supports Tor / proxy routing

How It Works

User query → SearXNG → Multiple search engines → Aggregated results → Returned to user

SearXNG acts as an intermediary, preventing search engines from identifying the user directly.

Architecture Components

Search engine connectors (Google, DuckDuckGo, Bing, etc.)

Result aggregator & ranking system

Web UI frontend

Configurable settings engine

Optional AI answer provider

Use Cases

Privacy-focused personal search engine

AI-enhanced search (local LLM)

Research aggregation tool

Enterprise internal search

Tor-based anonymous browsing

Advantages

No ads or tracking

Full control over search configuration

Open-source and community maintained

Can be deployed locally or publicly

Extensible with AI capabilities

Typical Deployment Options

Docker / Podman containers

Reverse proxy (Nginx / Caddy)

Cloud VPS hosting

Local AI integration via Ollama

## ⚠️ Podman on Windows (WSL Backend)

When using Podman with WSL:

* Access via `localhost`, not VM IP
* Avoid mounting empty config directories
* Use `host.containers.internal` to reach Ollama
* Ensure Podman machine is running

---

## 🧰 Persistent Setup (Optional)

```bash
podman rm -f searxng

podman run -d \
  --name searxng \
  -p 8080:8080 \
  -v $(pwd)/searxng:/etc/searxng \
  docker.io/searxng/searxng
```

---

## ✅ Compatibility

Podman CLI is compatible with Docker CLI.

Most Docker commands in this README can be replaced:

```
docker → podman
docker-compose → podman-compose
```

---

## 📌 Verified Environment

* Podman 4+
* WSL2 (Windows)
* Ubuntu / Arch Linux
* Ollama local LLM
* SearXNG latest container

---

## 🔒 Benefits of Podman

* Rootless containers
* No daemon
* Better security model
* Systemd integration
* OCI compliant

---

# License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

You are free to use, modify, and distribute this software under the terms of the GPL-3.0 license.
