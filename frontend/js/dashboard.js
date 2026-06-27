(async () => {
  const user = await guardAuth();
  if (!user) return;

  initNavbar(user);
  document.getElementById('greeting').textContent = `Welcome back, ${user.name}! 👋`;
  document.getElementById('statSince').textContent = formatDate(user.created_at);

  const histRes = await API.getHistory();
  if (!histRes.error && histRes.history) {
    const list   = histRes.history;
    const scores = list.map(h => h.ats_score).filter(Boolean);
    document.getElementById('statTotal').textContent  = list.length;
    document.getElementById('statBest').textContent   = scores.length ? Math.max(...scores).toFixed(0) + '%' : '—';
    document.getElementById('statLatest').textContent = scores.length ? scores[0].toFixed(0) + '%' : '—';
  }

  const dropZone = document.getElementById('dropZone');
  dropZone.addEventListener('dragover',  e => { e.preventDefault(); dropZone.classList.add('drag-over'); });
  dropZone.addEventListener('dragleave', ()=> dropZone.classList.remove('drag-over'));
  dropZone.addEventListener('drop', e => {
    e.preventDefault(); dropZone.classList.remove('drag-over');
    if (e.dataTransfer.files[0]) setFile(e.dataTransfer.files[0]);
  });
})();

let selectedFile = null;

function handleFileSelect(input) { if (input.files[0]) setFile(input.files[0]); }

function setFile(file) {
  const allowed = ['application/pdf','application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
  if (!allowed.includes(file.type) && !file.name.match(/\.(pdf|docx)$/i)) {
    showToast('Only PDF or DOCX files allowed.', 'error'); return;
  }
  selectedFile = file;
  document.getElementById('fileName').textContent = file.name;
  document.getElementById('fileSize').textContent = (file.size/1024).toFixed(1) + ' KB';
  document.getElementById('filePreview').style.display = 'flex';
  document.getElementById('filePreview').classList.remove('hidden');
}

function clearFile() {
  selectedFile = null;
  document.getElementById('fileInput').value = '';
  document.getElementById('filePreview').style.display = 'none';
}

async function handleUpload() {
  const btn      = document.getElementById('analyzeBtn');
  const errEl    = document.getElementById('uploadErr');
  const jobTitle = document.getElementById('jobTitle').value.trim();
  const jobDesc  = document.getElementById('jobDesc').value.trim();

  errEl.classList.add('hidden');
  if (!selectedFile) { errEl.textContent = 'Please select a resume file.'; errEl.classList.remove('hidden'); return; }
  if (!jobDesc)       { errEl.textContent = 'Job description is required.'; errEl.classList.remove('hidden'); return; }

  btn.disabled = true; btn.textContent = 'Uploading…';

  const result = await API.upload(selectedFile, jobTitle, jobDesc);
  if (result.error) {
    errEl.textContent = result.error; errEl.classList.remove('hidden');
    btn.disabled = false; btn.textContent = 'Analyze My Resume →'; return;
  }

  sessionStorage.setItem('history_id', result.history_id);
  sessionStorage.setItem('filename',   result.filename);
  sessionStorage.setItem('job_desc',   jobDesc);
  sessionStorage.setItem('job_title',  jobTitle);

  showToast('Upload successful! Running ATS analysis…', 'success');
  setTimeout(() => { window.location.href = 'report.html'; }, 800);
}
