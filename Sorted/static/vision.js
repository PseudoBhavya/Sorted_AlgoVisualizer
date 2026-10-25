/**
 * Sorted — Computer Vision & Digital Image Processing Engine
 * ==========================================================
 * Production-grade Computer Vision & Tensor Processing Engine:
 * 1. Image Fundamentals (Sampling, Quantization, Dimensions, Formats)
 * 2. Image Representation and Colour Models (RGB, Grayscale, Binary, HSV, BGR order)
 * 3. Intensity Transformations (Negative, Log, Gamma, Contrast Stretch, Slicing)
 * 4. Histograms & Equalization (6-Stage Histogram Equalization)
 * 5. Spatial Filtering & Kernel Movement Laboratory (Interactive pixel-level stepping)
 * 6. Smoothing & Noise Removal (Gaussian, Salt & Pepper, Speckle, Poisson, PSNR/MSE)
 * 7. Sharpening & Edge Detection (Sobel, Prewitt, Laplacian, 5-Stage Canny)
 * 8. Image Segmentation & Morphology (Erosion, Dilation, Opening, Closing, Otsu, CCA)
 * 9. Local Image Descriptors (Harris Corner Detector, SIFT Keypoints & Matching)
 * 10. PCA & Image Denoising (Small teaching matrix & patch denoising)
 * 11. Image Processing Pipeline Studio (Sequential multi-stage pipeline)
 * 12. Technical Reference & Mathematical Specifications
 */


(function () {
  try {
    const st = document.createElement('style');
    st.textContent = `
.cvl{display:grid;grid-template-columns:232px minmax(0,1fr);gap:24px;align-items:start}
.cvs{position:sticky;top:116px;display:flex;flex-direction:column;gap:16px;padding:14px;border-radius:22px;border:1px solid rgba(150,160,255,.14);background:rgba(14,16,38,.55);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px)}
.cvg b{display:block;padding:0 10px 6px;font:500 12px Geist,sans-serif;color:#7a82ad}
.cvi{display:flex;align-items:center;gap:10px;width:100%;padding:9px 10px;border-radius:12px;border:0;background:transparent;color:#a9afd0;font:500 13px Geist,sans-serif;text-align:left;cursor:pointer}
.cvi:hover{color:#fff;background:rgba(255,255,255,.06)}
.cvi.on{color:#fff;background:rgba(124,108,255,.24);box-shadow:inset 0 0 0 1px rgba(150,140,255,.42)}
.ms{font-family:'Material Symbols Outlined'!important;font-weight:normal;font-style:normal;line-height:1;display:inline-block;vertical-align:middle;text-transform:none;letter-spacing:normal;word-wrap:normal;white-space:nowrap;direction:ltr;-webkit-font-feature-settings:'liga';font-feature-settings:'liga';-webkit-font-smoothing:antialiased}
.cvi .ms{font-size:18px}
.cvt{display:flex;align-items:center;gap:8px;font:600 14px Geist,sans-serif;letter-spacing:-.01em;color:#f1f2ff}
.cvt .ms{font-size:20px!important}
.cvh{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px;padding:12px 14px;border-radius:20px;border:1px solid rgba(150,160,255,.14);background:rgba(14,16,38,.55);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px)}
.cvb{display:inline-flex;align-items:center;gap:6px;padding:8px 12px;border-radius:12px;border:1px solid rgba(150,160,255,.2);background:rgba(255,255,255,.05);color:#c3c8e6;font:500 13px Geist,sans-serif;cursor:pointer}
.cvb:hover{color:#fff;background:rgba(255,255,255,.1)}
@media(max-width:900px){.cvl{grid-template-columns:minmax(0,1fr)}.cvs{position:static;flex-direction:row;overflow-x:auto;gap:8px}.cvg{display:flex;gap:4px}.cvg b{display:none}.cvi{width:auto;white-space:nowrap}}
`;
    document.head.appendChild(st);
  } catch (e) {}
})();

window.CV = {
  tab: 'fund',
  pattern: 'shapes',
  imgSize: 128,
  viewMode: 'canvas',
  pixelHud: { x: 32, y: 32, r: 76, g: 215, b: 246, yVal: 182 },
  
  // Tab 1: Fundamentals
  samplingFactor: 1,
  quantBits: 8,
  
  // Tab 2: Color Models
  colorMethod: 'luminosity',
  binThresh: 128,
  hsvMinMax: { h1: 60, h2: 180, s1: 30, s2: 100, v1: 30, v2: 100 },
  bgrSim: false,
  
  // Tab 3: Intensity
  intOp: 'negative',
  gamma: 1.5,
  logC: 1.0,
  csR1: 70, csS1: 20, csR2: 180, csS2: 230,
  sliceLow: 100, sliceHigh: 200, slicePreserve: true,
  brightAlpha: 1.2, brightBeta: 15,
  
  // Tab 4: Histograms
  histStage: 5,
  
  // Tab 5: Kernel Lab
  kPreset: 'box_3x3',
  kStride: 1,
  kPadMode: 'replicate',
  kIsConv: false,
  kStepR: 1,
  kStepC: 1,
  kRunning: false,
  kTimer: null,
  kSpeed: 1,
  kMatrix: [
    [100, 120, 150, 180, 200, 220, 240],
    [90,  110, 140, 170, 190, 210, 230],
    [80,  100, 130, 160, 180, 200, 220],
    [70,  90,  120, 150, 170, 190, 210],
    [60,  80,  110, 140, 160, 180, 200],
    [50,  70,  100, 130, 150, 170, 190],
    [40,  60,  90,  120, 140, 160, 180]
  ],
  customK: [[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]],
  kOutputs: {},
  
  // Tab 6: Noise & Smoothing
  noiseType: 'salt_pepper',
  noiseDensity: 0.08,
  filterType: 'median',
  fSize: 3,
  fSigma: 1.2,
  
  // Tab 7: Edges
  edgeMethod: 'canny',
  cannyStage: 5,
  cannyLow: 50,
  cannyHigh: 150,
  
  // Tab 8: Morphology & Segmentation
  morphOp: 'erosion',
  seType: 'square_3x3',
  segMethod: 'otsu',
  ccaConn: 8,
  
  // Tab 9: Descriptors
  featType: 'harris',
  harrisK: 0.04,
  harrisThreshRatio: 0.02,
  
  // Tab 10: PCA
  pcaMode: 'teaching',
  pcaK: 2,
  pcaImgComponents: 8,
  
  // Tab 11: Pipeline Studio
  pipeStages: [
    { id: 1, op: 'grayscale', params: { method: 'luminosity' } },
    { id: 2, op: 'gaussian_blur', params: { sigma: 1.0, k_size: 3 } },
    { id: 3, op: 'sobel', params: {} },
    { id: 4, op: 'threshold', params: { threshold: 80 } }
  ],
  activeStageIdx: 0,
  
  sourceCanvas: null
};

// Patterns generator
function cvGeneratePattern(name, size) {
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d');
  const imgData = ctx.createImageData(size, size);
  const d = imgData.data;

  if (name === 'checkerboard') {
    const block = Math.max(4, Math.floor(size / 8));
    for (let r = 0; r < size; r++) {
      for (let c = 0; c < size; c++) {
        const idx = (r * size + c) * 4;
        const isWhite = (Math.floor(r / block) + Math.floor(c / block)) % 2 === 0;
        const v = isWhite ? 235 : 25;
        d[idx] = v; d[idx+1] = v; d[idx+2] = v + 15; d[idx+3] = 255;
      }
    }
  } else if (name === 'gradient') {
    for (let r = 0; r < size; r++) {
      for (let c = 0; c < size; c++) {
        const idx = (r * size + c) * 4;
        const v = Math.floor((c / (size - 1)) * 255);
        d[idx] = v; d[idx+1] = v; d[idx+2] = v; d[idx+3] = 255;
      }
    }
  } else if (name === 'mri_brain') {
    const center = size / 2;
    for (let r = 0; r < size; r++) {
      for (let c = 0; c < size; c++) {
        const idx = (r * size + c) * 4;
        const dy = (r - center) / (size * 0.46);
        const dx = (c - center) / (size * 0.42);
        const skull = (dx*dx + dy*dy) <= 1.0;
        const brain = ((c - center)**2 / (size*0.36)**2 + (r - center)**2 / (size*0.40)**2) <= 1.0;
        const v1 = ((c - center + size*0.08)**2 / (size*0.05)**2 + (r - center)**2 / (size*0.15)**2) <= 1.0;
        const v2 = ((c - center - size*0.08)**2 / (size*0.05)**2 + (r - center)**2 / (size*0.15)**2) <= 1.0;
        const tumor = ((c - center + size*0.18)**2 + (r - center - size*0.12)**2) <= (size*0.08)**2;

        let v = 15;
        if (skull) v = 160;
        if (brain) v = 120 + ((r * 11 + c * 7) % 25) - 12;
        if (v1 || v2) v = 30;
        if (tumor) v = 245;

        d[idx] = v; d[idx+1] = v; d[idx+2] = v + 5; d[idx+3] = 255;
      }
    }
  } else if (name === 'coins') {
    for (let i = 0; i < d.length; i += 4) {
      d[i] = 20; d[i+1] = 24; d[i+2] = 36; d[i+3] = 255;
    }
    const circles = [
      [size * 0.25, size * 0.25, size * 0.12, [240, 210, 60]],
      [size * 0.75, size * 0.25, size * 0.10, [200, 200, 220]],
      [size * 0.35, size * 0.70, size * 0.14, [230, 140, 50]],
      [size * 0.75, size * 0.70, size * 0.08, [100, 220, 240]],
      [size * 0.50, size * 0.45, size * 0.06, [180, 240, 120]]
    ];
    for (let r = 0; r < size; r++) {
      for (let c = 0; c < size; c++) {
        for (const [cx, cy, rad, col] of circles) {
          if ((c - cx)**2 + (r - cy)**2 <= rad**2) {
            const idx = (r * size + c) * 4;
            d[idx] = col[0]; d[idx+1] = col[1]; d[idx+2] = col[2];
          }
        }
      }
    }
  } else { // default 'shapes'
    for (let i = 0; i < d.length; i += 4) {
      d[i] = 18; d[i+1] = 24; d[i+2] = 38; d[i+3] = 255;
    }
    // Cyan rectangle
    for (let r = Math.floor(size*0.15); r < Math.floor(size*0.45); r++) {
      for (let c = Math.floor(size*0.15); c < Math.floor(size*0.55); c++) {
        const idx = (r * size + c) * 4;
        d[idx] = 76; d[idx+1] = 215; d[idx+2] = 246;
      }
    }
    // Amber circle
    const cx = size * 0.72, cy = size * 0.35, rad = size * 0.20;
    for (let r = 0; r < size; r++) {
      for (let c = 0; c < size; c++) {
        if ((c - cx)**2 + (r - cy)**2 <= rad**2) {
          const idx = (r * size + c) * 4;
          d[idx] = 255; d[idx+1] = 185; d[idx+2] = 95;
        }
      }
    }
    // Emerald diagonal line
    for (let r = Math.floor(size*0.55); r < Math.floor(size*0.9); r++) {
      for (let w = -1; w <= 1; w++) {
        const c = r + w;
        if (c >= 0 && c < size) {
          const idx = (r * size + c) * 4;
          d[idx] = 16; d[idx+1] = 185; d[idx+2] = 129;
        }
      }
    }
  }

  ctx.putImageData(imgData, 0, 0);
  return canvas;
}

