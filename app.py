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


# -----------------------------
# Consultation Finalized
# -----------------------------
@app.get("/api/finalized")
def get_finalized():
    res = supabase.table(TABLE).select("ConsultationFinalized").eq("id", ROW_ID).single().execute()
    val = bool(res.data.get("ConsultationFinalized")) if res.data else False
    return jsonify({"finalized": val}), 200


@app.post("/api/finalized")
def set_finalized():
    data = request.get_json(silent=True) or {}
    val = bool(data.get("finalized", False))
    supabase.table(TABLE).update({"ConsultationFinalized": val}).eq("id", ROW_ID).execute()
    return jsonify({"ok": True, "finalized": val}), 200


# -----------------------------
# Architect Meeting Done
# -----------------------------
@app.get("/api/architect-meeting")
def get_architect_meeting():
    res = supabase.table(TABLE).select("ArchitectMeetingDone").eq("id", ROW_ID).single().execute()
    val = bool(res.data.get("ArchitectMeetingDone")) if res.data else False
    return jsonify({"architect_meeting_done": val}), 200


@app.post("/api/architect-meeting")
def set_architect_meeting():
    data = request.get_json(silent=True) or {}
    val = bool(data.get("architect_meeting_done", False))
    supabase.table(TABLE).update({"ArchitectMeetingDone": val}).eq("id", ROW_ID).execute()
    return jsonify({"ok": True, "architect_meeting_done": val}), 200


# -----------------------------
# Meeting Done (3-state: True / False / NULL)
# -----------------------------
@app.get("/api/meeting-done")
def get_meeting_done():
    res = supabase.table(TABLE).select("MeetingDone").eq("id", ROW_ID).single().execute()
    meeting_val = res.data.get("MeetingDone") if res.data else None
    return jsonify({"meeting_done": meeting_val}), 200


@app.post("/api/meeting-done")
def set_meeting_done():
    data = request.get_json(silent=True) or {}
    # Allow True, False, or None
    meeting_val = data.get("meeting_done", None)
    supabase.table(TABLE).update({"MeetingDone": meeting_val}).eq("id", ROW_ID).execute()
    return jsonify({"ok": True, "meeting_done": meeting_val}), 200


# -----------------------------
# Minimal Admin HTML Interface
# -----------------------------
ADMIN_HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Admin Controls</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style>
      body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial;
           max-width:520px;margin:40px auto;padding:0 16px;}
      .row{display:flex;align-items:center;gap:10px;margin-bottom:20px;}
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

    <h2>Architect Meeting Done</h2>
    <div class="row">
      <input id="chk_arch" type="checkbox" />
      <span id="lbl_arch" class="muted">Loading…</span>
      <button id="refresh_arch" class="btn">Refresh</button>
    </div>

    <h2>Meeting Done</h2>
    <div class="row">
      <select id="select_meet">
        <option value="null">Not Set (NULL)</option>
        <option value="true">True</option>
        <option value="false">False</option>
      </select>
      <span id="lbl_meet" class="muted">Loading…</span>
      <button id="refresh_meet" class="btn">Refresh</button>
    </div>

    <script>
      // ---- Consultation Finalized ----
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

      // ---- Architect Meeting Done ----
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

      // ---- Meeting Done (3-state) ----
      async function loadMeeting() {
        const r = await fetch('/api/meeting-done');
        const j = await r.json();
        const sel = document.getElementById('select_meet');
        const lbl = document.getElementById('lbl_meet');
        if (j.meeting_done === true) {
          sel.value = 'true';
          lbl.textContent = 'True';
        } else if (j.meeting_done === false) {
          sel.value = 'false';
          lbl.textContent = 'False';
        } else {
          sel.value = 'null';
          lbl.textContent = 'Not Set';
        }
      }

      async function saveMeeting() {
        const sel = document.getElementById('select_meet');
        const lbl = document.getElementById('lbl_meet');
        let val = null;
        if (sel.value === 'true') val = true;
        else if (sel.value === 'false') val = false;

        await fetch('/api/meeting-done', {
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify({ meeting_done: val })
        });

        lbl.textContent = sel.value === 'null' ? 'Not Set' : sel.value.charAt(0).toUpperCase() + sel.value.slice(1);
      }

      // ---- Event bindings ----
      document.getElementById('chk').addEventListener('change', save);
      document.getElementById('refresh').addEventListener('click', load);
      document.getElementById('chk_arch').addEventListener('change', saveArchitect);
      document.getElementById('refresh_arch').addEventListener('click', loadArchitect);
      document.getElementById('select_meet').addEventListener('change', saveMeeting);
      document.getElementById('refresh_meet').addEventListener('click', loadMeeting);

      // ---- Initial load ----
      load();
      loadArchitect();
      loadMeeting();
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
