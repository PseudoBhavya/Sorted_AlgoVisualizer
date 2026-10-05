"""
Script to build the unified AlgoVision / AlgoLens exact frontend.
Extracts the exact components from Stitch and connects them with a reactive JS engine.
"""

import os
import re
import json

STITCH_DIR = "/Users/apple/.gemini/antigravity-ide/brain/9531af3c-7367-4d77-91d7-2875cf941f52/scratch/stitch_reference/stitch_algovision_algorithm_visualizer_workspace"

with open(os.path.join(STITCH_DIR, "algovision_interactive_algorithm_execution_workspace", "code.html")) as f:
    h_vis = f.read()

with open(os.path.join(STITCH_DIR, "algovision_algorithm_catalog_selection", "code.html")) as f:
    h_cat = f.read()

with open(os.path.join(STITCH_DIR, "algovision_multi_algorithm_comparison_arena", "code.html")) as f:
    h_comp = f.read()

# Extract prefix (head, header, aside, opening pl-64 container)
prefix = h_vis.split('<main')[0]

# Extract main bodies
main_vis = re.search(r'<main[^>]*>(.*?)</main>', h_vis, re.DOTALL).group(1)
main_cat = re.search(r'<main[^>]*>(.*?)</main>', h_cat, re.DOTALL).group(1)
main_comp = re.search(r'<main[^>]*>(.*?)</main>', h_comp, re.DOTALL).group(1)

# Load precomputed trace for instant zero-latency loading
with open('/Users/apple/BCA/Python Mega Project/algolens/static/default_trace.json') as f:
    default_traces_json = f.read()