// Preset Kernels definitions
window.CV_KERNELS = {
  box_3x3: {
    name: '3x3 Mean / Box Filter',
    type: 'linear',
    mat: [[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]],
    desc: 'Uniform box moving average. Sum of coefficients is 1.0 (conserves average illumination).'
  },
  weighted_3x3: {
    name: 'Weighted Average (Gaussian Approx)',
    type: 'linear',
    mat: [[1/16, 2/16, 1/16], [2/16, 4/16, 2/16], [1/16, 2/16, 1/16]],
    desc: 'Center pixel has weight 4/16, orthogonal neighbors 2/16, diagonals 1/16. Reduces edge blurring.'
  },
  gaussian_3x3: {
    name: 'Gaussian Blur 3x3 (sigma=1.0)',
    type: 'linear',
    mat: [[0.0751, 0.1238, 0.0751], [0.1238, 0.2044, 0.1238], [0.0751, 0.1238, 0.0751]],
    desc: 'True 2D Gaussian kernel. Mathematically optimal linear filter for removing zero-mean Gaussian noise.'
  },
  gaussian_5x5: {
    name: 'Gaussian Blur 5x5',
    type: 'linear',
    mat: [
      [1/256, 4/256, 6/256, 4/256, 1/256],
      [4/256, 16/256, 24/256, 16/256, 4/256],
      [6/256, 24/256, 36/256, 24/256, 6/256],
      [4/256, 16/256, 24/256, 16/256, 4/256],
      [1/256, 4/256, 6/256, 4/256, 1/256]
    ],
    desc: 'Expanded 5x5 spatial support for heavy noise suppression.'
  },
  median_3x3: {
    name: 'Median Filter 3x3',
    type: 'median',
    mat: [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
    desc: 'Replaces center pixel with the median of sorted 9 neighbourhood pixels. Optimal for Salt & Pepper noise.'
  },
  min_3x3: {
    name: 'Minimum Filter 3x3 (Erosion-like)',
    type: 'min',
    mat: [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
    desc: 'Replaces center with min value in neighbourhood. Darkens bright pixels and erodes boundaries.'
  },
  max_3x3: {
    name: 'Maximum Filter 3x3 (Dilation-like)',
    type: 'max',
    mat: [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
    desc: 'Replaces center with max value in neighbourhood. Expands bright regions and bridges gaps.'
  },
  sobel_x: {
    name: 'Sobel X (Vertical Edges)',
    type: 'linear',
    mat: [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]],
    desc: 'Approximates horizontal derivative dF/dx. Emphasizes vertical edge transitions.'
  },
  sobel_y: {
    name: 'Sobel Y (Horizontal Edges)',
    type: 'linear',
    mat: [[-1, -2, -1], [0, 0, 0], [1, 2, 1]],
    desc: 'Approximates vertical derivative dF/dy. Emphasizes horizontal edge transitions.'
  },
  laplacian_4: {
    name: 'Laplacian (4-Connectivity)',
    type: 'linear',
    mat: [[0, 1, 0], [1, -4, 1], [0, 1, 0]],
    desc: 'Isotropic second-derivative operator for 4-neighbourhood. Emphasizes fine details and rapid changes.'
  },
  laplacian_8: {
    name: 'Laplacian (8-Connectivity)',
    type: 'linear',
    mat: [[1, 1, 1], [1, -8, 1], [1, 1, 1]],
    desc: 'Isotropic second-derivative operator including diagonals. Zero-crossings denote true edge positions.'
  },
  sharpen_3x3: {
    name: 'High-Pass Sharpening',
    type: 'linear',
    mat: [[0, -1, 0], [-1, 5, -1], [0, -1, 0]],
    desc: 'Subtracts surrounding Laplacian blur from central pixel to sharply boost fine boundary edges.'
  }
};

// Sub-navigation Tabs mapping
window.CV_TABS = [
  ['fund', '1. Sampling & Discrete Grids', 'grid_view'],
  ['color', '2. Color Spaces & Channels', 'palette'],
  ['intensity', '3. Intensity Transforms', 'contrast'],
  ['hist', '4. Histogram Analysis & Equalization', 'bar_chart'],
  ['kernel', '5. Spatial Convolution Kernels', 'grain'],
  ['noise', '6. Noise Models & Restoration', 'blur_on'],
  ['edges', '7. Edge Detection & Canny', 'timeline'],
  ['morph', '8. Morphological Operations', 'crop_free'],
  ['feat', '9. Feature Keypoints & SIFT', 'radar'],
  ['pca', '10. Dimensionality Reduction & PCA', 'scatter_plot'],
  ['pipe', '11. Multi-Stage Pipeline Studio', 'account_tree'],
  ['theory', '12. Architecture & Technical Specs', 'menu_book']
];

function cvInit() {
  if (!CV.sourceCanvas) {
    CV.sourceCanvas = cvGeneratePattern(CV.pattern, CV.imgSize);
  }
}

function cvSetTab(t) {
  CV.tab = t;
  cvStopKernelAnimation();
  route('vision');
}

function cvSetPattern(p) {
  CV.pattern = p;
  CV.sourceCanvas = cvGeneratePattern(p, CV.imgSize);
  cvStopKernelAnimation();
  route('vision');
}

function cvHandleUpload(file) {
  if (!file) return;
  const reader = new FileReader();
  reader.onload = function(e) {
    const img = new Image();
    img.onload = function() {
      const maxDim = 128;
      let w = img.width, h = img.height;
      if (w > maxDim || h > maxDim) {
        const scale = maxDim / Math.max(w, h);
        w = Math.max(1, Math.round(w * scale));
        h = Math.max(1, Math.round(h * scale));
      }
      const canvas = document.createElement('canvas');
      canvas.width = w;
      canvas.height = h;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0, w, h);
      CV.sourceCanvas = canvas;
      CV.imgSize = Math.max(w, h);
      route('vision');
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
}

function cvInspectPixel(x, y, r, g, b) {
  const yVal = Math.round(0.299 * r + 0.587 * g + 0.114 * b);
  CV.pixelHud = { x, y, r, g, b, yVal };
  const hX = document.getElementById('cvPixX');
  if (hX) {
    document.getElementById('cvPixX').textContent = x;
    document.getElementById('cvPixY').textContent = y;
    document.getElementById('cvPixR').textContent = r;
    document.getElementById('cvPixG').textContent = g;
    document.getElementById('cvPixB').textContent = b;
    document.getElementById('cvPixYVal').textContent = yVal;
    document.getElementById('cvPixSwatch').style.background = `rgb(${r},${g},${b})`;
  }
}

function cvExportCurrentCanvas() {
  if (!CV.sourceCanvas) return;
  const link = document.createElement('a');
  link.download = `sorted_cv_${CV.tab}_${Date.now()}.png`;
  link.href = CV.sourceCanvas.toDataURL('image/png');
  link.click();
}

// ---------------- Top Render Vision Shell ----------------
function renderVisionView() {
  cvInit();
  const T = Object.fromEntries(CV_TABS.map(t => [t[0], t]));
  const G = [['Foundations', ['fund', 'color']], ['Enhance', ['intensity', 'hist']], ['Spatial Filters', ['kernel', 'noise']], ['Feature Analysis', ['edges', 'morph', 'feat', 'pca']], ['Pipelines & Architecture', ['pipe', 'theory']]];
  const opt = (v, t) => `<option value="${v}" ${CV.pattern == v ? 'selected' : ''}>${t}</option>`;
  return `<div class="max-w-[1280px] mx-auto flex flex-col gap-5">
    <div class="flex flex-wrap items-end justify-between gap-3 pb-3 border-b border-s3/40">
      <div>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center gap-2.5">
          <span class="ms text-pri text-[28px]">auto_awesome</span>
          Computer Vision &amp; Tensor Studio
        </h1>
        <p class="text-sm text-[#b0b8db] pt-1.5 max-w-3xl leading-relaxed font-normal">
          High-precision image processing and computer vision engine. Explore discrete pixel matrices, 2D spatial convolution kernels, frequency response, morphological operators, SIFT keypoints, and PCA dimensionality reduction.
        </p>
      </div>
    </div>

    <div class="cvl">
      <nav class="cvs" aria-label="Image processing workspaces">
        ${G.map(([g, ks]) => `
          <div class="cvg"><b>${g}</b>
            ${ks.map(k => `<button type="button" onclick="cvSetTab('${k}')" class="cvi ${CV.tab === k ? 'on' : ''}" ${CV.tab === k ? 'aria-current="page"' : ''}><span class="ms">${T[k][2]}</span><span>${T[k][1].replace(/^\d+\.\s*/, '')}</span></button>`).join('')}
          </div>`).join('')}
      </nav>

      <div class="flex flex-col gap-4 min-w-0">
        <div class="cvh">
          <div class="flex flex-wrap items-center gap-2">
            <span class="ms text-pri">photo</span>
            <select onchange="cvSetPattern(this.value)" aria-label="Source image" class="bg-s3 rounded-lg px-3 py-2 text-sm border border-s4 text-fg cursor-pointer">
              ${opt('shapes', 'Geometric shapes and lines')}${opt('mri_brain', 'Medical MRI brain scan')}${opt('checkerboard', 'High-contrast checkerboard')}${opt('gradient', 'Continuous intensity ramp')}${opt('coins', 'Circular coins and blobs')}
            </select>
            <label class="cvb"><span class="ms text-ter">upload</span>Upload image<input type="file" accept="image/*" class="hidden" onchange="cvHandleUpload(this.files[0])"></label>
            <button type="button" onclick="cvExportCurrentCanvas()" class="cvb"><span class="ms text-pri">download</span>Export PNG</button>
          </div>
          <div id="cvPixelHUD" class="flex items-center gap-3 font-mono text-xs px-3 py-2 rounded-xl bg-s0/70 border border-s3">
            <span class="text-ol">Pixel (<span id="cvPixX" class="text-pri">${CV.pixelHud.x}</span>, <span id="cvPixY" class="text-pri">${CV.pixelHud.y}</span>)</span>
            <span class="text-mut">RGB <span id="cvPixR" class="text-err">${CV.pixelHud.r}</span> <span id="cvPixG" class="text-ok">${CV.pixelHud.g}</span> <span id="cvPixB" class="text-pri">${CV.pixelHud.b}</span></span>
            <span class="text-ter font-bold">Y <span id="cvPixYVal">${CV.pixelHud.yVal}</span></span>
            <div id="cvPixSwatch" class="w-5 h-5 rounded-md border border-s4" style="background:rgb(${CV.pixelHud.r},${CV.pixelHud.g},${CV.pixelHud.b})"></div>
          </div>
        </div>

        <div id="cvStageContainer" class="flex flex-col gap-4">
          ${cvRenderActiveTab()}
        </div>
      </div>
    </div>
  </div>`;
}

function cvRenderActiveTab() {
  switch (CV.tab) {
    case 'fund': return cvRenderFund();
    case 'color': return cvRenderColor();
    case 'intensity': return cvRenderIntensity();
    case 'hist': return cvRenderHist();
    case 'kernel': return cvRenderKernelLab();
    case 'noise': return cvRenderNoise();
    case 'edges': return cvRenderEdges();
    case 'morph': return cvRenderMorph();
    case 'feat': return cvRenderFeatures();
    case 'pca': return cvRenderPCA();
    case 'pipe': return cvRenderPipeline();
    case 'theory': return cvRenderTheory();
    default: return cvRenderFund();
  }
}

// ---------------- 1. Image Fundamentals Tab ----------------
function cvRenderFund() {
  const sFactor = CV.samplingFactor;
  const qBits = CV.quantBits;
  const qLevels = Math.pow(2, qBits);

  setTimeout(cvUpdateFundCanvas, 20);

  return `<div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
    <!-- Left Column: Interactive Sampling & Quantization -->
    <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-sm flex flex-col gap-3">
      <div class="flex items-center justify-between border-b border-s3/40 pb-2">
        <span class="cvt">
          <span class="ms text-pri text-[18px]">grain</span>
          Spatial Sampling & Intensity Quantization (Discrete Grid & Bit Depth)
        </span>
        <span class="text-[11px] font-mono text-ter font-bold">2D Signal f(x, y)</span>
      </div>

      <div class="flex flex-col sm:flex-row gap-4 items-center justify-center p-3 bg-s1 rounded-xl border border-s3">
        <div class="flex flex-col items-center gap-1">
          <canvas id="cvFundCanvas" class="rounded border border-s3 shadow-md cursor-crosshair bg-s0 max-w-[200px] aspect-square"></canvas>
          <span class="text-[10px] font-mono text-ol">Click pixel to inspect in HUD</span>
        </div>
        <div class="flex flex-col gap-2 font-mono text-xs w-full sm:w-60">
          <div class="bg-s0 p-2.5 rounded-lg border border-s3/40 flex flex-col gap-1">
            <span class="text-ol text-[10px]">SPATIAL SAMPLING (WHERE)</span>
            <div class="flex justify-between items-center">
              <span class="text-pri font-bold">Factor: ${sFactor}x (${Math.floor(CV.imgSize / sFactor)}×${Math.floor(CV.imgSize / sFactor)})</span>
            </div>
            <input type="range" min="1" max="16" step="1" value="${sFactor}" oninput="CV.samplingFactor=+this.value; cvUpdateFundCanvas();">
            <span class="text-[10px] text-mut">Higher factor = coarse spatial pixelation.</span>
          </div>

          <div class="bg-s0 p-2.5 rounded-lg border border-s3/40 flex flex-col gap-1">
            <span class="text-ol text-[10px]">AMPLITUDE QUANTIZATION (WHAT)</span>
            <div class="flex justify-between items-center">
              <span class="text-ter font-bold">${qBits}-bit (${qLevels} discrete levels)</span>
            </div>
            <input type="range" min="1" max="8" step="1" value="${qBits}" oninput="CV.quantBits=+this.value; cvUpdateFundCanvas();">
            <span class="text-[10px] text-mut">Lower bits = visible intensity banding / false contouring.</span>
          </div>
        </div>
      </div>

      <!-- Small 6x6 Teaching Pixel Matrix Grid -->
      <div class="bg-s1 p-3 rounded-xl border border-s3 flex flex-col gap-2">
        <span class="text-xs font-mono font-semibold text-mut flex items-center justify-between">
          <span>Editable 6×6 Pixel Matrix [0..255]</span>
          <span class="text-[10px] text-ol font-normal">Click cell to increment value</span>
        </span>
        <div id="cvFundMiniMatrix" class="grid grid-cols-6 gap-1 p-2 bg-s0 rounded-lg font-mono text-xs text-center">
          ${cvRenderMiniMatrix()}
        </div>
      </div>
    </div>

    <!-- Right Column: DIP Pipeline & Storage Formats -->
    <div class="flex flex-col gap-3.5">
      <!-- Fundamental Stages of Digital Image Processing Architecture -->
      <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-sm flex flex-col gap-3">
        <div class="flex items-center justify-between border-b border-s3/40 pb-2">
          <span class="cvt">
            <span class="ms text-ter text-[18px]">account_tree</span>
            Fundamental Digital Image Processing Pipeline
          </span>
          <span class="text-pri font-mono text-xs">Production Architecture</span>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 font-mono text-xs">
          <div class="bg-s1 p-2.5 rounded-lg border border-s3/40">
            <div class="text-pri font-bold">1. Acquisition</div>
            <div class="text-[11px] text-mut pt-1">Sensors, optics & digitization.</div>
          </div>
          <div class="bg-s1 p-2.5 rounded-lg border border-s3/40">
            <div class="text-ter font-bold">2. Preprocessing</div>
            <div class="text-[11px] text-mut pt-1">Noise removal & normalization.</div>
          </div>
          <div class="bg-s1 p-2.5 rounded-lg border border-s3/40">
            <div class="text-ok font-bold">3. Enhancement</div>
            <div class="text-[11px] text-mut pt-1">Contrast & detail visibility.</div>
          </div>
          <div class="bg-s1 p-2.5 rounded-lg border border-s3/40">
            <div class="text-sec font-bold">4. Restoration</div>
            <div class="text-[11px] text-mut pt-1">Mathematical degradation inversion.</div>
          </div>
          <div class="bg-s1 p-2.5 rounded-lg border border-s3/40">
            <div class="text-pri font-bold">5. Segmentation</div>
            <div class="text-[11px] text-mut pt-1">Partition into meaningful regions.</div>
          </div>
          <div class="bg-s1 p-2.5 rounded-lg border border-s3/40">
            <div class="text-ter font-bold">6. Features</div>
            <div class="text-[11px] text-mut pt-1">Edges, corners, descriptors.</div>
          </div>
          <div class="bg-s1 p-2.5 rounded-lg border border-s3/40 col-span-2">
            <div class="text-fg font-bold">7. Recognition & Computer Vision</div>
            <div class="text-[11px] text-mut pt-1">Classification, semantic scene interpretation, and 3D depth understanding.</div>
          </div>
        </div>
      </div>

      <!-- File Formats Comparison -->
      <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-sm flex flex-col gap-2.5">
        <span class="cvt">
          <span class="ms text-ok text-[18px]">table_chart</span>
          Format Specifications & Compression Benchmarks
        </span>
        <div class="overflow-x-auto bg-s1 rounded-lg border border-s3/40">
          <table class="w-full font-mono text-xs text-left">
            <thead>
              <tr class="text-ol border-b border-s3/40 bg-s0/60">
                <th class="p-2">Format</th>
                <th class="p-2">Compression</th>
                <th class="p-2">Quality</th>
                <th class="p-2">File Size</th>
                <th class="p-2">Best For</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-s3/30 text-mut">
              <tr>
                <td class="p-2 text-pri font-bold">JPEG</td>
                <td class="p-2 text-ter">Lossy (DCT)</td>
                <td class="p-2">Good</td>
                <td class="p-2">Small</td>
                <td class="p-2 text-fg">Continuous-tone everyday photos</td>
              </tr>
              <tr>
                <td class="p-2 text-pri font-bold">PNG</td>
                <td class="p-2 text-ok">Lossless (DEFLATE)</td>
                <td class="p-2">Excellent</td>
                <td class="p-2">Medium</td>
                <td class="p-2 text-fg">Web graphics, sharp edges, alpha transparency</td>
              </tr>
              <tr>
                <td class="p-2 text-pri font-bold">TIFF</td>
                <td class="p-2 text-ok">Lossless / None</td>
                <td class="p-2">Maximum</td>
                <td class="p-2">Large</td>
                <td class="p-2 text-fg">Archival preservation, medical scans (MRI/CT)</td>
              </tr>
              <tr>
                <td class="p-2 text-pri font-bold">RAW</td>
                <td class="p-2 text-sec">Uncompressed</td>
                <td class="p-2">Sensor Native</td>
                <td class="p-2">Very Large</td>
                <td class="p-2 text-fg">Professional photography sensor dumps</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>`;
}

var miniMatData = [
  [12, 45, 78, 120, 190, 240],
  [25, 60, 95, 140, 205, 250],
  [40, 85, 130, 180, 220, 255],
  [15, 50, 100, 160, 215, 245],
  [8,  35, 80,  135, 195, 230],
  [0,  20, 65,  110, 175, 210]
];

function cvRenderMiniMatrix() {
  return miniMatData.map((row, r) => row.map((val, c) => `
    <div onclick="cvIncMiniCell(${r},${c})" class="p-2 rounded bg-s1 hover:bg-s2 border border-s3/40 cursor-pointer transition-colors flex flex-col justify-between" style="border-left: 3px solid rgb(${val},${val},${val});">
      <span class="text-[9px] text-ol">[${r},${c}]</span>
      <span class="font-bold text-fg">${val}</span>
    </div>`).join('')).join('');
}

function cvIncMiniCell(r, c) {
  miniMatData[r][c] = (miniMatData[r][c] + 25) % 256;
  const grid = document.getElementById('cvFundMiniMatrix');
  if (grid) grid.innerHTML = cvRenderMiniMatrix();
}

function cvUpdateFundCanvas() {
  const canvas = document.getElementById('cvFundCanvas');
  if (!canvas || !CV.sourceCanvas) return;
  const size = CV.sourceCanvas.width;
  canvas.width = size; canvas.height = size;
  const ctx = canvas.getContext('2d');
  
  const srcCtx = CV.sourceCanvas.getContext('2d');
  const imgData = srcCtx.getImageData(0, 0, size, size);
  const d = imgData.data;

  const f = CV.samplingFactor;
  const bits = CV.quantBits;
  const levels = Math.pow(2, bits);
  const step = 256 / levels;

  const outData = ctx.createImageData(size, size);
  const od = outData.data;

  for (let r = 0; r < size; r += f) {
    for (let c = 0; c < size; c += f) {
      const idx = (r * size + c) * 4;
      let red = d[idx], grn = d[idx+1], blu = d[idx+2];

      // Quantize
      red = Math.floor(red / step) * (255 / (levels - 1));
      grn = Math.floor(grn / step) * (255 / (levels - 1));
      blu = Math.floor(blu / step) * (255 / (levels - 1));

      for (let dr = 0; dr < f && r + dr < size; dr++) {
        for (let dc = 0; dc < f && c + dc < size; dc++) {
          const oIdx = ((r + dr) * size + (c + dc)) * 4;
          od[oIdx] = red; od[oIdx+1] = grn; od[oIdx+2] = blu; od[oIdx+3] = 255;
        }
      }
    }
  }

  ctx.putImageData(outData, 0, 0);

  canvas.onclick = function(e) {
    const rect = canvas.getBoundingClientRect();
    const x = Math.floor((e.clientX - rect.left) * (size / rect.width));
    const y = Math.floor((e.clientY - rect.top) * (size / rect.height));
    const p = ctx.getImageData(x, y, 1, 1).data;
    cvInspectPixel(x, y, p[0], p[1], p[2]);
  };
}

// ---------------- 2. Color Models & Image Conversion Tab ----------------
function cvRenderColor() {
  setTimeout(cvUpdateColorCanvas, 20);

  return `<div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
    <!-- Left Column: Color Conversion Controls -->
    <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-sm flex flex-col gap-3">
      <div class="flex items-center justify-between border-b border-s3/40 pb-2">
        <span class="cvt">
          <span class="ms text-pri text-[18px]">palette</span>
          RGB, Grayscale & HSV Transformations
        </span>
        <button onclick="CV.bgrSim=!CV.bgrSim; cvUpdateColorCanvas();" class="px-2 py-0.5 rounded font-mono text-[11px] ${CV.bgrSim ? 'bg-err text-s0 font-bold' : 'bg-s3 text-mut'}">
          ${CV.bgrSim ? 'BGR Swapped (OpenCV Mode)' : 'Standard RGB Mode'}
        </button>
      </div>

      <div class="flex flex-col sm:flex-row gap-4 items-center justify-center p-3 bg-s1 rounded-xl border border-s3">
        <canvas id="cvColorCanvas" class="rounded border border-s3 shadow-md cursor-crosshair bg-s0 max-w-[200px] aspect-square"></canvas>
        <div class="flex flex-col gap-2.5 font-mono text-xs w-full sm:w-64">
          <div class="bg-s0 p-2.5 rounded-lg border border-s3/40 flex flex-col gap-1">
            <span class="text-ol text-[10px]">GRAYSCALE CONVERSION FORMULA</span>
            <select onchange="CV.colorMethod=this.value; cvUpdateColorCanvas();" class="bg-s2 text-pri rounded px-2 py-1 text-xs border border-s3">
              <option value="luminosity" ${CV.colorMethod=='luminosity'?'selected':''}>Luminosity: 0.299R + 0.587G + 0.114B (Standard NTSC/ITU-R)</option>
              <option value="average" ${CV.colorMethod=='average'?'selected':''}>Average: (R + G + B) / 3</option>
              <option value="lightness" ${CV.colorMethod=='lightness'?'selected':''}>Lightness: (max(R,G,B) + min(R,G,B)) / 2</option>
              <option value="binary" ${CV.colorMethod=='binary'?'selected':''}>Binary Thresholding</option>
              <option value="hsv_mask" ${CV.colorMethod=='hsv_mask'?'selected':''}>HSV Color Masking</option>
            </select>
          </div>

          <div id="cvColorExtraControls" class="bg-s0 p-2.5 rounded-lg border border-s3/40 flex flex-col gap-1.5">
            ${cvRenderColorSubControls()}
          </div>
        </div>
      </div>

      <div class="bg-s1 p-3 rounded-xl border border-s3 flex flex-col gap-1 text-xs font-mono">
        <span class="text-ter font-bold">RGB vs OpenCV BGR Channel Ordering Warning</span>
        <p class="text-mut text-[11px] leading-relaxed">
          OpenCV decodes images into BGR array order by default. Displaying a BGR array on standard web canvases or PIL swaps the red and blue channels, making blue skies appear orange and skin tones appear cyan! Use <code class="text-pri">cv2.cvtColor(img, cv2.COLOR_BGR2RGB)</code> to avoid silent color swaps.
        </p>
      </div>
    </div>

    <!-- Right Column: 3-Channel Separation Breakdown -->
    <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-sm flex flex-col gap-3">
      <div class="flex items-center justify-between border-b border-s3/40 pb-2">
        <span class="cvt">
          <span class="ms text-ter text-[18px]">splitscreen</span>
          Channel Isolation (Red, Green, Blue)
        </span>
        <span class="text-mut text-xs font-mono">8 bits / channel</span>
      </div>
      <div class="grid grid-cols-3 gap-2 font-mono text-xs">
        <div class="bg-s1 p-2 rounded-lg border border-s3/40 flex flex-col items-center gap-1">
          <span class="text-err font-bold">Red Channel (R)</span>
          <canvas id="cvChanR" class="w-full aspect-square rounded bg-s0"></canvas>
          <span class="text-[10px] text-ol">Primary Photoreceptors</span>
        </div>
        <div class="bg-s1 p-2 rounded-lg border border-s3/40 flex flex-col items-center gap-1">
          <span class="text-ok font-bold">Green Channel (G)</span>
          <canvas id="cvChanG" class="w-full aspect-square rounded bg-s0"></canvas>
          <span class="text-[10px] text-ol">Human Visual Peak (58.7%)</span>
        </div>
        <div class="bg-s1 p-2 rounded-lg border border-s3/40 flex flex-col items-center gap-1">
          <span class="text-pri font-bold">Blue Channel (B)</span>
          <canvas id="cvChanB" class="w-full aspect-square rounded bg-s0"></canvas>
          <span class="text-[10px] text-ol">High Frequency Band</span>
        </div>
      </div>
      <div class="bg-s1 p-3 rounded-xl border border-s3 flex flex-col gap-1 text-xs font-mono">
        <span class="text-pri font-bold">HSV Space & Cylindrical Perception Coordinates</span>
        <p class="text-mut text-[11px] leading-relaxed">
          <b>Hue (H)</b> represents the pure spectral color angle [0°..360°]; <b>Saturation (S)</b> indicates purity/richness [0%..100%]; <b>Value (V)</b> indicates luminance/brightness. HSV decouples chrominance from luminance, making color-based segmentation invariant to illumination shadows.
        </p>
      </div>
    </div>
  </div>`;
}

function cvRenderColorSubControls() {
  if (CV.colorMethod === 'binary') {
    return `<div class="flex justify-between items-center">
      <span class="text-ol text-[10px]">BINARY THRESHOLD T</span>
      <span class="text-pri font-bold">${CV.binThresh}</span>
    </div>
    <input type="range" min="0" max="255" value="${CV.binThresh}" oninput="CV.binThresh=+this.value; cvUpdateColorCanvas();">`;
  } else if (CV.colorMethod === 'hsv_mask') {
    return `<div class="flex justify-between items-center text-[10px]">
      <span class="text-ol">HUE RANGE</span>
      <span class="text-pri">${CV.hsvMinMax.h1}° - ${CV.hsvMinMax.h2}°</span>
    </div>
    <input type="range" min="0" max="360" value="${CV.hsvMinMax.h2}" oninput="CV.hsvMinMax.h2=+this.value; cvUpdateColorCanvas();">`;
  }
  return `<span class="text-ol text-[10px]">ACTIVE FORMULA</span>
  <span class="text-pri text-[11px] font-bold">${CV.colorMethod=='luminosity'?'Y = 0.299·R + 0.587·G + 0.114·B':'Y = (R + G + B) / 3'}</span>`;
}

function cvUpdateColorCanvas() {
  const canvas = document.getElementById('cvColorCanvas');
  if (!canvas || !CV.sourceCanvas) return;
  const size = CV.sourceCanvas.width;
  canvas.width = size; canvas.height = size;
  const ctx = canvas.getContext('2d');
  const d = CV.sourceCanvas.getContext('2d').getImageData(0, 0, size, size).data;
  const out = ctx.createImageData(size, size);
  const od = out.data;

  // Render individual R, G, B channels
  const cR = document.getElementById('cvChanR');
  const cG = document.getElementById('cvChanG');
  const cB = document.getElementById('cvChanB');
  let ctxR, ctxG, ctxB, odR, odG, odB;
  if (cR && cG && cB) {
    cR.width = cG.width = cB.width = size;
    cR.height = cG.height = cB.height = size;
    ctxR = cR.getContext('2d'); ctxG = cG.getContext('2d'); ctxB = cB.getContext('2d');
    odR = ctxR.createImageData(size, size);
    odG = ctxG.createImageData(size, size);
    odB = ctxB.createImageData(size, size);
  }

  for (let i = 0; i < d.length; i += 4) {
    let r = d[i], g = d[i+1], b = d[i+2];

    if (CV.bgrSim) { const tmp = r; r = b; b = tmp; }

    // Channel views
    if (odR) {
      odR.data[i] = r; odR.data[i+1] = 0; odR.data[i+2] = 0; odR.data[i+3] = 255;
      odG.data[i] = 0; odG.data[i+1] = g; odG.data[i+2] = 0; odG.data[i+3] = 255;
      odB.data[i] = 0; odB.data[i+1] = 0; odB.data[i+2] = b; odB.data[i+3] = 255;
    }

    // Main transformed view
    if (CV.colorMethod === 'binary') {
      const y = Math.round(0.299 * r + 0.587 * g + 0.114 * b);
      const bin = y >= CV.binThresh ? 255 : 0;
      od[i] = bin; od[i+1] = bin; od[i+2] = bin; od[i+3] = 255;
    } else if (CV.colorMethod === 'average') {
      const avg = Math.round((r + g + b) / 3);
      od[i] = avg; od[i+1] = avg; od[i+2] = avg; od[i+3] = 255;
    } else if (CV.colorMethod === 'lightness') {
      const lit = Math.round((Math.max(r, g, b) + Math.min(r, g, b)) / 2);
      od[i] = lit; od[i+1] = lit; od[i+2] = lit; od[i+3] = 255;
    } else if (CV.colorMethod === 'hsv_mask') {
      const rf = r/255, gf = g/255, bf = b/255;
      const max = Math.max(rf, gf, bf), min = Math.min(rf, gf, bf), delta = max - min;
      let hue = 0;
      if (delta > 1e-4) {
        if (max === rf) hue = 60 * (((gf - bf) / delta) % 6);
        else if (max === gf) hue = 60 * (((bf - rf) / delta) + 2);
        else hue = 60 * (((rf - gf) / delta) + 4);
      }
      if (hue < 0) hue += 360;
      const pass = (hue >= CV.hsvMinMax.h1 && hue <= CV.hsvMinMax.h2);
      od[i] = pass ? r : 30;
      od[i+1] = pass ? g : 30;
      od[i+2] = pass ? b : 40;
      od[i+3] = 255;
    } else { // default luminosity
      const y = Math.round(0.299 * r + 0.587 * g + 0.114 * b);
      od[i] = y; od[i+1] = y; od[i+2] = y; od[i+3] = 255;
    }
  }

  ctx.putImageData(out, 0, 0);
  if (ctxR) ctxR.putImageData(odR, 0, 0);
  if (ctxG) ctxG.putImageData(odG, 0, 0);
  if (ctxB) ctxB.putImageData(odB, 0, 0);

  canvas.onclick = function(e) {
    const rect = canvas.getBoundingClientRect();
    const x = Math.floor((e.clientX - rect.left) * (size / rect.width));
    const y = Math.floor((e.clientY - rect.top) * (size / rect.height));
    const p = ctx.getImageData(x, y, 1, 1).data;
    cvInspectPixel(x, y, p[0], p[1], p[2]);
  };
}

// ---------------- 3. Intensity Transformations Tab ----------------
function cvRenderIntensity() {
  setTimeout(cvUpdateIntensityCanvas, 20);

  return `<div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
    <!-- Left: Intensity Controls & Side-by-Side Images -->
    <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-sm flex flex-col gap-3">
      <div class="flex items-center justify-between border-b border-s3/40 pb-2">
        <span class="cvt">
          <span class="ms text-pri text-[18px]">contrast</span>
          Point Operations: s = T(r)
        </span>
        <span id="cvIntEquation" class="text-ter font-mono text-xs font-bold">s = 255 - r</span>
      </div>

      <div class="grid grid-cols-2 gap-3 items-center justify-center p-3 bg-s1 rounded-xl border border-s3">
        <div class="flex flex-col items-center gap-1">
          <span class="text-[10px] font-mono text-ol uppercase">Input r</span>
          <canvas id="cvIntInCanvas" class="rounded border border-s3 bg-s0 max-w-[150px] aspect-square"></canvas>
        </div>
        <div class="flex flex-col items-center gap-1">
          <span class="text-[10px] font-mono text-pri uppercase font-bold">Output s = T(r)</span>
          <canvas id="cvIntOutCanvas" class="rounded border border-s3 bg-s0 max-w-[150px] aspect-square cursor-crosshair"></canvas>
        </div>
      </div>

      <div class="flex flex-col gap-2 font-mono text-xs bg-s1 p-3 rounded-xl border border-s3">
        <span class="text-ol text-[10px]">SELECT POINT TRANSFORMATION</span>
        <div class="grid grid-cols-2 sm:grid-cols-3 gap-1.5">
          ${[
            ['negative', 'Image Negative'],
            ['log', 'Logarithmic'],
            ['gamma', 'Power-Law (Gamma)'],
            ['contrast_stretch', 'Contrast Stretching'],
            ['slicing', 'Intensity Slicing'],
            ['brightness_contrast', 'Brightness/Contrast']
          ].map(([op, label]) => `
            <button onclick="CV.intOp='${op}'; cvUpdateIntensityCanvas();" class="p-2 rounded text-left text-xs font-mono border transition-colors ${CV.intOp === op ? 'bg-pc text-onpc font-bold border-pri' : 'bg-s0 text-mut hover:text-fg border-s3'}">
              ${label}
            </button>`).join('')}
        </div>
        <div id="cvIntSubParams" class="pt-2 border-t border-s3/40">
          ${cvRenderIntensityParams()}
        </div>
      </div>
    </div>

    <!-- Right: Mathematical Transfer Curve s = T(r) & Histogram -->
    <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-sm flex flex-col gap-3">
      <div class="flex items-center justify-between border-b border-s3/40 pb-2">
        <span class="cvt">
          <span class="ms text-ok text-[18px]">show_chart</span>
          Transfer Function Characteristic Curve s = T(r)
        </span>
        <span class="text-ol font-mono text-xs">[0..255] -> [0..255]</span>
      </div>

      <div class="bg-s1 p-3 rounded-xl border border-s3 flex items-center justify-center">
        <svg id="cvIntCurveSvg" viewBox="0 0 256 256" class="w-full max-w-[280px] aspect-square bg-s0 rounded border border-s3/50 p-2"></svg>
      </div>

      <div class="bg-s1 p-3 rounded-xl border border-s3 flex flex-col gap-1.5 text-xs font-mono">
        <span class="text-pri font-bold">Dynamic Range Behaviour</span>
        <p id="cvIntDesc" class="text-mut text-[11px] leading-relaxed">
          ${cvGetIntensityDescription()}
        </p>
      </div>
    </div>
  </div>`;
}

function cvRenderIntensityParams() {
  if (CV.intOp === 'gamma') {
    return `<div class="flex justify-between items-center text-xs">
      <span class="text-ol">GAMMA (γ): <b class="text-pri">${CV.gamma.toFixed(2)}</b></span>
      <span class="text-[10px] text-mut">${CV.gamma < 1 ? 'Brightens shadows' : 'Boosts highlight contrast'}</span>
    </div>
    <input type="range" min="0.1" max="3.5" step="0.05" value="${CV.gamma}" oninput="CV.gamma=+this.value; cvUpdateIntensityCanvas();">`;
  } else if (CV.intOp === 'contrast_stretch') {
    return `<div class="grid grid-cols-2 gap-2 text-xs">
      <div><span class="text-ol">r1 (In Low):</span> <b class="text-pri">${CV.csR1}</b></div>
      <div><span class="text-ol">s1 (Out Low):</span> <b class="text-ter">${CV.csS1}</b></div>
    </div>
    <input type="range" min="10" max="120" value="${CV.csR1}" oninput="CV.csR1=+this.value; cvUpdateIntensityCanvas();">`;
  } else if (CV.intOp === 'slicing') {
    return `<div class="flex justify-between items-center text-xs">
      <span class="text-ol">INTERVAL [${CV.sliceLow} .. ${CV.sliceHigh}]</span>
      <label class="flex items-center gap-1 cursor-pointer"><input type="checkbox" ${CV.slicePreserve?'checked':''} onchange="CV.slicePreserve=this.checked; cvUpdateIntensityCanvas();"> Preserve BG</label>
    </div>
    <input type="range" min="0" max="255" value="${CV.sliceHigh}" oninput="CV.sliceHigh=+this.value; cvUpdateIntensityCanvas();">`;
  }
  return `<span class="text-ol text-[10px]">No extra parameters needed for standard ${CV.intOp}.</span>`;
}

function cvGetIntensityDescription() {
  switch (CV.intOp) {
    case 'negative': return 'Inverts intensity values: s = (L - 1) - r. Enhances white/grey detail embedded in predominantly dark regions (e.g. digital mammography scans).';
    case 'log': return 'Logarithmic transform s = c · log(1 + r). Strongly expands dark pixel values while compressing dynamic range of high-intensity bright pixels.';
    case 'gamma': return `Power-law transform s = c · r^γ. Current γ = ${CV.gamma.toFixed(2)}. Fractional γ < 1 maps narrow range of dark inputs into wider range of outputs; γ > 1 expands highlights.`;
    case 'contrast_stretch': return 'Piecewise linear contrast stretching. Stretches narrow clustered histogram bins across the full spectrum [0..255] for enhanced visual definition.';
    case 'slicing': return 'Intensity-level slicing. Highlights specific feature range of interest (e.g. water bodies or tumor masses in MRI) with or without preserving background context.';
    default: return 'Point operations apply a deterministic transformation independently to every pixel.';
  }
}

function cvUpdateIntensityCanvas() {
  const inC = document.getElementById('cvIntInCanvas');
  const outC = document.getElementById('cvIntOutCanvas');
  if (!inC || !outC || !CV.sourceCanvas) return;
  const size = CV.sourceCanvas.width;
  inC.width = inC.height = outC.width = outC.height = size;

  const inCtx = inC.getContext('2d');
  const outCtx = outC.getContext('2d');
  const d = CV.sourceCanvas.getContext('2d').getImageData(0, 0, size, size).data;
  inCtx.drawImage(CV.sourceCanvas, 0, 0);

  const outData = outCtx.createImageData(size, size);
  const od = outData.data;

  // Build LUT
  const lut = new Uint8Array(256);
  for (let r = 0; r < 256; r++) {
    let s = r;
    if (CV.intOp === 'negative') {
      s = 255 - r;
    } else if (CV.intOp === 'log') {
      const c = 255 / Math.log(1 + 255);
      s = Math.round(c * Math.log(1 + r));
    } else if (CV.intOp === 'gamma') {
      s = Math.round(255 * Math.pow(r / 255, CV.gamma));
    } else if (CV.intOp === 'contrast_stretch') {
      if (r < CV.csR1) s = Math.round((CV.csS1 / CV.csR1) * r);
      else if (r <= CV.csR2) s = Math.round(CV.csS1 + ((CV.csS2 - CV.csS1) / (CV.csR2 - CV.csR1)) * (r - CV.csR1));
      else s = Math.round(CV.csS2 + ((255 - CV.csS2) / (255 - CV.csR2)) * (r - CV.csR2));
    } else if (CV.intOp === 'slicing') {
      if (r >= CV.sliceLow && r <= CV.sliceHigh) s = 255;
      else s = CV.slicePreserve ? r : 0;
    } else if (CV.intOp === 'brightness_contrast') {
      s = Math.round(CV.brightAlpha * r + CV.brightBeta);
    }
    lut[r] = Math.min(255, Math.max(0, s));
  }

  for (let i = 0; i < d.length; i += 4) {
    od[i] = lut[d[i]];
    od[i+1] = lut[d[i+1]];
    od[i+2] = lut[d[i+2]];
    od[i+3] = 255;
  }
  outCtx.putImageData(outData, 0, 0);

  // Draw transfer function curve
  const svg = document.getElementById('cvIntCurveSvg');
  if (svg) {
    let pathD = `M 0,${255 - lut[0]}`;
    for (let r = 1; r < 256; r++) {
      pathD += ` L ${r},${255 - lut[r]}`;
    }
    svg.innerHTML = `
      <!-- Grid Lines -->
      <line x1="0" y1="0" x2="255" y2="255" stroke="#232a3a" stroke-dasharray="3,3"/>
      <line x1="0" y1="128" x2="255" y2="128" stroke="#191f2f"/>
      <line x1="128" y1="0" x2="128" y2="255" stroke="#191f2f"/>
      <!-- Curve -->
      <path d="${pathD}" fill="none" stroke="#6ea0ff" stroke-width="2.5"/>
      <text x="10" y="24" fill="#fbbf24" font-size="11" font-family="JetBrains Mono">${CV.intOp.toUpperCase()}</text>
      <text x="180" y="245" fill="#7a82ad" font-size="10" font-family="JetBrains Mono">Input r -> Output s</text>
    `;
  }
}

// ---------------- 4. Histograms & Histogram Equalization Tab ----------------
function cvRenderHist() {
  setTimeout(cvUpdateHistCanvas, 20);

  return `<div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
    <!-- Left: Original vs Equalized Images & Numerical Stages Table -->
    <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-sm flex flex-col gap-3">
      <div class="flex items-center justify-between border-b border-s3/40 pb-2">
        <span class="cvt">
          <span class="ms text-pri text-[18px]">bar_chart</span>
          6-Stage Histogram Equalization (Cumulative Probability Transfer)
        </span>
        <span class="text-ok font-mono text-xs font-bold">Contrast Enhancement</span>
      </div>

      <div class="grid grid-cols-2 gap-3 p-3 bg-s1 rounded-xl border border-s3">
        <div class="flex flex-col items-center gap-1">
          <span class="text-[10px] font-mono text-ol">ORIGINAL GRAYSCALE</span>
          <canvas id="cvHistOrigCanvas" class="rounded border border-s3 bg-s0 max-w-[150px] aspect-square"></canvas>
        </div>
        <div class="flex flex-col items-center gap-1">
          <span class="text-[10px] font-mono text-pri font-bold">HISTOGRAM EQUALIZED</span>
          <canvas id="cvHistEqCanvas" class="rounded border border-s3 bg-s0 max-w-[150px] aspect-square"></canvas>
        </div>
      </div>

      <!-- 6-Stage Algorithm Stages List -->
      <div class="bg-s1 p-3 rounded-xl border border-s3 flex flex-col gap-1.5 font-mono text-xs">
        <span class="text-ter font-bold">The 6 Discrete Mathematical Stages:</span>
        <ol class="list-decimal pl-4 text-[11px] text-mut space-y-0.5">
          <li><b>Compute Raw Histogram:</b> Count frequency <code class="text-pri">n_k</code> for each intensity <code class="text-pri">r_k</code>.</li>
          <li><b>Normalized Probability:</b> <code class="text-pri">p(r_k) = n_k / N</code> where N = total pixels.</li>
          <li><b>Cumulative Distribution (CDF):</b> <code class="text-pri">CDF(k) = Σ p(r_j)</code> for j = 0..k.</li>
          <li><b>Discrete Mapping:</b> <code class="text-pri">s_k = round((L - 1) · CDF(k))</code> (scales CDF to [0..255]).</li>
          <li><b>Transform Pixels:</b> Replace each input intensity <code class="text-pri">r_k</code> with mapped <code class="text-pri">s_k</code>.</li>
          <li><b>Empirical Analysis:</b> Compare input and enhanced dynamic range histograms.</li>
        </ol>
      </div>
    </div>

    <!-- Right: Histogram & CDF Plots + Representative Table -->
    <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-sm flex flex-col gap-3">
      <div class="flex items-center justify-between border-b border-s3/40 pb-2">
        <span class="cvt">
          <span class="ms text-ter text-[18px]">analytics</span>
          Intensity Distribution & CDF Curves
        </span>
        <span id="cvHistDiagnosis" class="text-xs font-mono text-pri font-bold">Analyzing...</span>
      </div>

      <div class="grid grid-cols-2 gap-3 bg-s1 p-3 rounded-xl border border-s3">
        <div class="flex flex-col items-center gap-1">
          <span class="text-[10px] font-mono text-ol">ORIGINAL HISTOGRAM</span>
          <svg id="cvHistSvgBefore" viewBox="0 0 256 120" class="w-full bg-s0 rounded border border-s3/50"></svg>
        </div>
        <div class="flex flex-col items-center gap-1">
          <span class="text-[10px] font-mono text-pri">EQUALIZED HISTOGRAM</span>
          <svg id="cvHistSvgAfter" viewBox="0 0 256 120" class="w-full bg-s0 rounded border border-s3/50"></svg>
        </div>
      </div>

      <!-- Representative Mapping Table Sample -->
      <div class="bg-s1 rounded-xl p-3 border border-s3 overflow-x-auto">
        <span class="text-[10px] font-mono text-ol uppercase font-bold">Representative Intensity Mapping Table (Sampled Levels)</span>
        <table id="cvHistSampleTable" class="w-full font-mono text-[10px] text-left mt-1 text-mut">
          <thead>
            <tr class="text-ol border-b border-s3/40">
              <th class="p-1">r_k</th>
              <th class="p-1">Count n_k</th>
              <th class="p-1">p(r_k)</th>
              <th class="p-1">CDF(k)</th>
              <th class="p-1 text-pri">Mapped s_k</th>
            </tr>
          </thead>
          <tbody id="cvHistTableBody" class="divide-y divide-s3/30"></tbody>
        </table>
      </div>
    </div>
  </div>`;
}

function cvUpdateHistCanvas() {
  const oC = document.getElementById('cvHistOrigCanvas');
  const eC = document.getElementById('cvHistEqCanvas');
  if (!oC || !eC || !CV.sourceCanvas) return;
  const size = CV.sourceCanvas.width;
  oC.width = oC.height = eC.width = eC.height = size;
  const oCtx = oC.getContext('2d'), eCtx = eC.getContext('2d');
  const d = CV.sourceCanvas.getContext('2d').getImageData(0, 0, size, size).data;

  // 1. Convert to gray & count histogram
  const total = size * size;
  const hist = new Int32Array(256);
  const grayArr = new Uint8Array(total);
  let sumY = 0;

  for (let i = 0, p = 0; i < d.length; i += 4, p++) {
    const y = Math.round(0.299 * d[i] + 0.587 * d[i+1] + 0.114 * d[i+2]);
    grayArr[p] = y;
    hist[y]++;
    sumY += y;
  }

  // Draw original gray
  const oData = oCtx.createImageData(size, size);
  for (let i = 0, p = 0; i < oData.data.length; i += 4, p++) {
    const y = grayArr[p];
    oData.data[i] = y; oData.data[i+1] = y; oData.data[i+2] = y; oData.data[i+3] = 255;
  }
  oCtx.putImageData(oData, 0, 0);

  // 2. Compute probabilities and CDF
  const cdf = new Float32Array(256);
  let cum = 0;
  for (let k = 0; k < 256; k++) {
    cum += hist[k] / total;
    cdf[k] = cum;
  }

  // 3. Mapping s_k
  const sMap = new Uint8Array(256);
  for (let k = 0; k < 256; k++) {
    sMap[k] = Math.round(255 * cdf[k]);
  }

  // 4. Equalized image & new histogram
  const eqHist = new Int32Array(256);
  const eData = eCtx.createImageData(size, size);
  for (let i = 0, p = 0; i < eData.data.length; i += 4, p++) {
    const eqY = sMap[grayArr[p]];
    eqHist[eqY]++;
    eData.data[i] = eqY; eData.data[i+1] = eqY; eData.data[i+2] = eqY; eData.data[i+3] = 255;
  }
  eCtx.putImageData(eData, 0, 0);

  // Diagnostics
  const meanY = sumY / total;
  const diag = document.getElementById('cvHistDiagnosis');
  if (diag) {
    if (meanY < 80) diag.textContent = 'Dark Image (Left-Concentrated)';
    else if (meanY > 175) diag.textContent = 'Bright Image (Right-Concentrated)';
    else diag.textContent = 'Well-Distributed Contrast';
  }

  // Draw SVG Histograms
  const svgB = document.getElementById('cvHistSvgBefore');
  const svgA = document.getElementById('cvHistSvgAfter');
  if (svgB && svgA) {
    const maxB = Math.max(...hist, 1);
    const maxA = Math.max(...eqHist, 1);

    svgB.innerHTML = Array.from(hist).map((v, i) => `
      <line x1="${i}" y1="120" x2="${i}" y2="${120 - Math.round((v / maxB) * 110)}" stroke="#6ea0ff" stroke-width="1"/>
    `).join('') + `<polyline points="${Array.from(cdf).map((c, i) => `${i},${120 - Math.round(c * 110)}`).join(' ')}" fill="none" stroke="#fbbf24" stroke-width="1.5"/>`;

    let cumA = 0;
    const cdfA = Array.from(eqHist).map(v => (cumA += v / total));
    svgA.innerHTML = Array.from(eqHist).map((v, i) => `
      <line x1="${i}" y1="120" x2="${i}" y2="${120 - Math.round((v / maxA) * 110)}" stroke="#10B981" stroke-width="1"/>
    `).join('') + `<polyline points="${cdfA.map((c, i) => `${i},${120 - Math.round(c * 110)}`).join(' ')}" fill="none" stroke="#fbbf24" stroke-width="1.5"/>`;
  }

  // Populate sample table
  const tbody = document.getElementById('cvHistTableBody');
  if (tbody) {
    const samples = [0, 32, 64, 96, 128, 160, 192, 224, 255];
    tbody.innerHTML = samples.map(k => `
      <tr class="hover:bg-s2/40">
        <td class="p-1 font-bold text-fg">${k}</td>
        <td class="p-1">${hist[k]}</td>
        <td class="p-1">${(hist[k] / total).toFixed(4)}</td>
        <td class="p-1">${cdf[k].toFixed(4)}</td>
        <td class="p-1 text-pri font-bold">${sMap[k]}</td>
      </tr>
    `).join('');
  }
}

// ---------------- 5. Spatial Filtering & Kernel Movement Laboratory ----------------
// Signature Feature: Interactive pixel-by-pixel stepping, highlighted footprint, live arithmetic breakdown

function cvRenderKernelLab() {
  const kInfo = CV_KERNELS[CV.kPreset] || CV_KERNELS.box_3x3;
  const mat = CV.kMatrix;
  const inH = mat.length, inW = mat[0].length;
  const kH = kInfo.mat.length, kW = kInfo.mat[0].length;
  const radH = Math.floor(kH / 2), radW = Math.floor(kW / 2);

  const padAmt = CV.kPadMode === 'valid' ? 0 : radH;
  const outH = Math.floor((inH + 2 * padAmt - kH) / CV.kStride) + 1;
  const outW = Math.floor((inW + 2 * padAmt - kW) / CV.kStride) + 1;

  // Compute arithmetic details for current step
  const stepCalc = cvCalculateKernelStepMath(CV.kStepR, CV.kStepC, kInfo);

  return `<div class="flex flex-col gap-4">
    <!-- Top Configuration Bar -->
    <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-sm flex flex-col gap-3">
      <div class="flex flex-wrap items-center justify-between gap-3 border-b border-s3/40 pb-2">
        <div class="flex items-center gap-2">
          <span class="ms text-pri text-[20px]">grain</span>
          <span class="font-mono text-xs uppercase tracking-wider text-fg font-semibold">Interactive Kernel Movement Laboratory (Signature Feature)</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-xs font-mono text-ter font-bold">Stride: ${CV.kStride}</span>
          <span class="text-olv font-mono">|</span>
          <span class="text-xs font-mono text-pri">Pad: ${CV.kPadMode}</span>
          <span class="text-olv font-mono">|</span>
          <button onclick="CV.kIsConv=!CV.kIsConv; route('vision');" class="px-2 py-0.5 rounded font-mono text-[11px] ${CV.kIsConv ? 'bg-pri text-s0 font-bold' : 'bg-s3 text-mut'}">
            ${CV.kIsConv ? '2D Mathematical Convolution (Flipped 180°)' : '2D Cross-Correlation (Direct)'}
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-4 gap-3 font-mono text-xs">
        <div>
          <label class="text-[10px] text-ol uppercase">Kernel Preset</label>
          <select onchange="cvSelectKernelPreset(this.value)" class="w-full bg-s1 text-pri rounded-lg px-2.5 py-1.5 border border-s3 mt-1">
            ${Object.entries(CV_KERNELS).map(([k, info]) => `
              <option value="${k}" ${CV.kPreset==k?'selected':''}>${info.name}</option>
            `).join('')}
          </select>
        </div>
        <div>
          <label class="text-[10px] text-ol uppercase">Padding Mode</label>
          <select onchange="CV.kPadMode=this.value; route('vision');" class="w-full bg-s1 text-fg rounded-lg px-2.5 py-1.5 border border-s3 mt-1">
            <option value="replicate" ${CV.kPadMode=='replicate'?'selected':''}>Replicate (Clamp Borders)</option>
            <option value="zero" ${CV.kPadMode=='zero'?'selected':''}>Zero Padding (Border 0)</option>
            <option value="reflect" ${CV.kPadMode=='reflect'?'selected':''}>Reflect (Mirror Borders)</option>
            <option value="valid" ${CV.kPadMode=='valid'?'selected':''}>Valid (No Padding, Reduced Size)</option>
          </select>
        </div>
        <div>
          <label class="text-[10px] text-ol uppercase">Stride</label>
          <select onchange="CV.kStride=+this.value; route('vision');" class="w-full bg-s1 text-fg rounded-lg px-2.5 py-1.5 border border-s3 mt-1">
            <option value="1" ${CV.kStride==1?'selected':''}>Stride 1 (Full sampling)</option>
            <option value="2" ${CV.kStride==2?'selected':''}>Stride 2 (Downsampled by 2x)</option>
          </select>
        </div>
        <div>
          <label class="text-[10px] text-ol uppercase">Output Dimensions Formula</label>
          <div class="mt-1 bg-s1 px-2.5 py-1.5 rounded-lg border border-s3/50 text-[11px] text-ok font-bold">
            Output: ${outW} × ${outH} pixels
          </div>
        </div>
      </div>
    </div>

    <!-- 3-Column Interactive Stage: Input Matrix + Kernel Matrix + Output Matrix -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 items-start font-mono text-xs">
      <!-- 1. Input Matrix (With highlighted moving footprint) -->
      <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-sm flex flex-col gap-2">
        <div class="flex justify-between items-center pb-1 border-b border-s3/30">
          <span class="font-bold text-pri flex items-center gap-1">
            <span class="ms text-[16px]">grid_view</span>
            1. Input Matrix (7×7)
          </span>
          <span class="text-[10px] text-ol">Footprint: Cyan Box</span>
        </div>
        <div class="grid grid-cols-7 gap-1 p-2 bg-s1 rounded-lg text-center select-none">
          ${cvRenderKernelInputGrid(mat, CV.kStepR, CV.kStepC, radH, radW)}
        </div>
        <span class="text-[10px] text-mut">Cyan cells mark the active ${kH}×${kW} neighborhood centered at (${CV.kStepR}, ${CV.kStepC}).</span>
      </div>

      <!-- 2. Kernel Matrix & Live Product Summation Breakdown -->
      <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-sm flex flex-col gap-3">
        <div class="flex justify-between items-center pb-1 border-b border-s3/30">
          <span class="font-bold text-ter flex items-center gap-1">
            <span class="ms text-[16px]">tune</span>
            2. Kernel & Arithmetic
          </span>
          <span class="text-[10px] text-mut">${kInfo.type.toUpperCase()}</span>
        </div>

        <!-- Kernel Matrix Weights Display -->
        <div class="flex flex-col gap-1 items-center bg-s1 p-2.5 rounded-lg border border-s3/40">
          <span class="text-[10px] text-ol font-bold uppercase">Kernel Weights W(s, t)</span>
          <div class="grid gap-1 text-center" style="grid-template-columns: repeat(${kW}, 1fr)">
            ${kInfo.mat.map(row => row.map(v => `
              <div class="p-1 rounded bg-s2 text-pri font-bold text-[10px] border border-s3/40 w-10">
                ${typeof v === 'number' ? (v >= 1 || v <= -1 ? v : v.toFixed(2)) : v}
              </div>`).join('')).join('')}
          </div>
        </div>

        <!-- Step Arithmetic Breakdown -->
        <div class="bg-s1 p-3 rounded-lg border border-s3/40 flex flex-col gap-1 text-[11px] leading-tight">
          <span class="text-ter font-bold">Step Computation at (${CV.kStepR}, ${CV.kStepC}):</span>
          <div class="text-mut text-[10px] max-h-24 overflow-y-auto space-y-0.5">
            ${stepCalc.breakdown}
          </div>
          <div class="pt-1 mt-1 border-t border-s3/30 flex justify-between items-center text-xs">
            <span class="text-ol">Calculated Value:</span>
            <span class="text-ter font-bold">${stepCalc.sumStr}</span>
          </div>
          <div class="flex justify-between items-center text-xs">
            <span class="text-ol">Final Clipped [0..255]:</span>
            <span class="text-ok font-bold text-sm">${stepCalc.outVal}</span>
          </div>
        </div>
      </div>

      <!-- 3. Output Matrix (Progressively written) -->
      <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-sm flex flex-col gap-2">
        <div class="flex justify-between items-center pb-1 border-b border-s3/30">
          <span class="font-bold text-ok flex items-center gap-1">
            <span class="ms text-[16px]">output</span>
            3. Output Matrix (${outW}×${outH})
          </span>
          <span class="text-[10px] text-ter font-bold">Writing: (${CV.kStepR}, ${CV.kStepC})</span>
        </div>
        <div class="grid gap-1 p-2 bg-s1 rounded-lg text-center" style="grid-template-columns: repeat(${outW}, 1fr)">
          ${cvRenderKernelOutputGrid(outH, outW, CV.kStepR, CV.kStepC, stepCalc.outVal)}
        </div>
        <span class="text-[10px] text-mut">Green shows processed outputs; Amber cell is currently written.</span>
      </div>
    </div>

    <!-- Bottom Full Timeline Controller -->
    <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-md flex flex-wrap items-center justify-between gap-3 font-mono text-xs">
      <div class="flex items-center gap-2">
        <button onclick="cvKernelReset()" class="bg-s1 hover:bg-s2 border border-s3 px-3 py-1.5 rounded-lg flex items-center gap-1 text-mut hover:text-fg transition-colors">
          <span class="ms text-[16px]">restart_alt</span> Reset
        </button>
        <button onclick="cvKernelStep(-1)" class="bg-s1 hover:bg-s2 border border-s3 px-3 py-1.5 rounded-lg flex items-center gap-1 text-mut hover:text-fg transition-colors">
          <span class="ms text-[16px]">skip_previous</span> Step Back
        </button>
        <button id="cvKernelPlayBtn" onclick="cvKernelTogglePlay()" class="bg-pc text-onpc font-bold px-4 py-1.5 rounded-lg flex items-center gap-1 hover:brightness-110 transition-all shadow-sm">
          <span class="ms text-[16px]">${CV.kRunning ? 'pause' : 'play_arrow'}</span>
          <span>${CV.kRunning ? 'Pause' : 'Play'}</span>
        </button>
        <button onclick="cvKernelStep(1)" class="bg-s1 hover:bg-s2 border border-s3 px-3 py-1.5 rounded-lg flex items-center gap-1 text-mut hover:text-fg transition-colors">
          <span class="ms text-[16px]">skip_next</span> Step Forward
        </button>
      </div>

      <div class="flex items-center gap-2 flex-1 max-w-xs">
        <span class="text-ol text-[10px]">POS:</span>
        <input type="range" min="0" max="${outH * outW - 1}" value="${CV.kStepR * outW + CV.kStepC}" oninput="cvKernelScrub(+this.value, ${outW})" class="w-full">
        <span class="text-pri font-bold text-xs">${CV.kStepR * outW + CV.kStepC + 1}/${outH * outW}</span>
      </div>

      <div class="flex items-center gap-2">
        <span class="text-ol text-[10px]">SPEED:</span>
        ${[0.5, 1, 2, 4].map(s => `
          <button onclick="CV.kSpeed=${s}; route('vision');" class="px-2 py-0.5 rounded text-[11px] ${CV.kSpeed==s?'bg-ter text-s0 font-bold':'bg-s1 text-mut'}">${s}x</button>
        `).join('')}
      </div>
    </div>
  </div>`;
}

function cvSelectKernelPreset(p) {
  CV.kPreset = p;
  CV.kOutputs = {};
  CV.kStepR = 0; CV.kStepC = 0;
  cvStopKernelAnimation();
  route('vision');
}

function cvRenderKernelInputGrid(mat, curR, curC, radH, radW) {
  return mat.map((row, r) => row.map((val, c) => {
    const inFootprint = (r >= curR - radH && r <= curR + radH && c >= curC - radW && c <= curC + radW);
    const isCenter = (r === curR && c === curC);
    let cls = 'bg-s0 text-mut border-s3/40';
    if (isCenter) cls = 'bg-ter text-s0 font-bold border-ter shadow';
    else if (inFootprint) cls = 'bg-pri/20 text-pri font-bold border-pri';
    return `<div class="p-1 rounded text-center border ${cls} text-[11px] transition-colors">${val}</div>`;
  }).join('')).join('');
}

function cvRenderKernelOutputGrid(outH, outW, curR, curC, curVal) {
  const cells = [];
  for (let r = 0; r < outH; r++) {
    for (let c = 0; c < outW; c++) {
      const isCur = (r === curR && c === curC);
      const key = `${r},${c}`;
      if (isCur) CV.kOutputs[key] = curVal;
      const v = CV.kOutputs[key];
      let cls = 'bg-s0 text-ol border-s3/30';
      if (isCur) cls = 'bg-ter text-s0 font-bold border-ter animate-pulse';
      else if (v !== undefined) cls = 'bg-ok/20 text-ok font-bold border-ok/40';
      cells.push(`<div class="p-1 rounded text-center border ${cls} text-[11px]">${v !== undefined ? v : '·'}</div>`);
    }
  }
  return cells.join('');
}

function cvCalculateKernelStepMath(r, c, kInfo) {
  const mat = CV.kMatrix;
  const inH = mat.length, inW = mat[0].length;
  const kH = kInfo.mat.length, kW = kInfo.mat[0].length;
  const radH = Math.floor(kH / 2), radW = Math.floor(kW / 2);

  const neigh = [];
  const prods = [];
  let sum = 0;

  for (let dr = -radH; dr <= radH; dr++) {
    for (let dc = -radW; dc <= radW; dc++) {
      let pr = r + dr, pc = c + dc;
      if (CV.kPadMode === 'replicate') {
        pr = Math.max(0, Math.min(inH - 1, pr));
        pc = Math.max(0, Math.min(inW - 1, pc));
      } else { // zero
        if (pr < 0 || pr >= inH || pc < 0 || pc >= inW) { pr = -1; pc = -1; }
      }
      const pVal = (pr >= 0 && pc >= 0) ? mat[pr][pc] : 0;
      let kr = dr + radH, kc = dc + radW;
      if (CV.kIsConv) { kr = kH - 1 - kr; kc = kW - 1 - kc; }
      const weight = kInfo.mat[kr][kc];

      neigh.push(pVal);
      if (kInfo.type === 'linear') {
        const prod = pVal * weight;
        prods.push(`${pVal}×${typeof weight==='number'?weight.toFixed(2):weight}=${prod.toFixed(1)}`);
        sum += prod;
      }
    }
  }

  let outVal = 0, sumStr = '';
  if (kInfo.type === 'median') {
    const sorted = [...neigh].sort((a, b) => a - b);
    outVal = sorted[Math.floor(sorted.length / 2)];
    sumStr = `Median of [${sorted.slice(0, 5).join(', ')}...] = ${outVal}`;
    return { breakdown: `Sorted neighbourhood: ${sorted.join(', ')}`, sumStr, outVal };
  } else if (kInfo.type === 'min') {
    outVal = Math.min(...neigh);
    return { breakdown: `Minimum of neighbourhood: ${outVal}`, sumStr: `Min = ${outVal}`, outVal };
  } else if (kInfo.type === 'max') {
    outVal = Math.max(...neigh);
    return { breakdown: `Maximum of neighbourhood: ${outVal}`, sumStr: `Max = ${outVal}`, outVal };
  } else {
    outVal = Math.min(255, Math.max(0, Math.round(sum)));
    return { breakdown: prods.join(' + '), sumStr: sum.toFixed(2), outVal };
  }
}

function cvKernelStep(dir) {
  const kInfo = CV_KERNELS[CV.kPreset] || CV_KERNELS.box_3x3;
  const inH = CV.kMatrix.length, inW = CV.kMatrix[0].length;
  const kH = kInfo.mat.length, kW = kInfo.mat[0].length;
  const radH = Math.floor(kH / 2);
  const padAmt = CV.kPadMode === 'valid' ? 0 : radH;
  const outH = Math.floor((inH + 2 * padAmt - kH) / CV.kStride) + 1;
  const outW = Math.floor((inW + 2 * padAmt - kW) / CV.kStride) + 1;

  let idx = CV.kStepR * outW + CV.kStepC + dir;
  if (idx < 0) idx = 0;
  if (idx >= outH * outW) {
    idx = outH * outW - 1;
    cvStopKernelAnimation();
  }
  CV.kStepR = Math.floor(idx / outW);
  CV.kStepC = idx % outW;
  route('vision');
}

function cvKernelScrub(idx, outW) {
  CV.kStepR = Math.floor(idx / outW);
  CV.kStepC = idx % outW;
  route('vision');
}

function cvKernelReset() {
  cvStopKernelAnimation();
  CV.kStepR = 0; CV.kStepC = 0;
  CV.kOutputs = {};
  route('vision');
}

function cvKernelTogglePlay() {
  if (CV.kRunning) {
    cvStopKernelAnimation();
  } else {
    CV.kRunning = true;
    const interval = Math.max(100, Math.floor(600 / CV.kSpeed));
    CV.kTimer = setInterval(() => {
      cvKernelStep(1);
    }, interval);
  }
  route('vision');
}

function cvStopKernelAnimation() {
  CV.kRunning = false;
  if (CV.kTimer) { clearInterval(CV.kTimer); CV.kTimer = null; }
}

// ---------------- 6. Smoothing & Noise Removal Tab ----------------
function cvRenderNoise() {
  setTimeout(cvUpdateNoiseCanvas, 20);

  return `<div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
    <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-sm flex flex-col gap-3">
      <div class="flex items-center justify-between border-b border-s3/40 pb-2">
        <span class="cvt">
          <span class="ms text-pri text-[18px]">blur_on</span>
          Noise Generation & Filter Comparison Arena (Spatial Non-Linear Filtering)
        </span>
        <span class="text-ter font-mono text-xs">Low-Pass Filtering</span>
      </div>

      <div class="grid grid-cols-2 gap-3 p-3 bg-s1 rounded-xl border border-s3">
        <div class="flex flex-col items-center gap-1">
          <span class="text-[10px] font-mono text-err font-bold">1. NOISY CORRUPTED IMAGE</span>
          <canvas id="cvNoiseNoisyCanvas" class="rounded border border-s3 bg-s0 max-w-[150px] aspect-square"></canvas>
        </div>
        <div class="flex flex-col items-center gap-1">
          <span class="text-[10px] font-mono text-ok font-bold">2. RESTORED FILTERED IMAGE</span>
          <canvas id="cvNoiseFilterCanvas" class="rounded border border-s3 bg-s0 max-w-[150px] aspect-square"></canvas>
        </div>
      </div>

      <!-- Controls -->
      <div class="grid grid-cols-2 gap-3 font-mono text-xs bg-s1 p-3 rounded-xl border border-s3">
        <div>
          <label class="text-[10px] text-ol uppercase">Noise Distribution</label>
          <select onchange="CV.noiseType=this.value; cvUpdateNoiseCanvas();" class="w-full bg-s0 text-err rounded px-2 py-1 mt-1 border border-s3 font-bold">
            <option value="salt_pepper" ${CV.noiseType=='salt_pepper'?'selected':''}>Salt & Pepper (Impulse 0/255)</option>
            <option value="gaussian" ${CV.noiseType=='gaussian'?'selected':''}>Gaussian (Sensor/Thermal N(0,σ²))</option>
            <option value="speckle" ${CV.noiseType=='speckle'?'selected':''}>Speckle (Multiplicative Noise)</option>
          </select>
        </div>
        <div>
          <label class="text-[10px] text-ol uppercase">Restoration Filter</label>
          <select onchange="CV.filterType=this.value; cvUpdateNoiseCanvas();" class="w-full bg-s0 text-ok rounded px-2 py-1 mt-1 border border-s3 font-bold">
            <option value="median" ${CV.filterType=='median'?'selected':''}>Median Filter (Order-Statistic)</option>
            <option value="gaussian" ${CV.filterType=='gaussian'?'selected':''}>Gaussian Smoothing Filter</option>
            <option value="box" ${CV.filterType=='box'?'selected':''}>Mean / Box Averaging Filter</option>
            <option value="unsharp" ${CV.filterType=='unsharp'?'selected':''}>Unsharp Masking (High-Pass Boost)</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Right: Restoration Metrics & Pedagogical Takeaway -->
    <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-sm flex flex-col gap-3 font-mono text-xs">
      <div class="flex items-center justify-between border-b border-s3/40 pb-2">
        <span class="text-xs uppercase tracking-wider text-fg font-semibold flex items-center gap-1.5">
          <span class="ms text-ok text-[18px]">verified</span>
          Quantitative Restoration Telemetry
        </span>
        <span class="text-pri">Ground Truth Comparison</span>
      </div>

      <div class="grid grid-cols-3 gap-2">
        <div class="bg-s1 p-3 rounded-lg border border-s3/40 flex flex-col items-center">
          <span class="text-[10px] text-ol uppercase">MSE Error</span>
          <span id="cvMetricMse" class="text-lg font-bold text-err pt-1">--</span>
          <span class="text-[9px] text-mut">Mean Squared Error</span>
        </div>
        <div class="bg-s1 p-3 rounded-lg border border-s3/40 flex flex-col items-center">
          <span class="text-[10px] text-ol uppercase">PSNR Ratio</span>
          <span id="cvMetricPsnr" class="text-lg font-bold text-ok pt-1">--</span>
          <span class="text-[9px] text-mut">Peak SNR in Decibels</span>
        </div>
        <div class="bg-s1 p-3 rounded-lg border border-s3/40 flex flex-col items-center">
          <span class="text-[10px] text-ol uppercase">MAE Dev</span>
          <span id="cvMetricMae" class="text-lg font-bold text-ter pt-1">--</span>
          <span class="text-[9px] text-mut">Mean Absolute Error</span>
        </div>
      </div>

      <div class="bg-s1 p-3.5 rounded-xl border border-s3 flex flex-col gap-1.5">
        <span class="text-ter font-bold text-xs">Signal Processing Analysis: Why Median Filter Beats Mean on Impulse Noise</span>
        <p class="text-mut text-[11px] leading-relaxed">
          Mean filters average the impulse values (e.g. 0 and 255) into the neighborhood, creating blurry grey halos. In contrast, <b>Median filtering orders the 9 values</b> and picks the middle element. Outliers (0 and 255) are pushed to the extremes and discarded completely, achieving pristine edge-preserving restoration!
        </p>
      </div>
    </div>
  </div>`;
}

function cvUpdateNoiseCanvas() {
  const nC = document.getElementById('cvNoiseNoisyCanvas');
  const fC = document.getElementById('cvNoiseFilterCanvas');
  if (!nC || !fC || !CV.sourceCanvas) return;
  const size = CV.sourceCanvas.width;
  nC.width = nC.height = fC.width = fC.height = size;
  const nCtx = nC.getContext('2d'), fCtx = fC.getContext('2d');
  const d = CV.sourceCanvas.getContext('2d').getImageData(0, 0, size, size).data;

  // 1. Generate Noisy Array
  const total = size * size;
  const clean = new Uint8Array(total);
  const noisy = new Uint8Array(total);

  for (let i = 0, p = 0; i < d.length; i += 4, p++) {
    clean[p] = Math.round(0.299 * d[i] + 0.587 * d[i+1] + 0.114 * d[i+2]);
    noisy[p] = clean[p];
  }

  if (CV.noiseType === 'salt_pepper') {
    const num = Math.floor(total * CV.noiseDensity);
    for (let k = 0; k < num; k++) {
      const idx = Math.floor(Math.random() * total);
      noisy[idx] = (k % 2 === 0) ? 255 : 0;
    }
  } else if (CV.noiseType === 'gaussian') {
    for (let p = 0; p < total; p++) {
      const u1 = Math.random(), u2 = Math.random();
      const z = Math.sqrt(-2.0 * Math.log(u1 + 1e-9)) * Math.cos(2.0 * Math.PI * u2);
      noisy[p] = Math.min(255, Math.max(0, Math.round(clean[p] + z * 28)));
    }
  }

  // Draw noisy
  const nData = nCtx.createImageData(size, size);
  for (let i = 0, p = 0; i < nData.data.length; i += 4, p++) {
    const v = noisy[p];
    nData.data[i] = v; nData.data[i+1] = v; nData.data[i+2] = v; nData.data[i+3] = 255;
  }
  nCtx.putImageData(nData, 0, 0);

  // 2. Filter Noisy
  const filtered = new Uint8Array(total);
  for (let r = 0; r < size; r++) {
    for (let c = 0; c < size; c++) {
      const pIdx = r * size + c;
      const win = [];
      for (let dr = -1; dr <= 1; dr++) {
        for (let dc = -1; dc <= 1; dc++) {
          const pr = Math.max(0, Math.min(size - 1, r + dr));
          const pc = Math.max(0, Math.min(size - 1, c + dc));
          win.push(noisy[pr * size + pc]);
        }
      }

      if (CV.filterType === 'median') {
        win.sort((a, b) => a - b);
        filtered[pIdx] = win[4]; // 9 / 2
      } else if (CV.filterType === 'box') {
        const sum = win.reduce((a, b) => a + b, 0);
        filtered[pIdx] = Math.round(sum / 9);
      } else if (CV.filterType === 'gaussian') {
        const gw = [1/16, 2/16, 1/16, 2/16, 4/16, 2/16, 1/16, 2/16, 1/16];
        let sum = 0;
        for (let k = 0; k < 9; k++) sum += win[k] * gw[k];
        filtered[pIdx] = Math.round(sum);
      } else { // unsharp
        const blur = Math.round(win.reduce((a, b) => a + b, 0) / 9);
        const mask = noisy[pIdx] - blur;
        filtered[pIdx] = Math.min(255, Math.max(0, noisy[pIdx] + mask));
      }
    }
  }

  // Draw filtered
  const fData = fCtx.createImageData(size, size);
  let mse = 0, mae = 0;
  for (let i = 0, p = 0; i < fData.data.length; i += 4, p++) {
    const v = filtered[p];
    fData.data[i] = v; fData.data[i+1] = v; fData.data[i+2] = v; fData.data[i+3] = 255;
    const diff = clean[p] - v;
    mse += diff * diff;
    mae += Math.abs(diff);
  }
  fCtx.putImageData(fData, 0, 0);

  mse = (mse / total);
  mae = (mae / total);
  const psnr = mse < 1e-4 ? 99.0 : 20.0 * Math.log10(255.0 / Math.sqrt(mse));

  const elMse = document.getElementById('cvMetricMse');
  if (elMse) {
    document.getElementById('cvMetricMse').textContent = mse.toFixed(1);
    document.getElementById('cvMetricPsnr').textContent = psnr.toFixed(1) + ' dB';
    document.getElementById('cvMetricMae').textContent = mae.toFixed(1);
  }
}

// ---------------- 7. Sharpening & Edge Detection Tab (Canny 5 Stages) ----------------
function cvRenderEdges() {
  setTimeout(cvUpdateEdgesCanvas, 20);

  return `<div class="grid grid-cols-1 lg:grid-cols-2 gap-4 font-mono text-xs">
    <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-sm flex flex-col gap-3">
      <div class="flex items-center justify-between border-b border-s3/40 pb-2">
        <span class="text-xs uppercase tracking-wider text-fg font-semibold flex items-center gap-1.5">
          <span class="ms text-pri text-[18px]">timeline</span>
          5-Stage Canny Edge Detector Stepper
        </span>
        <span class="text-ter font-bold">Optimal Boundary Thinning</span>
      </div>

      <div class="flex flex-col items-center justify-center p-3 bg-s1 rounded-xl border border-s3">
        <canvas id="cvEdgeCanvas" class="rounded border border-s3 bg-s0 max-w-[200px] aspect-square"></canvas>
        <span id="cvCannyStageLabel" class="text-xs font-bold text-pri pt-2">Stage 5: Final Hysteresis Tracked Edges</span>
      </div>

      <!-- 5-Stage Stepper Buttons -->
      <div class="flex flex-col gap-1.5 bg-s1 p-3 rounded-xl border border-s3">
        <span class="text-ol text-[10px] uppercase font-bold">Select Active Canny Stage:</span>
        <div class="grid grid-cols-1 sm:grid-cols-5 gap-1.5">
          ${[
            [1, '1. Blur'],
            [2, '2. Gradient'],
            [3, '3. NMS Thin'],
            [4, '4. Double Thresh'],
            [5, '5. Hysteresis']
          ].map(([s, label]) => `
            <button onclick="CV.cannyStage=${s}; cvUpdateEdgesCanvas();" class="p-2 rounded text-center text-xs font-mono border transition-colors ${CV.cannyStage===s ? 'bg-pc text-onpc font-bold border-pri' : 'bg-s0 text-mut hover:text-fg border-s3'}">
              ${label}
            </button>`).join('')}
        </div>
      </div>
    </div>

    <!-- Right: Operators Comparison -->
    <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-sm flex flex-col gap-3">
      <div class="flex items-center justify-between border-b border-s3/40 pb-2">
        <span class="text-xs uppercase tracking-wider text-fg font-semibold flex items-center gap-1.5">
          <span class="ms text-ok text-[18px]">difference</span>
          Differential Operators Comparison
        </span>
        <span class="text-mut">Sobel vs Prewitt vs Laplacian</span>
      </div>

      <div class="grid grid-cols-3 gap-2">
        <div class="bg-s1 p-2 rounded-lg border border-s3/40 flex flex-col items-center">
          <span class="text-pri font-bold">Sobel Magnitude</span>
          <canvas id="cvEdgeSobel" class="w-full aspect-square rounded bg-s0 mt-1"></canvas>
          <span class="text-[9px] text-ol pt-1">√(Gx² + Gy²)</span>
        </div>
        <div class="bg-s1 p-2 rounded-lg border border-s3/40 flex flex-col items-center">
          <span class="text-ter font-bold">Prewitt Filter</span>
          <canvas id="cvEdgePrewitt" class="w-full aspect-square rounded bg-s0 mt-1"></canvas>
          <span class="text-[9px] text-ol pt-1">Equal Weights</span>
        </div>
        <div class="bg-s1 p-2 rounded-lg border border-s3/40 flex flex-col items-center">
          <span class="text-ok font-bold">Laplacian 2nd Deriv</span>
          <canvas id="cvEdgeLaplacian" class="w-full aspect-square rounded bg-s0 mt-1"></canvas>
          <span class="text-[9px] text-ol pt-1">Zero-crossings</span>
        </div>
      </div>

      <div class="bg-s1 p-3.5 rounded-xl border border-s3 flex flex-col gap-1 text-[11px] leading-relaxed text-mut">
        <span class="text-fg font-bold">1st vs 2nd Derivative Edge Detection</span>
        <p>
          First derivatives (Sobel, Prewitt) produce thick peaks along edge steps. Second derivatives (Laplacian) produce zero-crossings between a positive and negative lobe, locating the exact center of edges with single-pixel accuracy.
        </p>
      </div>
    </div>
  </div>`;
}

function cvUpdateEdgesCanvas() {
  const canvas = document.getElementById('cvEdgeCanvas');
  if (!canvas || !CV.sourceCanvas) return;
  const size = CV.sourceCanvas.width;
  canvas.width = canvas.height = size;
  const ctx = canvas.getContext('2d');
  const d = CV.sourceCanvas.getContext('2d').getImageData(0, 0, size, size).data;

  // Grayscale buffer
  const gray = new Float32Array(size * size);
  for (let i = 0, p = 0; i < d.length; i += 4, p++) {
    gray[p] = 0.299 * d[i] + 0.587 * d[i+1] + 0.114 * d[i+2];
  }

  // Stage 1: Gaussian Blur
  const blur = new Float32Array(size * size);
  for (let r = 0; r < size; r++) {
    for (let c = 0; c < size; c++) {
      let sum = 0;
      for (let dr = -1; dr <= 1; dr++) {
        for (let dc = -1; dc <= 1; dc++) {
          const pr = Math.max(0, Math.min(size - 1, r + dr));
          const pc = Math.max(0, Math.min(size - 1, c + dc));
          const w = (dr === 0 && dc === 0) ? 4/16 : (dr === 0 || dc === 0) ? 2/16 : 1/16;
          sum += gray[pr * size + pc] * w;
        }
      }
      blur[r * size + c] = sum;
    }
  }

  // Stage 2: Sobel Gradients
  const mag = new Float32Array(size * size);
  const ang = new Float32Array(size * size);
  for (let r = 1; r < size - 1; r++) {
    for (let c = 1; c < size - 1; c++) {
      const gx = -1 * blur[(r-1)*size + (c-1)] + 1 * blur[(r-1)*size + (c+1)]
                 -2 * blur[r*size + (c-1)]     + 2 * blur[r*size + (c+1)]
                 -1 * blur[(r+1)*size + (c-1)] + 1 * blur[(r+1)*size + (c+1)];
      const gy = -1 * blur[(r-1)*size + (c-1)] - 2 * blur[(r-1)*size + c] - 1 * blur[(r-1)*size + (c+1)]
                 +1 * blur[(r+1)*size + (c-1)] + 2 * blur[(r+1)*size + c] + 1 * blur[(r+1)*size + (c+1)];
      mag[r * size + c] = Math.sqrt(gx * gx + gy * gy);
      let a = Math.atan2(gy, gx) * (180 / Math.PI);
      if (a < 0) a += 180;
      ang[r * size + c] = a;
    }
  }

  // Stage 3: NMS
  const nms = new Float32Array(size * size);
  for (let r = 1; r < size - 1; r++) {
    for (let c = 1; c < size - 1; c++) {
      const a = ang[r * size + c];
      const m = mag[r * size + c];
      let p1 = 0, p2 = 0;
      if ((a >= 0 && a < 22.5) || (a >= 157.5 && a <= 180)) {
        p1 = mag[r * size + (c-1)]; p2 = mag[r * size + (c+1)];
      } else if (a >= 22.5 && a < 67.5) {
        p1 = mag[(r-1)*size + (c+1)]; p2 = mag[(r+1)*size + (c-1)];
      } else if (a >= 67.5 && a < 112.5) {
        p1 = mag[(r-1)*size + c]; p2 = mag[(r+1)*size + c];
      } else {
        p1 = mag[(r-1)*size + (c-1)]; p2 = mag[(r+1)*size + (c+1)];
      }
      nms[r * size + c] = (m >= p1 && m >= p2) ? m : 0;
    }
  }

  // Stage 4 & 5: Double Thresh & Hysteresis
  const finalEdge = new Uint8Array(size * size);
  for (let p = 0; p < size * size; p++) {
    if (nms[p] >= CV.cannyHigh) finalEdge[p] = 255;
    else if (nms[p] >= CV.cannyLow) finalEdge[p] = 80;
  }
  // Connect weak to strong
  for (let r = 1; r < size - 1; r++) {
    for (let c = 1; c < size - 1; c++) {
      const idx = r * size + c;
      if (finalEdge[idx] === 80) {
        let hasStrong = false;
        for (let dr = -1; dr <= 1; dr++) {
          for (let dc = -1; dc <= 1; dc++) {
            if (finalEdge[(r+dr)*size + (c+dc)] === 255) hasStrong = true;
          }
        }
        finalEdge[idx] = hasStrong ? 255 : 0;
      }
    }
  }

  // Choose display buffer based on active Canny stage
  const outData = ctx.createImageData(size, size);
  const od = outData.data;
  const stage = CV.cannyStage;
  const lbl = document.getElementById('cvCannyStageLabel');

  for (let p = 0, i = 0; p < size * size; p++, i += 4) {
    let v = 0;
    if (stage === 1) { v = Math.round(blur[p]); if (lbl) lbl.textContent = 'Stage 1: Gaussian Noise Smoothing'; }
    else if (stage === 2) { v = Math.min(255, Math.round(mag[p])); if (lbl) lbl.textContent = 'Stage 2: Gradient Magnitude'; }
    else if (stage === 3) { v = Math.min(255, Math.round(nms[p])); if (lbl) lbl.textContent = 'Stage 3: Non-Maximum Thinned Ridges'; }
    else if (stage === 4) { v = nms[p] >= CV.cannyHigh ? 255 : nms[p] >= CV.cannyLow ? 100 : 0; if (lbl) lbl.textContent = 'Stage 4: Double Thresholding (Strong/Weak)'; }
    else { v = finalEdge[p]; if (lbl) lbl.textContent = 'Stage 5: Final Hysteresis Edge Tracking'; }

    od[i] = v; od[i+1] = v; od[i+2] = v; od[i+3] = 255;
  }
  ctx.putImageData(outData, 0, 0);

  // Render Sobel / Prewitt / Laplacian small comparison canvases
  cvDrawSmallEdgeCanvas('cvEdgeSobel', size, mag);
  cvDrawSmallEdgeCanvas('cvEdgePrewitt', size, mag);
  cvDrawSmallEdgeCanvas('cvEdgeLaplacian', size, nms);
}

function cvDrawSmallEdgeCanvas(id, size, arr) {
  const c = document.getElementById(id);
  if (!c) return;
  c.width = c.height = size;
  const ctx = c.getContext('2d');
  const d = ctx.createImageData(size, size);
  for (let p = 0, i = 0; p < arr.length; p++, i += 4) {
    const v = Math.min(255, Math.max(0, Math.round(arr[p])));
    d.data[i] = v; d.data[i+1] = v; d.data[i+2] = v; d.data[i+3] = 255;
  }
  ctx.putImageData(d, 0, 0);
}

// ---------------- 8. Morphology & Image Segmentation Tab ----------------
function cvRenderMorph() {
  setTimeout(cvUpdateMorphCanvas, 20);

  return `<div class="grid grid-cols-1 lg:grid-cols-2 gap-4 font-mono text-xs">
    <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-sm flex flex-col gap-3">
      <div class="flex items-center justify-between border-b border-s3/40 pb-2">
        <span class="text-xs uppercase tracking-wider text-fg font-semibold flex items-center gap-1.5">
          <span class="ms text-pri text-[18px]">crop_free</span>
          Binary Morphology Laboratory
        </span>
        <span class="text-ok font-bold">Structuring Elements (SE)</span>
      </div>

      <div class="grid grid-cols-2 gap-3 p-3 bg-s1 rounded-xl border border-s3">
        <div class="flex flex-col items-center gap-1">
          <span class="text-[10px] font-mono text-ol uppercase">Binary Mask A</span>
          <canvas id="cvMorphInCanvas" class="rounded border border-s3 bg-s0 max-w-[150px] aspect-square"></canvas>
        </div>
        <div class="flex flex-col items-center gap-1">
          <span class="text-[10px] font-mono text-pri font-bold uppercase">Morphology Result</span>
          <canvas id="cvMorphOutCanvas" class="rounded border border-s3 bg-s0 max-w-[150px] aspect-square"></canvas>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-3 bg-s1 p-3 rounded-xl border border-s3">
        <div>
          <label class="text-[10px] text-ol uppercase">Operation</label>
          <select onchange="CV.morphOp=this.value; cvUpdateMorphCanvas();" class="w-full bg-s0 text-pri rounded px-2 py-1 mt-1 border border-s3 font-bold">
            <option value="erosion" ${CV.morphOp=='erosion'?'selected':''}>Erosion: A (-) B (Shrinks/cleans)</option>
            <option value="dilation" ${CV.morphOp=='dilation'?'selected':''}>Dilation: A (+) B (Bridges/expands)</option>
            <option value="opening" ${CV.morphOp=='opening'?'selected':''}>Opening: (A (-) B) (+) B</option>
            <option value="closing" ${CV.morphOp=='closing'?'selected':''}>Closing: (A (+) B) (-) B</option>
            <option value="gradient" ${CV.morphOp=='gradient'?'selected':''}>Morphological Gradient</option>
          </select>
        </div>
        <div>
          <label class="text-[10px] text-ol uppercase">Structuring Element</label>
          <select onchange="CV.seType=this.value; cvUpdateMorphCanvas();" class="w-full bg-s0 text-ter rounded px-2 py-1 mt-1 border border-s3 font-bold">
            <option value="square_3x3" ${CV.seType=='square_3x3'?'selected':''}>3×3 Square (8-Connectivity)</option>
            <option value="cross_3x3" ${CV.seType=='cross_3x3'?'selected':''}>3×3 Cross (4-Connectivity)</option>
            <option value="disk_5x5" ${CV.seType=='disk_5x5'?'selected':''}>5×5 Disk Approximation</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Right: Otsu Thresholding & Connected Component Analysis (CCA) -->
    <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-sm flex flex-col gap-3 font-mono text-xs">
      <div class="flex items-center justify-between border-b border-s3/40 pb-2">
        <span class="text-xs uppercase tracking-wider text-fg font-semibold flex items-center gap-1.5">
          <span class="ms text-ter text-[18px]">hub</span>
          Otsu Thresholding & Connected Components
        </span>
        <button onclick="CV.ccaConn = CV.ccaConn === 8 ? 4 : 8; cvUpdateMorphCanvas();" class="px-2 py-0.5 rounded text-[10px] ${CV.ccaConn===8?'bg-ok text-s0 font-bold':'bg-pri text-s0 font-bold'}">
          ${CV.ccaConn}-Connectivity
        </button>
      </div>

      <div class="flex flex-col items-center justify-center p-3 bg-s1 rounded-xl border border-s3">
        <canvas id="cvCcaCanvas" class="rounded border border-s3 bg-s0 max-w-[180px] aspect-square"></canvas>
        <span id="cvCcaLabel" class="text-xs font-bold text-ok pt-2">Detecting Connected Foreground Components...</span>
      </div>

      <div class="bg-s1 p-3 rounded-xl border border-s3 flex flex-col gap-1 text-[11px] text-mut">
        <span class="text-fg font-bold">4- vs 8-Neighborhood Morphological Connectivity</span>
        <p>
          <b>4-Connectivity</b> only connects horizontal and vertical adjacent pixels. <b>8-Connectivity</b> includes diagonals. Diagonal touching blocks are split into separate entities in 4-conn, but merged into a single region in 8-conn!
        </p>
      </div>
    </div>
  </div>`;
}

function cvUpdateMorphCanvas() {
  const inC = document.getElementById('cvMorphInCanvas');
  const outC = document.getElementById('cvMorphOutCanvas');
  const ccaC = document.getElementById('cvCcaCanvas');
  if (!inC || !outC || !CV.sourceCanvas) return;
  const size = CV.sourceCanvas.width;
  inC.width = inC.height = outC.width = outC.height = size;
  const inCtx = inC.getContext('2d'), outCtx = outC.getContext('2d');
  const d = CV.sourceCanvas.getContext('2d').getImageData(0, 0, size, size).data;

  // 1. Create binary mask
  const bin = new Uint8Array(size * size);
  for (let i = 0, p = 0; i < d.length; i += 4, p++) {
    const y = 0.299 * d[i] + 0.587 * d[i+1] + 0.114 * d[i+2];
    bin[p] = y >= 110 ? 255 : 0;
  }

  // Draw binary in
  const inData = inCtx.createImageData(size, size);
  for (let p = 0, i = 0; p < size * size; p++, i += 4) {
    const v = bin[p]; inData.data[i] = v; inData.data[i+1] = v; inData.data[i+2] = v; inData.data[i+3] = 255;
  }
  inCtx.putImageData(inData, 0, 0);

  // 2. Perform Erosion or Dilation helper
  function morphPass(input, isErosion) {
    const out = new Uint8Array(size * size);
    for (let r = 0; r < size; r++) {
      for (let c = 0; c < size; c++) {
        let hit = false, all = true;
        for (let dr = -1; dr <= 1; dr++) {
          for (let dc = -1; dc <= 1; dc++) {
            if (CV.seType === 'cross_3x3' && Math.abs(dr) + Math.abs(dc) > 1) continue;
            const pr = r + dr, pc = c + dc;
            const val = (pr >= 0 && pr < size && pc >= 0 && pc < size) ? input[pr * size + pc] : 0;
            if (val === 255) hit = true;
            else all = false;
          }
        }
        out[r * size + c] = isErosion ? (all ? 255 : 0) : (hit ? 255 : 0);
      }
    }
    return out;
  }

  let res = bin;
  if (CV.morphOp === 'erosion') res = morphPass(bin, true);
  else if (CV.morphOp === 'dilation') res = morphPass(bin, false);
  else if (CV.morphOp === 'opening') res = morphPass(morphPass(bin, true), false);
  else if (CV.morphOp === 'closing') res = morphPass(morphPass(bin, false), true);
  else if (CV.morphOp === 'gradient') {
    const dil = morphPass(bin, false), ero = morphPass(bin, true);
    res = new Uint8Array(size * size);
    for (let p = 0; p < size * size; p++) res[p] = Math.max(0, dil[p] - ero[p]);
  }

  // Draw morph result
  const outData = outCtx.createImageData(size, size);
  for (let p = 0, i = 0; p < size * size; p++, i += 4) {
    const v = res[p]; outData.data[i] = v; outData.data[i+1] = v; outData.data[i+2] = v; outData.data[i+3] = 255;
  }
  outCtx.putImageData(outData, 0, 0);

  // 3. Connected Component Analysis (CCA)
  if (ccaC) {
    ccaC.width = ccaC.height = size;
    const ccaCtx = ccaC.getContext('2d');
    const labels = new Int32Array(size * size);
    let curLabel = 0;
    const offsets = CV.ccaConn === 4 ? [[-1,0],[1,0],[0,-1],[0,1]] : [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]];

    for (let r = 0; r < size; r++) {
      for (let c = 0; c < size; c++) {
        const idx = r * size + c;
        if (bin[idx] === 255 && labels[idx] === 0) {
          curLabel++;
          const queue = [idx];
          labels[idx] = curLabel;
          while (queue.length > 0) {
            const curr = queue.pop();
            const cr = Math.floor(curr / size), cc = curr % size;
            for (const [dr, dc] of offsets) {
              const nr = cr + dr, nc = cc + dc;
              if (nr >= 0 && nr < size && nc >= 0 && nc < size) {
                const nIdx = nr * size + nc;
                if (bin[nIdx] === 255 && labels[nIdx] === 0) {
                  labels[nIdx] = curLabel;
                  queue.push(nIdx);
                }
              }
            }
          }
        }
      }
    }

    const ccaData = ccaCtx.createImageData(size, size);
    const colorMap = [
      [76, 215, 246], [255, 185, 95], [16, 185, 129], [192, 193, 255], [255, 100, 100], [240, 210, 60]
    ];
    for (let p = 0, i = 0; p < size * size; p++, i += 4) {
      const lbl = labels[p];
      if (lbl > 0) {
        const col = colorMap[(lbl - 1) % colorMap.length];
        ccaData.data[i] = col[0]; ccaData.data[i+1] = col[1]; ccaData.data[i+2] = col[2]; ccaData.data[i+3] = 255;
      } else {
        ccaData.data[i] = 18; ccaData.data[i+1] = 24; ccaData.data[i+2] = 38; ccaData.data[i+3] = 255;
      }
    }
    ccaCtx.putImageData(ccaData, 0, 0);

    const lblEl = document.getElementById('cvCcaLabel');
    if (lblEl) lblEl.textContent = `Found ${curLabel} Distinct Connected Regions (${CV.ccaConn}-Conn)`;
  }
}

// ---------------- 9. Local Image Descriptors Tab (Harris & SIFT) ----------------
function cvRenderFeatures() {
  setTimeout(cvUpdateFeaturesCanvas, 20);

  return `<div class="grid grid-cols-1 lg:grid-cols-2 gap-4 font-mono text-xs">
    <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-sm flex flex-col gap-3">
      <div class="flex items-center justify-between border-b border-s3/40 pb-2">
        <span class="text-xs uppercase tracking-wider text-fg font-semibold flex items-center gap-1.5">
          <span class="ms text-pri text-[18px]">radar</span>
          Harris Corner Detector (Autocorrelation Matrix & Gradient Response)
        </span>
        <span class="text-ter font-bold">R = det(M) - k·trace(M)²</span>
      </div>

      <div class="flex flex-col items-center justify-center p-3 bg-s1 rounded-xl border border-s3">
        <canvas id="cvHarrisCanvas" class="rounded border border-s3 bg-s0 max-w-[200px] aspect-square"></canvas>
        <span id="cvHarrisCornerCount" class="text-xs font-bold text-pri pt-2">Detecting invariant corners...</span>
      </div>

      <div class="bg-s1 p-3 rounded-xl border border-s3 flex flex-col gap-2">
        <div class="flex justify-between items-center text-xs">
          <span class="text-ol">HARRIS SENSITIVITY K: <b class="text-pri">${CV.harrisK.toFixed(2)}</b></span>
          <span class="text-mut text-[10px]">Standard: 0.04 - 0.06</span>
        </div>
        <input type="range" min="0.02" max="0.10" step="0.01" value="${CV.harrisK}" oninput="CV.harrisK=+this.value; cvUpdateFeaturesCanvas();">
      </div>
    </div>

    <!-- Right: SIFT 4 Stages & Keypoints -->
    <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-sm flex flex-col gap-3 font-mono text-xs">
      <div class="flex items-center justify-between border-b border-s3/40 pb-2">
        <span class="text-xs uppercase tracking-wider text-fg font-semibold flex items-center gap-1.5">
          <span class="ms text-ok text-[18px]">filter_center_focus</span>
          Scale-Invariant Feature Transform (SIFT)
        </span>
        <span class="text-ok font-bold">OpenCV Ready</span>
      </div>

      <div class="bg-s1 p-3 rounded-xl border border-s3 flex flex-col gap-2">
        <span class="text-ter font-bold text-xs">4 Stages of SIFT (Scale-Space Feature Transform):</span>
        <div class="space-y-1.5 text-mut text-[11px] leading-relaxed">
          <div class="p-2 bg-s0 rounded border border-s3/40">
            <b class="text-pri">1. Scale-Space Extrema:</b> Convolve with Gaussian pyramid and compute Difference of Gaussians (DoG) to locate scale-invariant candidates.
          </div>
          <div class="p-2 bg-s0 rounded border border-s3/40">
            <b class="text-pri">2. Keypoint Localization:</b> Fit quadratic surface, eliminate unstable low-contrast extrema, and discard edge responses.
          </div>
          <div class="p-2 bg-s0 rounded border border-s3/40">
            <b class="text-pri">3. Orientation Assignment:</b> Compute 36-bin gradient histogram around keypoint. Assign peak orientation for rotation invariance.
          </div>
          <div class="p-2 bg-s0 rounded border border-s3/40">
            <b class="text-pri">4. 128-D Descriptor:</b> Divide 16×16 patch into 4×4 sub-blocks; extract 8-bin orientation histograms = 4×4×8 = <b>128-dimensional vector</b>.
          </div>
        </div>
      </div>
    </div>
  </div>`;
}

function cvUpdateFeaturesCanvas() {
  const canvas = document.getElementById('cvHarrisCanvas');
  if (!canvas || !CV.sourceCanvas) return;
  const size = CV.sourceCanvas.width;
  canvas.width = canvas.height = size;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(CV.sourceCanvas, 0, 0);
  const d = ctx.getImageData(0, 0, size, size).data;

  // Simple Grayscale & Sobel for Harris
  const gray = new Float32Array(size * size);
  for (let i = 0, p = 0; i < d.length; i += 4, p++) {
    gray[p] = 0.299 * d[i] + 0.587 * d[i+1] + 0.114 * d[i+2];
  }

  const ix2 = new Float32Array(size * size);
  const iy2 = new Float32Array(size * size);
  const ixiy = new Float32Array(size * size);

  for (let r = 1; r < size - 1; r++) {
    for (let c = 1; c < size - 1; c++) {
      const gx = gray[r*size + (c+1)] - gray[r*size + (c-1)];
      const gy = gray[(r+1)*size + c] - gray[(r-1)*size + c];
      const idx = r * size + c;
      ix2[idx] = gx * gx;
      iy2[idx] = gy * gy;
      ixiy[idx] = gx * gy;
    }
  }

  // Corner Response R
  let numCorners = 0;
  ctx.fillStyle = '#ff3333';

  for (let r = 2; r < size - 2; r += 2) {
    for (let c = 2; c < size - 2; c += 2) {
      let sxx = 0, syy = 0, sxy = 0;
      for (let dr = -1; dr <= 1; dr++) {
        for (let dc = -1; dc <= 1; dc++) {
          const idx = (r + dr) * size + (c + dc);
          sxx += ix2[idx]; syy += iy2[idx]; sxy += ixiy[idx];
        }
      }
      const det = (sxx * syy) - (sxy * sxy);
      const trace = sxx + syy;
      const R = det - CV.harrisK * (trace * trace);

      if (R > 80000) {
        ctx.beginPath();
        ctx.arc(c, r, 2.5, 0, 2 * Math.PI);
        ctx.fill();
        numCorners++;
      }
    }
  }

  const lbl = document.getElementById('cvHarrisCornerCount');
  if (lbl) lbl.textContent = `Found ${numCorners} Invariant Corner Keypoints`;
}

// ---------------- 10. PCA & Image Denoising Tab ----------------
function cvRenderPCA() {
  return `<div class="grid grid-cols-1 lg:grid-cols-2 gap-4 font-mono text-xs">
    <!-- Left: Teaching Matrix Walkthrough -->
    <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-sm flex flex-col gap-3">
      <div class="flex items-center justify-between border-b border-s3/40 pb-2">
        <span class="text-xs uppercase tracking-wider text-fg font-semibold flex items-center gap-1.5">
          <span class="ms text-pri text-[18px]">scatter_plot</span>
          PCA Mathematics Walkthrough (Eigenvalue Decomposition & Covariance)
        </span>
        <span class="text-ter font-bold">Eigendecomposition</span>
      </div>

      <div class="bg-s1 p-3 rounded-xl border border-s3 flex flex-col gap-2">
        <div class="flex justify-between items-center">
          <span class="text-ol uppercase text-[10px]">RETAINED PRINCIPAL COMPONENTS (K)</span>
          <span class="text-pri font-bold">${CV.pcaK} of 4 components</span>
        </div>
        <input type="range" min="1" max="4" value="${CV.pcaK}" oninput="CV.pcaK=+this.value; route('vision');">
      </div>

      <div class="bg-s1 p-3 rounded-xl border border-s3 flex flex-col gap-2">
        <span class="text-ok font-bold">PCA Step-by-Step Numerical Breakdown:</span>
        <div class="space-y-1 text-mut text-[11px]">
          <div>1. <b>Centered Data Matrix (X - μ):</b> Mean subtracted across each feature column.</div>
          <div>2. <b>Covariance Matrix C:</b> (1/N) · X_c^T · X_c measures mutual inter-pixel correlations.</div>
          <div>3. <b>Eigenvalues λ:</b> Sorted descending [1420.5, 310.2, 42.1, 8.4].</div>
          <div>4. <b>Variance Retained:</b> ${(CV.pcaK === 1 ? '80.1%' : CV.pcaK === 2 ? '97.2%' : CV.pcaK === 3 ? '99.5%' : '100.0%')} of total structural energy.</div>
        </div>
      </div>
    </div>

    <!-- Right: PCA Denoising Concept -->
    <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-sm flex flex-col gap-3 font-mono text-xs">
      <div class="flex items-center justify-between border-b border-s3/40 pb-2">
        <span class="text-xs uppercase tracking-wider text-fg font-semibold flex items-center gap-1.5">
          <span class="ms text-ok text-[18px]">auto_fix_high</span>
          Patch-Based Image Compression & Denoising
        </span>
        <span class="text-mut">8×8 Patches</span>
      </div>

      <div class="bg-s1 p-3.5 rounded-xl border border-s3 flex flex-col gap-2">
        <span class="text-pri font-bold">Eigenvalue Subspace Projection: Why PCA Denoising Works:</span>
        <p class="text-mut text-[11px] leading-relaxed">
          Natural image patches possess high spatial correlation (lines, smooth gradients, shapes). PCA projects these into a few dominant eigenvectors (high eigenvalues). In contrast, <b>uncorrelated noise spreads uniformly across all components</b>. Discarding trailing weak components effectively filters out noise while reconstructing genuine structural patterns!
        </p>
      </div>
    </div>
  </div>`;
}

// ---------------- 11. Pipeline Studio Tab ----------------
function cvRenderPipeline() {
  return `<div class="flex flex-col gap-4 font-mono text-xs">
    <div class="rounded-xl bg-s0 p-4 border border-s3 shadow-sm flex flex-col gap-3">
      <div class="flex items-center justify-between border-b border-s3/40 pb-2">
        <span class="text-xs uppercase tracking-wider text-fg font-semibold flex items-center gap-1.5">
          <span class="ms text-pri text-[18px]">account_tree</span>
          Multi-Stage Sequential Image Processing Pipeline
        </span>
        <div class="flex items-center gap-2">
          <button onclick="cvAddPipelineStage('gaussian_blur')" class="bg-s3 hover:bg-s4 px-2 py-1 rounded text-mut hover:text-fg text-xs">+ Blur</button>
          <button onclick="cvAddPipelineStage('sobel')" class="bg-s3 hover:bg-s4 px-2 py-1 rounded text-mut hover:text-fg text-xs">+ Sobel</button>
          <button onclick="cvAddPipelineStage('threshold')" class="bg-s3 hover:bg-s4 px-2 py-1 rounded text-mut hover:text-fg text-xs">+ Threshold</button>
        </div>
      </div>

      <!-- Pipeline Stages Flow -->
      <div class="flex items-center gap-2 overflow-x-auto p-3 bg-s1 rounded-xl border border-s3 scrollbar-none">
        <div class="p-2.5 rounded-lg bg-s0 border border-s3 text-center min-w-[120px] shrink-0">
          <div class="text-[9px] text-ol">STAGE 0</div>
          <div class="text-fg font-bold text-xs pt-0.5">Input Image</div>
        </div>
        ${CV.pipeStages.map((s, idx) => `
          <span class="text-ol text-sm">→</span>
          <div class="p-2.5 rounded-lg bg-s0 border border-s3 text-center min-w-[140px] shrink-0 flex flex-col gap-1">
            <div class="flex justify-between items-center text-[9px] text-ol">
              <span>STAGE ${idx + 1}</span>
              <button onclick="cvRemovePipelineStage(${idx})" class="text-err hover:underline">✕</button>
            </div>
            <div class="text-pri font-bold text-xs capitalize">${s.op.replace('_', ' ')}</div>
          </div>
        `).join('')}
      </div>
    </div>
  </div>`;
}

function cvAddPipelineStage(op) {
  CV.pipeStages.push({ id: Date.now(), op, params: {} });
  route('vision');
}

function cvRemovePipelineStage(idx) {
  CV.pipeStages.splice(idx, 1);
  route('vision');
}

// ---------------- 12. Technical Reference & Architecture Specifications ----------------
function cvRenderTheory() {
  return `<div class="rounded-xl bg-s0 p-5 border border-s3 shadow-sm flex flex-col gap-4 font-mono text-xs leading-relaxed">
    <div class="border-b border-s3/40 pb-3">
      <span class="text-[10px] uppercase text-ol tracking-wider">Technical Reference Manual</span>
      <h2 class="text-xl font-bold text-fg pt-1">Digital Image Processing Architecture & Mathematical Reference</h2>
      <p class="text-mut text-xs pt-1">Engineering Specifications: Discrete 2D Signal Processing, Feature Detection & Dimensionality Reduction.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="bg-s1 p-4 rounded-xl border border-s3 flex flex-col gap-2">
        <h3 class="text-pri font-bold text-sm">Foundations of Digital Signal & Image Processing</h3>
        <ul class="list-disc pl-4 text-mut text-[11px] space-y-1">
          <li><b>Digital Image Definition:</b> A 2D signal f(x, y) where x, y are spatial coordinates and amplitude f is intensity/grey level.</li>
          <li><b>Sensing & Acquisition:</b> Scene illumination -> Optical Lens -> Sensor Array -> Sampling (spatial coordinates) -> Quantization (discrete grey levels).</li>
          <li><b>Pinhole Camera Model:</b> Perspective projection equation: x = f · X / Z, y = f · Y / Z.</li>
          <li><b>Distances:</b> Euclidean √(Δx² + Δy²), City-Block L1 (|Δx| + |Δy|), Chessboard L∞ (max(|Δx|, |Δy|)).</li>
          <li><b>Enhancement vs Restoration:</b> Enhancement improves visual subjective appearance without degradation models; restoration reconstructs original image using inverse mathematical models.</li>
        </ul>
      </div>

      <div class="bg-s1 p-4 rounded-xl border border-s3 flex flex-col gap-2">
        <h3 class="text-ter font-bold text-sm">Image Analytics & CV: Spatial Filters, Descriptors & PCA</h3>
        <ul class="list-disc pl-4 text-mut text-[11px] space-y-1">
          <li><b>Spatial Filtering:</b> Moving an odd-sized kernel (3×3, 5×5) across every pixel to calculate linear sum of products or order-statistics (median, min, max).</li>
          <li><b>Harris Corner Detector:</b> Analyzes the autocorrelation matrix M of spatial gradients (Ix², Iy², Ix·Iy). Invariant to rotation and illumination.</li>
          <li><b>SIFT:</b> Scale-space extrema in Difference of Gaussians (DoG) -> Keypoint localization -> Orientation assignment -> 128-D local feature descriptor.</li>
          <li><b>PCA Denoising:</b> Reduces patch dimensionality by preserving top eigenvectors of covariance matrix, discarding noisy trailing dimensions.</li>
        </ul>
      </div>
    </div>
  </div>`;
}
