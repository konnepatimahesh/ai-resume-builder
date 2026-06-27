(async () => {
  const user = await guardAuth();
  if (!user) return;
  initNavbar(user);

  const result = await API.getHistory();

  if (result.error) {
    showToast(result.error, 'error');
    return;
  }

  const list = result.history || [];
  const badge = document.getElementById('totalBadge');
  badge.textContent = `${list.length} session${list.length !== 1 ? 's' : ''}`;

  const tbody = document.getElementById('historyBody');

  if (list.length === 0) {
    document.getElementById('tableWrapper').classList.add('hidden');
    document.getElementById('emptyState').classList.remove('hidden');
    return;
  }

  tbody.innerHTML = list.map((h, i) => {
    const score = h.ats_score != null ? h.ats_score.toFixed(0) : null;
    const scoreBadge = score
      ? `<span class="badge" style="background:${scoreColor(score)};color:#fff">${score}% ${scoreLabel(score)}</span>`
      : '<span class="text-muted">—</span>';

    const pdfLink  = h.pdf_path
      ? `<a href="http://localhost:5000/outputs/${h.pdf_path}" target="_blank" class="btn btn-ghost btn-sm">PDF</a>`
      : '';
    const docxLink = h.docx_path
      ? `<a href="http://localhost:5000/outputs/${h.docx_path}" target="_blank" class="btn btn-ghost btn-sm">DOCX</a>`
      : '';

    return `
      <tr>
        <td class="text-muted">${i + 1}</td>
        <td><strong>${h.job_title || 'Untitled'}</strong></td>
        <td>${scoreBadge}</td>
        <td>${formatDateTime(h.created_at)}</td>
        <td class="d-flex gap-1">${pdfLink}${docxLink || '<span class="text-muted text-sm">Not yet generated</span>'}</td>
      </tr>`;
  }).join('');
})();