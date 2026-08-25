#!/bin/bash
# Round-2 one-shot: everything after a fresh Colab VM (post-wipe).
# Usage: bash run_round2.sh <host> <port>
set -e
HOST="${1:-4.tcp.ngrok.io}"
PORT="${2:-11948}"
KEY=~/.ssh/opencode-colab_key
SSH="ssh -i $KEY -p $PORT -o StrictHostKeyChecking=no -o ConnectTimeout=15 root@$HOST"
SCP="scp -q -i $KEY -P $PORT -o StrictHostKeyChecking=no"

echo "== connectivity"
$SSH 'echo VM_OK'

echo "== push files"
$SSH 'mkdir -p /content/proj'
$SCP dev_notes/colab/bootstrap_q3.sh dev_notes/colab/probe_gemma.py /tmp/opencode/proj.tgz "root@$HOST:/content/"

echo "== bootstrap (pips + Q3_K_XL download in background)"
$SSH 'bash /content/bootstrap_q3.sh'

echo "== waiting for model download"
$SSH 'for i in $(seq 1 60); do grep -q ALL_MODELS_DONE /content/dl.log && break; sleep 20; done; tail -2 /content/dl.log'

echo "== extract project + fixture symlink"
$SSH 'cd /content && tar xzf proj.tgz && mkdir -p /content/proj && ln -sfn /content/sdk /content/proj/sdk && echo EXTRACT_OK'

echo "== launch battery"
$SSH 'source /etc/profile.d/nvidia.sh 2>/dev/null || export LD_LIBRARY_PATH=/usr/lib64-nvidia:/usr/local/cuda-12.8/compat; cd /content && nohup python3 probe_gemma.py > /content/battery.log 2>&1 < /dev/null & sleep 1; echo BATTERY_LAUNCHED'
