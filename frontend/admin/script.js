const validCredentials = { 'admin': 'admin123', 'supervisor': 'supervisor123' };

let reports = [];
let currentPage = 1;
const rowsPerPage = 30;

function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('errorMessage');

    if (validCredentials[username] && validCredentials[username] === password) {
        document.getElementById('loginPage').style.display = 'none';
        document.getElementById('reportsPage').style.display = 'block';
        loadReports();
        document.getElementById('username').value = '';
        document.getElementById('password').value = '';
        errorMessage.style.display = 'none';
    } else {
        errorMessage.style.display = 'block';
    }
}

function logout() {
    if (confirm('Yakin ingin logout?')) {
        document.getElementById('loginPage').style.display = 'block';
        document.getElementById('reportsPage').style.display = 'none';
        reports = [];
        currentPage = 1;
        document.getElementById('reportTable').innerHTML = '';
        document.getElementById('search').value = '';
    }
}

async function loadReports() {
    const searchValue = document.getElementById('search').value.trim();
    try {
        const res = await fetch("http://127.0.0.1:8000/admin/reports");
        const data = await res.json();
        reports = data.reports;
        if (searchValue) reports = reports.filter(r => r.ticket && r.ticket.includes(searchValue));
        currentPage = 1;
        displayReports();
    } catch (error) {
        alert("Error loading reports: " + error.message);
    }
}

function displayReports() {
    const start = (currentPage - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    const paginatedReports = reports.slice(start, end);
    const tbody = document.getElementById('reportTable');
    tbody.innerHTML = "";

    paginatedReports.forEach(r => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${r.ticket || ''}</td>
            <td>${r.email || ''}</td>
            <td>${r.nik || ''}</td>
            <td>${r.nama || ''}</td>
            <td>${r.lokasi || ''}</td>
            <td>${r.kategori || ''}</td>
            <td>${r.pesan || ''}</td>
            <td>${r.sentimen || ''}</td>
            <td>${r.waktu || ''}</td>
            <td>${r.status || ''}</td>
            <td class="actions">
            <button class="btn-pending" onclick="updateStatus('${r.ticket}', 'Belum selesai')">Belum selesai</button>
            <button class="btn-done" onclick="updateStatus('${r.ticket}', 'Selesai')">Selesai</button>
            </td>
        `;
        tbody.appendChild(tr);
    });

    document.getElementById('pageInfo').textContent =
        `Page ${currentPage} of ${Math.ceil(reports.length / rowsPerPage)}`;
}

async function updateStatus(ticket, newStatus) {
    if (!confirm(`Yakin ingin mengubah status menjadi "${newStatus}"?`)) return;

    try {
        const res = await fetch("http://127.0.0.1:8000/admin/update_status", {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ticket: ticket, new_status: newStatus })
        });
        if (res.ok) {
            const idx = reports.findIndex(r => r.ticket === ticket);
            if (idx > -1) reports[idx].status = newStatus;
            displayReports();
            alert(`Status berhasil diubah ke "${newStatus}"`);
        } else alert("Gagal mengubah status!");
    } catch (error) {
        alert("Error: " + error.message);
    }
}

function prevPage() {
    if (currentPage > 1) { currentPage--; displayReports(); }
}

function nextPage() {
    if (currentPage < Math.ceil(reports.length / rowsPerPage)) { currentPage++; displayReports(); }
}
