import sys
from pathlib import Path

# Add project root to sys.path so modules can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from flask import Flask, request, jsonify, render_template_string
from modules.memory_management.allocator import MemoryAllocator
from modules.memory_management.paging import PageReplacementManager
from modules.memory_management.comparison import MemoryComparisonEngine, PagingComparisonEngine

app = Flask(__name__)

HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Memory & Paging Optimization Subsystem</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 30px; background: #0f172a; color: #f8fafc; }
        h1 { color: #38bdf8; margin-bottom: 5px; }
        .subtitle { color: #94a3b8; margin-bottom: 25px; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 25px; }
        .card { background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 24px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2); }
        h2 { color: #f1f5f9; margin-top: 0; font-size: 1.25rem; border-bottom: 1px solid #334155; padding-bottom: 10px; }
        label { display: block; font-size: 13px; font-weight: 600; color: #cbd5e1; margin-top: 14px; margin-bottom: 6px; }
        input, select, textarea { width: 100%; box-sizing: border-box; background: #0f172a; border: 1px solid #475569; color: #fff; padding: 10px; border-radius: 4px; font-size: 13px; }
        input:focus, select:focus, textarea:focus { outline: none; border-color: #38bdf8; }
        button { margin-top: 18px; width: 100%; background: #0284c7; color: white; border: none; padding: 12px; border-radius: 4px; font-weight: 600; cursor: pointer; transition: background 0.2s; font-size: 14px; }
        button:hover { background: #0369a1; }
        pre { background: #0f172a; border: 1px solid #334155; padding: 14px; border-radius: 6px; overflow-x: auto; color: #a5f3fc; font-size: 12px; max-height: 480px; }
    </style>
</head>
<body>
    <h1>Memory Management & Virtual Memory Subsystem</h1>
    <div class="subtitle">Contiguous Allocation Strategies & Custom $O(1)$ LRU Page Replacement Engine</div>

    <div class="grid">
        <!-- 1. Contiguous Memory Allocation Card -->
        <div class="card">
            <h2>Contiguous Allocation Simulator</h2>
            <label>Partition Sizes (comma-separated)</label>
            <input id="partitions" value="100, 500, 200, 300, 600">

            <label>Requests (PID:Size, comma or newline separated)</label>
            <textarea id="requests" rows="4">P1:212, P2:417, P3:112, P4:426</textarea>

            <label>Allocation Policy</label>
            <select id="allocAlgo">
                <option value="First Fit">First Fit</option>
                <option value="Best Fit">Best Fit</option>
                <option value="Worst Fit">Worst Fit</option>
                <option value="Next Fit">Next Fit</option>
                <option value="Compare All">Compare All Strategies</option>
            </select>

            <button type="button" id="btnAlloc">Simulate Allocation</button>
            <div id="allocOutput" style="margin-top: 15px;"></div>
        </div>

        <!-- 2. Virtual Memory Page Replacement Card -->
        <div class="card">
            <h2>Page Replacement Simulator</h2>
            <label>Frame Capacity</label>
            <input id="capacity" type="number" value="3">

            <label>Reference String (comma-separated)</label>
            <input id="refString" value="7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2">

            <label>Replacement Algorithm</label>
            <select id="pagingAlgo">
                <option value="FIFO">FIFO</option>
                <option value="LRU">LRU (Custom HashTable + DLL)</option>
                <option value="Compare Both">Compare Both</option>
            </select>

            <button type="button" id="btnPaging">Simulate Paging</button>
            <div id="pagingOutput" style="margin-top: 15px;"></div>
        </div>
    </div>

    <script>
        // --- CONTIGUOUS ALLOCATION HANDLER ---
        document.getElementById('btnAlloc').addEventListener('click', async () => {
            const out = document.getElementById('allocOutput');
            out.innerHTML = '<span style="color:#94a3b8">Allocating memory...</span>';
            try {
                const partitions = document.getElementById('partitions').value
                    .split(',')
                    .map(x => parseInt(x.trim()))
                    .filter(x => !isNaN(x));

                const rawText = document.getElementById('requests').value;
                const items = rawText.split(/[\n,]+/).map(x => x.trim()).filter(Boolean);
                const requests = [];

                for (const item of items) {
                    if (item.includes(':')) {
                        const parts = item.split(':');
                        const pid = parts[0].trim();
                        const sz = parseInt(parts[1].trim());
                        if (pid && !isNaN(sz)) requests.push({ process_id: pid, size: sz });
                    }
                }

                const algo = document.getElementById('allocAlgo').value;
                const response = await fetch('/api/allocate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ partitions, requests, algorithm: algo })
                });
                const data = await response.json();
                out.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            } catch (err) {
                out.innerHTML = '<span style="color:#f87171">Error: ' + err.message + '</span>';
            }
        });

        // --- PAGE REPLACEMENT HANDLER ---
        document.getElementById('btnPaging').addEventListener('click', async () => {
            const out = document.getElementById('pagingOutput');
            out.innerHTML = '<span style="color:#94a3b8">Simulating Paging...</span>';
            try {
                const capacity = parseInt(document.getElementById('capacity').value);
                const refString = document.getElementById('refString').value
                    .split(',')
                    .map(x => parseInt(x.trim()))
                    .filter(x => !isNaN(x));

                const algo = document.getElementById('pagingAlgo').value;
                const response = await fetch('/api/paging', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ capacity, reference_string: refString, algorithm: algo })
                });
                const data = await response.json();
                out.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
            } catch (err) {
                out.innerHTML = '<span style="color:#f87171">Error: ' + err.message + '</span>';
            }
        });
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

# --- CONTIGUOUS ALLOCATION ROUTE ---
@app.route("/api/allocate", methods=["POST"])
def api_allocate():
    data = request.get_json() or {}
    partitions = data.get("partitions", [100, 500, 200, 300, 600])
    requests = data.get("requests", [])
    algo = data.get("algorithm", "First Fit")

    if algo == "Compare All":
        return jsonify(MemoryComparisonEngine.compare_allocators(partitions, requests))

    allocator = MemoryAllocator(partitions)
    return jsonify(allocator.run_simulation(algo, requests))

# --- PAGE REPLACEMENT ROUTE ---
@app.route("/api/paging", methods=["POST"])
def api_paging():
    data = request.get_json() or {}
    capacity = int(data.get("capacity", 3))
    ref_string = data.get("reference_string", [])
    algo = data.get("algorithm", "FIFO")

    if algo == "Compare Both":
        return jsonify(PagingComparisonEngine.compare_paging(capacity, ref_string))

    mgr = PageReplacementManager(capacity)
    result = mgr.run_fifo(ref_string) if algo == "FIFO" else mgr.run_lru(ref_string)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)