# JavaScript Engine implementing Play/Pause, Step, Scrubbing, Speed, and Tab navigation
js_engine = f"""
<script>
// AlgoLens Reactive Simulation & Navigation Engine
const DEFAULT_TRACES = {default_traces_json};

let currentAlgorithm = "Quick Sort (Hoare Scheme)";
let currentScheme = "hoare";
let currentTrace = DEFAULT_TRACES.quick_sort;
let currentStepIdx = 16; // Start at step 17 (the swap step shown in Stitch screenshot 3!)
let isPlaying = false;
let playTimer = null;
let clockSpeedMs = 400; // 1.0x normal
let currentTab = "visualize";

// DOM Elements
const tabPages = {{
  visualize: document.getElementById("page-visualize"),
  algorithms: document.getElementById("page-algorithms"),
  compare: document.getElementById("page-compare"),
  history: document.getElementById("page-history"),
  datasets: document.getElementById("page-datasets"),
  about: document.getElementById("page-about")
}};

function switchTab(tabName) {{
  if (!tabPages[tabName]) return;
  currentTab = tabName;

  // Toggle pages
  Object.keys(tabPages).forEach(key => {{
    if (key === tabName) {{
      tabPages[key].classList.remove("hidden");
    }} else {{
      tabPages[key].classList.add("hidden");
    }}
  }});

  // Update header nav active styles
  document.querySelectorAll("[data-nav-tab]").forEach(el => {{
    const t = el.getAttribute("data-nav-tab");
    if (t === tabName) {{
      el.className = "px-space-md py-1.5 transition-colors bg-primary-container text-on-primary-container font-medium rounded-lg";
    }} else {{
      el.className = "px-space-md py-1.5 text-on-surface-variant hover:text-on-surface font-label-md text-label-md transition-colors";
    }}
  }});

  // Update sidebar nav active styles
  document.querySelectorAll("[data-side-tab]").forEach(el => {{
    const t = el.getAttribute("data-side-tab");
    if (t === tabName) {{
      el.className = "flex items-center px-space-md py-2 transition-colors bg-primary-container text-on-primary-container font-medium rounded-lg";
    }} else {{
      el.className = "flex items-center px-space-md py-2 rounded-lg font-body-sm text-body-sm text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface transition-colors";
    }}
  }});

  // Scroll to top
  window.scrollTo(0, 0);
}}

// Attach tab listeners
document.querySelectorAll("[data-nav-tab], [data-side-tab]").forEach(el => {{
  el.addEventListener("click", (e) => {{
    e.preventDefault();
    const tab = el.getAttribute("data-nav-tab") || el.getAttribute("data-side-tab");
    switchTab(tab);
  }});
}});

// -------------------------------------------------------------
// Interactive Visualizer Engine
// -------------------------------------------------------------
function renderStep(idx) {{
  if (!currentTrace || !currentTrace.steps || currentTrace.steps.length === 0) return;
  
  idx = Math.max(0, Math.min(idx, currentTrace.steps.length - 1));
  currentStepIdx = idx;
  const step = currentTrace.steps[idx];
  const total = currentTrace.steps.length;
  const arr = step.array_state;
  const n = arr.length;
  const maxVal = Math.max(...arr.map(Number), 1);

  // 1. Update Timeline & Step Counter
  const stepNum = step.step_number || (idx + 1);
  const pct = Math.round((idx / Math.max(1, total - 1)) * 100);
  const badgeEl = document.getElementById("step-counter-badge");
  if (badgeEl) badgeEl.innerText = `Step ${{stepNum}} / ${{total}}`;
  const pctEl = document.getElementById("progress-percent");
  if (pctEl) pctEl.innerText = `${{pct}}% Completed`;
  
  const progFill = document.getElementById("progress-fill");
  if (progFill) progFill.style.width = `${{pct}}%`;
  const needle = document.getElementById("timeline-needle");
  if (needle) needle.style.left = `${{pct}}%`;

  // 2. Active Subarray Partition Bounding Indicator
  const partRange = step.partition_range || {{ low: 0, high: n - 1 }};
  const pivotVal = step.pivot ? step.pivot.value : (currentTrace.input_data ? currentTrace.input_data[0] : 45);
  const subRangeEl = document.getElementById("subarray-range-text");
  if (subRangeEl) subRangeEl.innerText = `[low=${{partRange.low}} .. high=${{partRange.high}}]`;
  const boundRangeEl = document.getElementById("bound-partition-range");
  if (boundRangeEl) boundRangeEl.innerText = `arr[${{partRange.low}}..${{partRange.high}}]`;
  const pivotHeaderEl = document.getElementById("pivot-header-val");
  if (pivotHeaderEl) pivotHeaderEl.innerText = `Pivot Val = ${{pivotVal}}`;

  // 3. Swap Arc SVG
  const swapSvg = document.getElementById("swap-arc-svg");
  const swapA = step.swap ? step.swap.index_a : null;
  const swapB = step.swap ? step.swap.index_b : null;
  if (swapSvg) {{
    if (swapA !== null && swapB !== null && swapA !== swapB && n > 1) {{
      swapSvg.style.display = "block";
      const leftIdx = Math.min(swapA, swapB);
      const rightIdx = Math.max(swapA, swapB);
      const x1 = ((leftIdx + 0.5) / n) * 700;
      const x2 = ((rightIdx + 0.5) / n) * 700;
      const midX = (x1 + x2) / 2;
      const arcPath = document.getElementById("swap-arc-path");
      if (arcPath) arcPath.setAttribute("d", `M ${{x1}} 60 Q ${{midX}} -20 ${{x2}} 60`);
      const arcPill = document.getElementById("swap-arc-pill");
      if (arcPill) arcPill.setAttribute("transform", `translate(${{midX}}, 12)`);
    }} else {{
      swapSvg.style.display = "none";
    }}
  }}

  // 4. Render Data Bars
  const barsContainer = document.getElementById("bars-container");
  if (barsContainer) {{
    barsContainer.innerHTML = "";
    arr.forEach((val, i) => {{
      const hPct = Math.max(14, Math.min(96, Math.round((Number(val) / maxVal) * 92)));
      const isPivot = (step.pivot && step.pivot.index === i);
      const isSwapA = (swapA === i);
      const isSwapB = (swapB === i);
      const isSwap = isSwapA || isSwapB;
      const isComparing = (step.active_indices && step.active_indices.includes(i) && !isSwap && !isPivot);
      const isSorted = (step.sorted_indices && step.sorted_indices.includes(i));

      let topBadge = '<div class="h-4"></div>';
      if (isPivot) {{
        topBadge = `
          <div class="px-2 py-0.5 rounded-full bg-tertiary-container text-on-tertiary-container font-label-sm text-[10px] font-bold tracking-wider shadow-sm flex items-center gap-0.5 animate-bounce">
            <span class="material-symbols-outlined text-[12px]">flag</span> PIVOT
          </div>`;
      }} else if (isSwap) {{
        const ptrLabel = isSwapA ? "i=" + i : "j=" + i;
        topBadge = `
          <div class="px-2 py-0.5 rounded bg-error-container text-on-error-container font-label-sm text-[10px] font-bold tracking-tight shadow-md flex items-center gap-1">
            <span>${{ptrLabel}}</span> <span class="material-symbols-outlined text-[12px]">arrow_downward</span>
          </div>`;
      }}

      let barStyle = "w-full rounded-t-lg flex flex-col justify-between items-center py-2 transition-all ";
      let indexPillStyle = "px-2 py-0.5 rounded font-code-sm text-code-sm ";
      let pointerText = "unvisited";
      let pointerClass = "text-[11px] font-code-sm text-outline-variant";

      if (isPivot) {{
        barStyle += "h-[" + hPct + "%] bg-gradient-to-t from-tertiary/20 to-tertiary/90 shadow-lg shadow-tertiary/10";
        indexPillStyle += "bg-surface-container text-tertiary font-semibold";
        pointerText = "low • pvt";
        pointerClass = "text-[11px] font-code-sm text-tertiary font-semibold tracking-tight";
      }} else if (isSwap) {{
        barStyle += "h-[" + hPct + "%] bg-gradient-to-t from-error-container to-error shadow-xl shadow-error/30 animate-pulse";
        indexPillStyle += "bg-error/20 text-error font-bold";
        pointerText = isSwapA ? "i (left > " + pivotVal + ")" : "j (right < " + pivotVal + ")";
        pointerClass = "text-[11px] font-code-sm text-error font-bold tracking-tight";
      }} else if (isComparing) {{
        barStyle += "h-[" + hPct + "%] bg-gradient-to-t from-primary/30 to-primary shadow-lg shadow-primary/20";
        indexPillStyle += "bg-primary/20 text-primary font-bold";
        pointerText = "comparing";
        pointerClass = "text-[11px] font-code-sm text-primary font-semibold";
      }} else if (isSorted) {{
        barStyle += "h-[" + hPct + "%] bg-gradient-to-t from-emerald-900/40 to-emerald-500 shadow-md";
        indexPillStyle += "bg-emerald-950 text-emerald-400 font-semibold";
        pointerText = "sorted";
        pointerClass = "text-[11px] font-code-sm text-emerald-400";
      }} else {{
        barStyle += "h-[" + hPct + "%] bg-surface-container-highest";
        indexPillStyle += "bg-surface-container text-outline";
        pointerText = (val <= pivotVal) ? "≤ " + pivotVal : "unvisited";
      }}

      const barHtml = `
        <div class="flex-1 flex flex-col items-center justify-end h-full gap-2 relative group" style="height: 100%;">
          ${{topBadge}}
          <div class="${{barStyle}}" style="height: ${{hPct}}%;">
            <span class="font-code-md text-code-md font-bold ${{isSwap ? 'text-on-error' : (isPivot ? 'text-surface-container-lowest' : 'text-on-surface-variant')}}">${{val}}</span>
            ${{isSwap ? '<span class="material-symbols-outlined text-on-error text-[14px]">priority_high</span>' : ''}}
          </div>
          <div class="${{indexPillStyle}}">[${{i}}]</div>
          <span class="${{pointerClass}}">${{pointerText}}</span>
        </div>`;
      barsContainer.insertAdjacentHTML('beforeend', barHtml);
    }});
  }}

  // 5. Memory Watcher Grid
  const wPvtVal = document.getElementById("watch-pivot-val");
  if (wPvtVal) wPvtVal.innerText = pivotVal;
  const wPvtIdx = document.getElementById("watch-pivot-idx");
  if (wPvtIdx) wPvtIdx.innerText = step.pivot ? step.pivot.index : (partRange.low || 0);

  const ptrI = step.pointers && step.pointers.i !== undefined ? step.pointers.i : (swapA !== null ? swapA : 2);
  const ptrJ = step.pointers && step.pointers.j !== undefined ? step.pointers.j : (swapB !== null ? swapB : 7);
  const wLeftPtr = document.getElementById("watch-left-ptr");
  if (wLeftPtr) wLeftPtr.innerHTML = `${{ptrI}} <span class="text-[10px] font-normal text-outline">val: ${{arr[ptrI] || 78}}</span>`;
  const wRightPtr = document.getElementById("watch-right-ptr");
  if (wRightPtr) wRightPtr.innerHTML = `${{ptrJ}} <span class="text-[10px] font-normal text-outline">val: ${{arr[ptrJ] || 18}}</span>`;

  const wComps = document.getElementById("watch-comparisons");
  if (wComps) wComps.innerText = step.metrics ? step.metrics.comparisons : 9;
  const wSwaps = document.getElementById("watch-swaps");
  if (wSwaps) wSwaps.innerText = step.metrics ? step.metrics.swaps : 1;

  // 6. "Why this step?" Cognitive Explanation
  const expText = document.getElementById("why-this-step-text");
  if (expText && step.explanation) {{
    expText.innerText = step.explanation;
  }}

  // 7. Python Source Tracer - Active Line Highlight
  const lineNum = step.code_line || 11;
  document.querySelectorAll("[data-code-line]").forEach(el => {{
    const l = Number(el.getAttribute("data-code-line"));
    if (l === lineNum) {{
      el.className = "px-2 py-1 bg-error-container text-on-error-container font-semibold rounded flex items-center gap-3 shadow-md";
      const icon = el.querySelector(".line-pointer-icon");
      if (icon) icon.style.display = "inline-flex";
    }} else {{
      el.className = "px-2 py-0.5 text-outline flex gap-3";
      const icon = el.querySelector(".line-pointer-icon");
      if (icon) icon.style.display = "none";
    }}
  }});

  // 8. Event Stream Ticker
  const streamTicker = document.getElementById("event-stream-ticker");
  if (streamTicker) {{
    streamTicker.innerHTML = `
      <span class="opacity-70">[Step ${{stepNum}}] Op: ${{step.operation}}</span>
      <span class="text-outline-variant">•</span>
      <span class="text-error font-semibold bg-error/10 px-1.5 py-0.5 rounded flex items-center gap-1">
        <span class="w-1.5 h-1.5 rounded-full bg-error animate-ping"></span>
        ${{step.explanation || 'Executing algorithm step'}}
      </span>
    `;
  }}
}}

// Play / Pause Simulation
function togglePlay() {{
  if (isPlaying) {{
    pause();
  }} else {{
    play();
  }}
}}

function play() {{
  isPlaying = true;
  updatePlayButtonUI(true);
  clearInterval(playTimer);
  playTimer = setInterval(() => {{
    if (currentStepIdx < currentTrace.steps.length - 1) {{
      renderStep(currentStepIdx + 1);
    }} else {{
      pause();
    }}
  }}, clockSpeedMs);
}}

function pause() {{
  isPlaying = false;
  clearInterval(playTimer);
  updatePlayButtonUI(false);
}}

function updatePlayButtonUI(playing) {{
  const btn = document.getElementById("btn-play-pause");
  const icon = document.getElementById("play-pause-icon");
  const text = document.getElementById("play-pause-text");
  const vcrBtn = document.getElementById("vcr-play-pause-btn");
  const vcrIcon = document.getElementById("vcr-play-pause-icon");
  const vcrText = document.getElementById("vcr-play-pause-text");

  if (playing) {{
    if (icon) icon.innerText = "pause";
    if (text) text.innerText = "Pause Execution";
    if (vcrIcon) vcrIcon.innerText = "pause";
    if (vcrText) vcrText.innerText = "Pause";
  }} else {{
    if (icon) icon.innerText = "play_arrow";
    if (text) text.innerText = "Resume Execution";
    if (vcrIcon) vcrIcon.innerText = "play_arrow";
    if (vcrText) vcrText.innerText = "Play";
  }}
}}

function stepNext() {{
  pause();
  if (currentStepIdx < currentTrace.steps.length - 1) {{
    renderStep(currentStepIdx + 1);
  }}
}}

function stepPrev() {{
  pause();
  if (currentStepIdx > 0) {{
    renderStep(currentStepIdx - 1);
  }}
}}

function stepFirst() {{
  pause();
  renderStep(0);
}}

function stepLast() {{
  pause();
  renderStep(currentTrace.steps.length - 1);
}}

function resetSimulation() {{
  pause();
  renderStep(0);
}}

// Clock Speed Handler
function setClockSpeed(speedMs, label) {{
  clockSpeedMs = speedMs;
  const speedLabel = document.getElementById("clock-speed-label");
  if (speedLabel) speedLabel.innerText = label;
  if (isPlaying) {{
    play(); // restart with new interval
  }}
}}

// Scrub Scrubber click handler
document.addEventListener("DOMContentLoaded", () => {{
  const scrubber = document.getElementById("timeline-scrubber");
  if (scrubber) {{
    scrubber.addEventListener("click", (e) => {{
      const rect = scrubber.getBoundingClientRect();
      const clickX = e.clientX - rect.left;
      const ratio = Math.max(0, Math.min(1, clickX / rect.width));
      const targetStep = Math.round(ratio * (currentTrace.steps.length - 1));
      pause();
      renderStep(targetStep);
    }});
  }}

  // Attach button events
  const btnPlay = document.getElementById("btn-play-pause");
  if (btnPlay) btnPlay.addEventListener("click", togglePlay);

  const vcrPlay = document.getElementById("vcr-play-pause-btn");
  if (vcrPlay) vcrPlay.addEventListener("click", togglePlay);

  const btnReset = document.getElementById("btn-reset");
  if (btnReset) btnReset.addEventListener("click", resetSimulation);

  const btnNext = document.getElementById("btn-vcr-next");
  if (btnNext) btnNext.addEventListener("click", stepNext);

  const btnPrev = document.getElementById("btn-vcr-prev");
  if (btnPrev) btnPrev.addEventListener("click", stepPrev);

  const btnFirst = document.getElementById("btn-vcr-first");
  if (btnFirst) btnFirst.addEventListener("click", stepFirst);

  const btnLast = document.getElementById("btn-vcr-last");
  if (btnLast) btnLast.addEventListener("click", stepLast);

  // Speed buttons
  document.querySelectorAll("[data-speed-ms]").forEach(btn => {{
    btn.addEventListener("click", () => {{
      const ms = Number(btn.getAttribute("data-speed-ms"));
      const lbl = btn.innerText.trim();
      setClockSpeed(ms, lbl);
    }});
  }});

  // Keyboard shortcuts (Space = play/pause, J = prev, K = next)
  window.addEventListener("keydown", (e) => {{
    if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;
    if (e.code === "Space") {{
      e.preventDefault();
      togglePlay();
    }} else if (e.code === "KeyK") {{
      stepNext();
    }} else if (e.code === "KeyJ") {{
      stepPrev();
    }}
  }});

  // Algorithm Selector Change
  const algoSelect = document.getElementById("algo-select");
  if (algoSelect) {{
    algoSelect.addEventListener("change", async () => {{
      const val = algoSelect.value;
      currentAlgorithm = val;
      await executeAndLoadTrace();
    }});
  }}

  // Array Input Enter / Change
  const arrayInput = document.getElementById("array-input");
  if (arrayInput) {{
    arrayInput.addEventListener("change", async () => {{
      await executeAndLoadTrace();
    }});
  }}

  // Initial render at step 16 (matches Stitch screenshot 3 exactly!)
  renderStep(16);
}});

// Fetch Real Trace from Flask API
async function executeAndLoadTrace() {{
  pause();
  const arrayInput = document.getElementById("array-input");
  let rawStr = arrayInput ? arrayInput.value : "[45, 12, 78, 23, 9, 34, 67, 18]";
  
  // Clean string
  rawStr = rawStr.replace(/[\\[\\]]/g, "");
  const numbers = rawStr.split(/[,\\s]+/).filter(Boolean).map(Number);
  
  try {{
    const res = await fetch("/api/execute", {{
      method: "POST",
      headers: {{ "Content-Type": "application/json" }},
      body: JSON.stringify({{
        algorithm: currentAlgorithm,
        data: numbers,
        params: {{ partition_scheme: currentScheme }}
      }})
    }});
    if (res.ok) {{
      const traceData = await res.json();
      currentTrace = traceData;
      renderStep(0);
    }} else {{
      console.warn("API returned error, using local fallback");
    }}
  }} catch (err) {{
    console.warn("Fetch failed, using current trace", err);
  }}
}}

// Algorithm Library Search & Filter (Screenshot 2)
function filterCatalog(query) {{
  query = (query || "").toLowerCase();
  document.querySelectorAll("[data-catalog-card]").forEach(card => {{
    const name = (card.getAttribute("data-algo-name") || "").toLowerCase();
    const desc = card.innerText.toLowerCase();
    if (name.includes(query) || desc.includes(query)) {{
      card.style.display = "block";
    }} else {{
      card.style.display = "none";
    }}
  }});
}}

const searchInput = document.getElementById("algoSearch");
if (searchInput) {{
  searchInput.addEventListener("input", (e) => filterCatalog(e.target.value));
}}

// Launch in Visualizer buttons
document.querySelectorAll("[data-launch-algo]").forEach(btn => {{
  btn.addEventListener("click", (e) => {{
    e.preventDefault();
    const algo = btn.getAttribute("data-launch-algo");
    const select = document.getElementById("algo-select");
    if (select) {{
      select.value = algo;
      currentAlgorithm = algo;
    }}
    switchTab("visualize");
    executeAndLoadTrace();
  }});
}});
</script>
"""

print("Writing unified frontend...")
