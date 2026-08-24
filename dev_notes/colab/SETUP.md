# Google Colab real-model testing — setup & operations guide

**Why this exists:** hosted reruns give one noisy LB number per ~14 h and no
per-family telemetry. A Colab GPU VM running the SDK's own model servers
(`unsloth/gpt-oss-20b-Q4_K_M`, `unsloth/gemma-4-26B-A4B-it-UD-Q4_K_M`) with
`SandboxEnv(seed=123)` + `OptimalGuardrail` reproduces hosted replay
semantics (greedy, n_ctx 8192, max_new_tokens 1024) and measures every
family's true raw/posts/latency in minutes. This is how S11_TOPTIER's pool
was chosen; see `colab_battery_2026-08-24.md` for the first battery's output.

**Status: proven workflow. Used 2026-08-24. Re-run whenever a new family/
shape/pool question appears that LB draws can't resolve cheaply.**

## One-time local prep (already done, redo if /tmp wiped)

```bash
ssh-keygen -t ed25519 -f /tmp/opencode/colab_key -N "" -C opencode-colab
```
Private key stays local; only the pubkey goes into Colab.

## User-side steps (they do these in the browser)

1. Colab: `Runtime → Change runtime type → T4 GPU` (free tier fine).
2. Cell 1 — sshd + authorize our key:
   ```python
   %%bash
   apt-get install -y openssh-server > /dev/null 2>&1
   mkdir -p /root/.ssh /run/sshd
   echo "ssh-ed25519 AAAA...opencode-colab" >> /root/.ssh/authorized_keys
   chmod 700 /root/.ssh && chmod 600 /root/.ssh/authorized_keys
   ```
3. Cell 2 — ngrok tunnel (user needs a free authtoken):
   ```python
   !pip -q install pyngrok
   from pyngrok import ngrok
   ngrok.set_auth_token("<USER_TOKEN>")
   print("CONNECT:", ngrok.connect(22, "tcp").public_url)
   ```
4. User pastes back `tcp://0.tcp.ngrok.io:NNNNN` → we connect
   `ssh -i /tmp/opencode/colab_key -p NNNNN root@0.tcp.ngrok.io`.

## VM gotchas (all hit 2026-08-24 — don't relearn them)

- **Colab's sshd_config listens on 127.0.0.1:2222**, not :22. Fix:
  ```bash
  sed -i -E '/^\s*ListenAddress\s+/d' /etc/ssh/sshd_config
  sed -i -E 's/^\s*(Port)\s+.*/Port 22/' /etc/ssh/sshd_config
  /usr/sbin/sshd -E /var/log/sshd.log   # run directly; `service` wrapper lies
  ```
- **VMs die hard** (~every 30–90 min in practice; /content wiped, tunnels
  drop). Treat everything on the VM as ephemeral:
  - `nohup` every long job; write results to `/content/results.jsonl`.
  - **scp-pull results to the local machine every few minutes** — the only
    durable copy is the one off-VM.
  - Keep `/tmp/opencode/bootstrap.sh` + `probe_battery.py` locally (mirrored
    in `dev_notes/colab/`) so a fresh VM is one paste + one tar.
- **Python is 3.13** but the SDK bundles a cp312 grpcio wheel whose auto-
  install fails. Pre-install first: `pip install grpcio-tools`.
- **llama-cpp-python**: no nvcc on the image; use prebuilt CUDA wheels:
  `pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu124`
  then always export `LD_LIBRARY_PATH=/usr/lib64-nvidia` (driver libs live
  there, not in ldconfig).
- **gemma-4-26B-A4B barely fits a T4**: weights ≈14 GB vs 15 GB VRAM ⇒ full
  offload OOMs at n_ctx 8192. Max working config measured: `n_gpu_layers=16`
  (hybrid CPU → slow). gpt-oss-20b Q4_K_M fits fully (`n_gpu_layers=-1`) and
  is fast (~10 s per 8-hop bare candidate).
- ngrok tunnels die with the VM process; user re-runs cell 2 to get a new
  port. Old port keeps "existing" in their list — use the NEW one.

## VM bootstrap (paste as /content/bootstrap.sh, then `bash` it)

See `dev_notes/colab/bootstrap.sh` — installs wheels, starts background
download of both GGUFs to `/content/models`.

## Probe battery

`dev_notes/colab/probe_battery.py` — drives `GgufModelServer`s through the
SDK sandbox exactly like hosted replay, walks the FAMILY_BUILDERS table,
appends JSONL per candidate. Usage on VM:

```bash
cd /content/proj && LD_LIBRARY_PATH=/usr/lib64-nvidia \
  nohup python3 probe_battery.py [smoke|gpt|gemma] > log 2>&1 &
```

Edit `FAMILIES`/`INDICES` at the top per question. Gemma runs need the
`ngl_try = [16]` patch (see gotchas) and patience (hybrid offload is slow).

## What Colab testing is NOT

- It does not remove LB replay noise for final scoring — endgame is still
  best-of re-ships of the frozen chassis.
- Absolute latencies differ from hosted (T4 vs their GPUs); RELATIVE family
  rankings and compliance counts transfer because decoding is deterministic
  given identical prompts/weights.
