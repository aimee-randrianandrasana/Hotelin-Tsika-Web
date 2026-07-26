document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    if (!searchInput) return;

    searchInput.addEventListener('input', function () {
        const q = this.value.toLowerCase();
        const rows = document.querySelectorAll('tbody tr');
        rows.forEach(row => {
            if (!row.querySelector('td')) return;
            row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
        });
    });
});
