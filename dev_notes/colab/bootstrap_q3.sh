#!/bin/bash
# Gemma-only Colab bootstrap, round 2 (2026-08-25).
# Q3_K_XL (12.9 GB) instead of Q4_K_M (16.9 GB):
#   - downloads ~25% faster on the fragile VM,
#   - fits FULLY in T4 15GB VRAM -> full offload -> CPU never runs ggml
#     tensor ops -> dodges the libggml-cpu invalid-opcode crash that killed
#     round 1 (partial-offload CPU kernels are broken on this image/CPU).
set -e
export DEBIAN_FRONTEND=noninteractive
mkdir -p /run/sshd
pip install -q huggingface_hub grpcio-tools 2>&1 | tail -1 || true
mkdir -p /content/models /content/proj
cat > /content/setup_dl.py <<'PYEOF'
from huggingface_hub import hf_hub_download
print("DONE", hf_hub_download(
    repo_id="unsloth/gemma-4-26B-A4B-it-GGUF",
    filename="gemma-4-26B-A4B-it-UD-Q3_K_XL.gguf",
    local_dir="/content/models"), flush=True)
print("ALL_MODELS_DONE", flush=True)
PYEOF
nohup python3 /content/setup_dl.py > /content/dl.log 2>&1 < /dev/null &
DL_PID=$!
echo "download started (pid $DL_PID); installing llama-cpp-python while it runs"
pip install -q llama-cpp-python \
  --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu124 2>&1 | tail -1 || true
ldconfig /usr/lib64-nvidia /usr/local/cuda-12.8/compat 2>/dev/null || true
echo "LD_LIBRARY_PATH fix:"; echo 'export LD_LIBRARY_PATH=/usr/lib64-nvidia:/usr/local/cuda-12.8/compat' > /etc/profile.d/nvidia.sh
wait $DL_PID || true
tail -2 /content/dl.log
echo "bootstrap ok"
