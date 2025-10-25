import os
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()  # loads .env in dev

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_KEY"]
TABLE = "app_settings"
ROW_ID = 1

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

app = Flask(__name__)
# You can restrict origins later, e.g., CORS(app, resources={r"/api/*": {"origins": ["http://localhost:19006"]}})
CORS(app)

@app.get("/api/finalized")
def get_finalized():
    res = supabase.table(TABLE).select("ConsultationFinalized").eq("id", ROW_ID).single().execute()
    val = bool(res.data["ConsultationFinalized"])
    return jsonify({"finalized": val}), 200

@app.post("/api/finalized")
def set_finalized():
    data = request.get_json(silent=True) or {}
    val = bool(data.get("finalized", False))
    supabase.table(TABLE).update({"ConsultationFinalized": val}).eq("id", ROW_ID).execute()
    return jsonify({"ok": True, "finalized": val}), 200

@app.get("/api/architect-meeting")
def get_architect_meeting():
    res = supabase.table(TABLE).select("ArchitectMeetingDone").eq("id", ROW_ID).single().execute()
    val = bool(res.data["ArchitectMeetingDone"])
    return jsonify({"architect_meeting_done": val}), 200

@app.post("/api/architect-meeting")
def set_architect_meeting():
    data = request.get_json(silent=True) or {}
    val = bool(data.get("architect_meeting_done", False))
    supabase.table(TABLE).update({"ArchitectMeetingDone": val}).eq("id", ROW_ID).execute()
    return jsonify({"ok": True, "architect_meeting_done": val}), 200


# Minimal admin HTML
ADMIN_HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Toggle Finalized</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style>
      body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial;
           max-width:520px;margin:40px auto;padding:0 16px;}
      .row{display:flex;align-items:center;gap:10px}
      .btn{padding:8px 12px;border:1px solid #ddd;border-radius:8px;cursor:pointer}
      .muted{color:#666}
    </style>
  </head>
  <body>
    <h2>Consultation Finalized</h2>
    <div class="row">
      <input id="chk" type="checkbox" />
      <span id="lbl" class="muted">Loading…</span>
      <button id="refresh" class="btn">Refresh</button>
    </div>
    <p class="muted">This page updates the single row in <code>app_settings</code>.</p>

    <script>
      async function load() {
        const r = await fetch('/api/finalized');
        const j = await r.json();
        const chk = document.getElementById('chk');
        const lbl = document.getElementById('lbl');
        chk.checked = !!j.finalized;
        lbl.textContent = j.finalized ? 'True' : 'False';
      }
      async function save() {
        const chk = document.getElementById('chk');
        const lbl = document.getElementById('lbl');
        await fetch('/api/finalized', {
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify({ finalized: chk.checked })
        });
        lbl.textContent = chk.checked ? 'True' : 'False';
      }
      document.getElementById('chk').addEventListener('change', save);
      document.getElementById('refresh').addEventListener('click', load);
      load();
    </script>

    <h2>Architect Meeting Done</h2>
<div class="row">
  <input id="chk_arch" type="checkbox" />
  <span id="lbl_arch" class="muted">Loading…</span>
  <button id="refresh_arch" class="btn">Refresh</button>
</div>

<script>
  async function loadArchitect() {
    const r = await fetch('/api/architect-meeting');
    const j = await r.json();
    const chk = document.getElementById('chk_arch');
    const lbl = document.getElementById('lbl_arch');
    chk.checked = !!j.architect_meeting_done;
    lbl.textContent = j.architect_meeting_done ? 'True' : 'False';
  }
  async function saveArchitect() {
    const chk = document.getElementById('chk_arch');
    const lbl = document.getElementById('lbl_arch');
    await fetch('/api/architect-meeting', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ architect_meeting_done: chk.checked })
    });
    lbl.textContent = chk.checked ? 'True' : 'False';
  }
  document.getElementById('chk_arch').addEventListener('change', saveArchitect);
  document.getElementById('refresh_arch').addEventListener('click', loadArchitect);
  loadArchitect();
</script>


  </body>
</html>
"""

@app.get("/admin")
def admin():
    return render_template_string(ADMIN_HTML)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
