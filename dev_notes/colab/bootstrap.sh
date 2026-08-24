#!/bin/bash
# Colab VM bootstrap — run as root right after first SSH connection.
# Installs wheels, starts background GGUF download to /content/models.
set -e
export DEBIAN_FRONTEND=noninteractive
mkdir -p /run/sshd
pip install -q huggingface_hub grpcio-tools \
  --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu124 \
  2>&1 | tail -1 || true
pip install -q llama-cpp-python \
  --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu124 2>&1 | tail -1 || true
mkdir -p /content/models /content/proj
cat > /content/setup_dl.py <<'PYEOF'
from huggingface_hub import hf_hub_download
for repo, fn in [("unsloth/gpt-oss-20b-GGUF","gpt-oss-20b-Q4_K_M.gguf"),
                 ("unsloth/gemma-4-26B-A4B-it-GGUF","gemma-4-26B-A4B-it-UD-Q4_K_M.gguf")]:
    print("DONE", hf_hub_download(repo_id=repo, filename=fn, local_dir="/content/models"), flush=True)
print("ALL_MODELS_DONE", flush=True)
PYEOF
nohup python3 /content/setup_dl.py > /content/dl.log 2>&1 &
echo "bootstrap ok, download pid $!"
