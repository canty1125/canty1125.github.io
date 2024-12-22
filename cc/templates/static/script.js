document.addEventListener('DOMContentLoaded', fetchStudents);

async function fetchStudents() {
    const response = await fetch('/get_students');
    const students = await response.json();
    const table = document.getElementById('student-table');
    table.innerHTML = '';
    students.forEach(student => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${student.name}</td>
            <td>
                <select onchange="updateStatus('${student.name}', this.value)">
                    <option value="未點名" ${student.status === '未點名' ? 'selected' : ''}>未點名</option>
                    <option value="已到" ${student.status === '已到' ? 'selected' : ''}>已到</option>
                    <option value="未到" ${student.status === '未到' ? 'selected' : ''}>未到</option>
                </select>
            </td>
            <td><button onclick="deleteStudent('${student.name}')">刪除</button></td>
        `;
        table.appendChild(row);
    });
}

async function updateStatus(name, status) {
    const response = await fetch('/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify([{ name, status }])
    });
    if (response.ok) {
        alert('狀態已更新！');
    }
}

async function addStudent() {
    const name = prompt('請輸入學生姓名：');
    if (!name) return;

    const response = await fetch('/add_student', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
    });

    if (response.ok) {
        alert(`學生 ${name} 已新增！`);
        fetchStudents();
    }
}

async function deleteStudent(name) {
    const response = await fetch('/delete_student', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
    });

    if (response.ok) {
        alert(`學生 ${name} 已刪除！`);
        fetchStudents();
    }
}

async function exportData() {
    window.location.href = '/export';
}
