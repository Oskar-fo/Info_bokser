function updateClock() {
    const now = new Date();
    const options = {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    };
    document.getElementById('timestamp').textContent = now.toLocaleDateString('no-NO', options);
}

setInterval(updateClock, 1000);
updateClock();

// To-Do liste
const API = 'http://localhost:5000';

async function loadList() {
    try {
        const res = await fetch(API + '/todos');
        const todos = await res.json();
        
        const list = document.getElementById('list');
        list.innerHTML = '';
        
        if (todos.length === 0) {
            list.innerHTML = '<li style="text-align:center; color:#999;">Ingen oppgaver</li>';
            return;
        }
        
        todos.forEach(todo => {
            const li = document.createElement('li');
            li.className = 'item';
            li.innerHTML = `
                <input 
                    type="checkbox" 
                    ${todo.fullfort ? 'checked' : ''}
                    class="checkbox"
                    onchange="toggle(${todo.id}, this.checked)"
                >
                <span style="${todo.fullfort ? 'text-decoration: line-through; opacity: 0.6;' : ''}">${todo.titel}</span>
                <button class="del-btn" onclick="del(${todo.id})">Slett</button>
            `;
            list.appendChild(li);
        });
    } catch (e) {
        console.error(e);
    }
}

async function add() {
    const input = document.getElementById('input');
    const text = input.value.trim();
    
    if (!text) return;
    
    try {
        await fetch(API + '/todos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ titel: text })
        });
        input.value = '';
        loadList();
    } catch (e) {
        alert('Feil: ' + e);
    }
}

async function toggle(id, done) {
    try {
        await fetch(API + '/todos/' + id, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ fullfort: done ? 1 : 0 })
        });
        loadList();
    } catch (e) {
        alert('Feil: ' + e);
    }
}

async function del(id) {
    if (!confirm('Slett?')) return;
    try {
        await fetch(API + '/todos/' + id, { method: 'DELETE' });
        loadList();
    } catch (e) {
        alert('Feil: ' + e);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('addBtn').addEventListener('click', add);
    document.getElementById('input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') add();
    });
    loadList();
});



