#!/bin/bash
# Gemma-only Colab bootstrap (S12 prerequisite battery, 2026-08-25).
# Downloads ONLY the gemma GGUF (~5 GB) — the battery below never touches
# gpt-oss, so skipping it halves time-to-first-measurement on a fragile VM.
set -e
export DEBIAN_FRONTEND=noninteractive
mkdir -p /run/sshd
pip install -q huggingface_hub grpcio-tools 2>&1 | tail -1 || true
pip install -q llama-cpp-python \
  --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu124 2>&1 | tail -1 || true
mkdir -p /content/models /content/proj
cat > /content/setup_dl.py <<'PYEOF'
from huggingface_hub import hf_hub_download
print("DONE", hf_hub_download(
    repo_id="unsloth/gemma-4-26B-A4B-it-GGUF",
    filename="gemma-4-26B-A4B-it-UD-Q4_K_M.gguf",
    local_dir="/content/models"), flush=True)
print("ALL_MODELS_DONE", flush=True)
PYEOF
nohup python3 /content/setup_dl.py > /content/dl.log 2>&1 &
echo "bootstrap ok, gemma download pid $!"
