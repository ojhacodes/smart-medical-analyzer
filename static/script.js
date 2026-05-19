document.addEventListener('DOMContentLoaded', () => {
    // Navigation
    const navAnalyze = document.getElementById('nav-analyze');
    const navHistory = document.getElementById('nav-history');
    const viewAnalyze = document.getElementById('view-analyze');
    const viewHistory = document.getElementById('view-history');

    navAnalyze.addEventListener('click', () => {
        navAnalyze.classList.add('active');
        navHistory.classList.remove('active');
        viewAnalyze.classList.add('active');
        viewHistory.classList.remove('active');
    });

    navHistory.addEventListener('click', () => {
        navHistory.classList.add('active');
        navAnalyze.classList.remove('active');
        viewHistory.classList.add('active');
        viewAnalyze.classList.remove('active');
        loadHistory();
    });

    // Analyze functionality
    const analyzeBtn = document.getElementById('analyze-btn');
    const notesInput = document.getElementById('notes-input');
    const btnText = analyzeBtn.querySelector('.btn-text');
    const btnLoader = document.getElementById('btn-loader');
    
    // Result elements
    const emptyState = document.getElementById('empty-state');
    const resultContent = document.getElementById('result-content');
    
    analyzeBtn.addEventListener('click', async () => {
        const notes = notesInput.value.trim();
        if (!notes) {
            showToast('Please enter some notes to analyze', 'error');
            return;
        }

        // Loading state
        analyzeBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'block';

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ notes: notes })
            });

            if (!response.ok) {
                throw new Error(`Server returned ${response.status}`);
            }

            const data = await response.json();
            displayResults(data);
            showToast('Analysis complete!', 'success');
        } catch (error) {
            console.error('Analysis error:', error);
            showToast('Failed to analyze notes. See console.', 'error');
        } finally {
            // Restore button
            analyzeBtn.disabled = false;
            btnText.style.display = 'block';
            btnLoader.style.display = 'none';
        }
    });

    function displayResults(data) {
        emptyState.classList.add('hidden');
        resultContent.classList.remove('hidden');

        // Demographics
        document.getElementById('res-age').textContent = data.age || 'N/A';
        document.getElementById('res-gender').textContent = data.gender || 'Unknown';

        // Symptoms
        const symContainer = document.getElementById('res-symptoms');
        symContainer.innerHTML = '';
        if (data.symptoms && data.symptoms.length > 0) {
            data.symptoms.forEach(sym => {
                const span = document.createElement('span');
                span.className = 'tag';
                span.textContent = sym;
                symContainer.appendChild(span);
            });
        } else {
            symContainer.textContent = 'None identified';
        }

        // Medications
        const tbody = document.querySelector('#res-medications tbody');
        tbody.innerHTML = '';
        if (data.medications && data.medications.length > 0) {
            data.medications.forEach(med => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>${med.name}</strong></td>
                    <td>${med.dosage}</td>
                    <td>${med.frequency}</td>
                    <td>${med.duration}</td>
                `;
                tbody.appendChild(tr);
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align:center">No medications prescribed</td></tr>';
        }

        // Advice
        const adviceEl = document.getElementById('res-advice');
        if (data.advice) {
            adviceEl.textContent = data.advice;
            adviceEl.parentElement.style.display = 'block';
        } else {
            adviceEl.parentElement.style.display = 'none';
        }
    }

    // History Functionality
    const historyList = document.getElementById('history-list');
    const refreshHistoryBtn = document.getElementById('refresh-history-btn');
    const historyLoader = document.getElementById('history-loader');

    refreshHistoryBtn.addEventListener('click', loadHistory);

    async function loadHistory() {
        historyList.innerHTML = '';
        historyLoader.classList.remove('hidden');
        historyList.appendChild(historyLoader);

        try {
            const response = await fetch('/history');
            if (!response.ok) throw new Error('Failed to fetch history');
            
            const records = await response.json();
            historyLoader.classList.add('hidden');
            
            if (records.length === 0) {
                historyList.innerHTML = '<p style="color:var(--text-secondary)">No history found.</p>';
                return;
            }

            records.reverse().forEach(record => {
                const date = new Date(record.created_at).toLocaleString();
                const item = document.createElement('div');
                item.className = 'history-item';
                item.innerHTML = `
                    <div class="history-header">
                        <span>ID: #${record.id}</span>
                        <span>${date}</span>
                    </div>
                    <div class="history-preview">
                        "${record.raw_notes.substring(0, 80)}${record.raw_notes.length > 80 ? '...' : ''}"
                    </div>
                `;
                
                // Clicking history loads it into the analyzer view
                item.addEventListener('click', () => {
                    displayResults(record);
                    notesInput.value = record.raw_notes;
                    navAnalyze.click(); // Switch tab
                });
                
                historyList.appendChild(item);
            });
        } catch (error) {
            console.error('History error:', error);
            historyLoader.classList.add('hidden');
            historyList.innerHTML = '<p style="color:var(--danger)">Error loading history.</p>';
        }
    }

    // Toast utility
    function showToast(message, type = 'success') {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.className = `toast show ${type}`;
        
        setTimeout(() => {
            toast.className = 'toast';
        }, 3000);
    }
});
