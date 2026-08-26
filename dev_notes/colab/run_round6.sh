#!/bin/bash
# Round-6 one-shot redeploy: instrumented gpt_oss battery on fresh Colab VM.
# Usage: bash run_round6.sh <host> <port>
set -e
HOST="${1:-4.tcp.ngrok.io}"
PORT="${2:?port required}"
KEY=~/.ssh/opencode-colab_key
SSH="ssh -i $KEY -p $PORT -o StrictHostKeyChecking=no -o ConnectTimeout=15 root@$HOST"
SCP="scp -q -i $KEY -P $PORT -o StrictHostKeyChecking=no"

echo "== connectivity"
$SSH 'echo VM_OK'

echo "== push files"
$SSH 'mkdir -p /content/proj'
$SCP dev_notes/colab/bootstrap.sh dev_notes/colab/probe_round6.py /tmp/opencode/proj.tgz "root@$HOST:/content/"

echo "== bootstrap (pips + model downloads in background)"
$SSH 'bash /content/bootstrap.sh'

echo "== waiting for gpt-oss GGUF"
$SSH 'for i in $(seq 1 90); do grep -q "gpt-oss-20b-Q4_K_M.gguf" /content/dl.log && break; sleep 10; done; grep DONE /content/dl.log | head -1'

echo "== extract project + fixture symlink"
$SSH 'cd /content && tar xzf proj.tgz && mkdir -p /content/proj && ln -sfn /content/sdk /content/proj/sdk && echo EXTRACT_OK'

echo "== launch battery"
$SSH 'export LD_LIBRARY_PATH=/usr/lib64-nvidia:/usr/local/cuda-12.8/compat; cd /content && nohup python3 probe_round6.py > /content/battery.log 2>&1 < /dev/null & sleep 2; echo BATTERY_LAUNCHED'
