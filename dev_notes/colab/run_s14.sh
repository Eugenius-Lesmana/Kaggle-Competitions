#!/bin/bash
# S14 one-shot redeploy: singlefile battery on fresh Colab VM.
# Usage: bash run_s14.sh <host> <port> [gpt|gemma]
set -e
HOST="${1:-8.tcp.ngrok.io}"
PORT="${2:?port required}"
WHICH="${3:-gpt}"
KEY=~/.ssh/opencode-colab_key
SSH="ssh -i $KEY -p $PORT -o StrictHostKeyChecking=no -o ConnectTimeout=15 root@$HOST"
SCP="scp -q -i $KEY -P $PORT -o StrictHostKeyChecking=no"

echo "== connectivity"
$SSH 'echo VM_OK'

echo "== push files"
$SSH 'mkdir -p /content/proj'
$SCP dev_notes/colab/bootstrap.sh dev_notes/colab/probe_s14.py /tmp/opencode/proj.tgz "root@$HOST:/content/"

echo "== bootstrap (pips + model downloads in background)"
$SSH 'bash /content/bootstrap.sh'

if [ "$WHICH" = "gemma" ]; then
  echo "== starting gemma Q3_K_XL download (Q4_K_M OOMs on T4)"
  $SSH 'rm -f /content/models/gemma-4-26B-A4B-it-UD-Q4_K_M.gguf; cat > /content/dl_q3.py <<EOF
from huggingface_hub import hf_hub_download
print("DONE", hf_hub_download(repo_id="unsloth/gemma-4-26B-A4B-it-GGUF", filename="gemma-4-26B-A4B-it-UD-Q3_K_XL.gguf", local_dir="/content/models"), flush=True)
EOF
nohup python3 /content/dl_q3.py > /content/dl_q3.log 2>&1 < /dev/null & echo DL_STARTED'
  echo "== waiting for gemma Q3_K_XL GGUF"
  $SSH 'for i in $(seq 1 120); do grep -q DONE /content/dl_q3.log 2>/dev/null && break; sleep 10; done; grep DONE /content/dl_q3.log | head -1; ls -la /content/models/*.gguf 2>/dev/null'
else
  echo "== waiting for gpt-oss GGUF"
  $SSH 'for i in $(seq 1 120); do grep -q "gpt-oss-20b-Q4_K_M.gguf" /content/dl.log && break; sleep 10; done; grep DONE /content/dl.log | head -1'
fi

echo "== extract project + fixture symlink"
$SSH 'cd /content && tar xzf proj.tgz && mkdir -p /content/proj && ln -sfn /content/sdk /content/proj/sdk && echo EXTRACT_OK'

echo "== launch battery ($WHICH)"
$SSH "export LD_LIBRARY_PATH=/usr/lib64-nvidia:/usr/local/cuda-12.8/compat; cd /content && nohup python3 probe_s14.py $WHICH > /content/battery.log 2>&1 < /dev/null & sleep 2; echo BATTERY_LAUNCHED"
