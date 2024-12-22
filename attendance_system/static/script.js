document.addEventListener('DOMContentLoaded', fetchStudents);

async function fetchStudents() {
    const response = await fetch('/get_students');
    const students = await response.json();
    const table = document.getElementById('student-table');
    table.innerHTML = '';
    students.forEach((student, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${student.姓名}</td>
            <td>
                <select id="status-${index}">
                    <option value="未點名" ${student.狀態 === '未點名' ? 'selected' : ''}>未點名</option>
                    <option value="已到" ${student.狀態 === '已到' ? 'selected' : ''}>已到</option>
                    <option value="未到" ${student.狀態 === '未到' ? 'selected' : ''}>未到</option>
                </select>
            </td>
        `;
        table.appendChild(row);
    });
}

async function saveData() {
    const rows = document.querySelectorAll('tbody tr');
    const data = [];
    rows.forEach((row, index) => {
        const name = row.cells[0].textContent;
        const status = document.getElementById(`status-${index}`).value;
        data.push({ 姓名: name, 狀態: status });
    });

    const response = await fetch('/update_students', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });

    if (response.ok) {
        alert('數據已保存！');
    }
}

async function exportData() {
    window.location.href = '/export';
}
