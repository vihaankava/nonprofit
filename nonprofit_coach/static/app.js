// Tab switching functionality
function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.tab === tabName) {
            btn.classList.add('active');
        }
    });
    
    // Update tab panes
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.remove('active');
    });
    document.getElementById(tabName).classList.add('active');
    
    // Reset the form when switching to "New Idea" tab
    if (tabName === 'new-idea') {
        resetQuestionnaire();
    }
}

// Add event listeners to tab buttons
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.addEventListener('click', () => {
            switchTab(btn.dataset.tab);
        });
    });
    
    // API Key Form Handler
    const apiKeyForm = document.getElementById('api-key-form');
    if (apiKeyForm) {
        apiKeyForm.addEventListener('submit', handleApiKeySubmit);
    }
    
    // Check for success message
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('success') === 'true') {
        const ideaId = urlParams.get('idea_id');
        // Show success message
        showSuccessMessage(ideaId);
        // Clean up URL
        window.history.replaceState({}, document.title, '/');
    }
});

// Show success message
function showSuccessMessage(ideaId) {
    const message = document.createElement('div');
    message.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #34c759;
        color: white;
        padding: 16px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        font-weight: 500;
    `;
    message.innerHTML = `
        ✅ Nonprofit idea created successfully! 
        <a href="/site/${ideaId}" style="color: white; text-decoration: underline; margin-left: 8px;">View Site</a>
    `;
    document.body.appendChild(message);
    
    // Remove after 5 seconds
    setTimeout(() => {
        message.style.transition = 'opacity 0.3s ease';
        message.style.opacity = '0';
        setTimeout(() => message.remove(), 300);
    }, 5000);
}

// Questionnaire state
let currentQuestion = 1;
const totalQuestions = 8;

// Setup API Key
async function setupApiKey() {
    const apiKey = document.getElementById('api-key').value.trim();
    const saveApiKey = document.getElementById('save-api-key').checked;
    
    if (!apiKey) {
        alert('Please enter an API key');
        return;
    }
    
    try {
        const response = await fetch('/api/setup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                api_key: apiKey,
                save_api_key: saveApiKey
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Hide API setup, show questionnaire
            document.getElementById('api-setup').style.display = 'none';
            document.getElementById('questionnaire').style.display = 'block';
            updateProgress();
        } else {
            alert(data.error || 'Failed to set up API key');
        }
    } catch (error) {
        alert('Network error. Please try again.');
    }
}

// Update progress bar
function updateProgress() {
    const progress = (currentQuestion / totalQuestions) * 100;
    document.getElementById('progress-fill').style.width = `${progress}%`;
    document.getElementById('progress-text').textContent = `Question ${currentQuestion} of ${totalQuestions}`;
}

// Move to next question
async function nextQuestion() {
    const currentQuestionEl = document.querySelector(`.question[data-question="${currentQuestion}"]`);
    const input = currentQuestionEl.querySelector('input, textarea');
    
    if (!input.value.trim()) {
        alert('Please provide an answer before continuing');
        return;
    }
    
    // Get AI follow-up if it's a textarea question (questions 2-7)
    if (currentQuestion >= 2 && currentQuestion <= 7) {
        await getAIFollowup(input.name, input.value.trim());
    }
    
    // Hide current question
    currentQuestionEl.classList.remove('active');
    
    // Show next question
    currentQuestion++;
    const nextQuestionEl = document.querySelector(`.question[data-question="${currentQuestion}"]`);
    nextQuestionEl.classList.add('active');
    
    // Update progress and buttons
    updateProgress();
    updateButtons();
}

// Move to previous question
function previousQuestion() {
    // Hide current question
    const currentQuestionEl = document.querySelector(`.question[data-question="${currentQuestion}"]`);
    currentQuestionEl.classList.remove('active');
    
    // Show previous question
    currentQuestion--;
    const prevQuestionEl = document.querySelector(`.question[data-question="${currentQuestion}"]`);
    prevQuestionEl.classList.add('active');
    
    // Update progress and buttons
    updateProgress();
    updateButtons();
}

// Update button visibility
function updateButtons() {
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const submitBtn = document.getElementById('submit-btn');
    
    prevBtn.style.display = currentQuestion === 1 ? 'none' : 'inline-block';
    nextBtn.style.display = currentQuestion === totalQuestions ? 'none' : 'inline-block';
    submitBtn.style.display = currentQuestion === totalQuestions ? 'inline-block' : 'none';
}

// Submit questionnaire
async function submitQuestionnaire() {
    const currentQuestionEl = document.querySelector(`.question[data-question="${currentQuestion}"]`);
    const input = currentQuestionEl.querySelector('input, textarea');
    
    if (!input.value.trim()) {
        alert('Please provide an answer before submitting');
        return;
    }
    
    // Collect all responses
    const formData = {};
    for (let i = 1; i <= totalQuestions; i++) {
        const questionEl = document.querySelector(`.question[data-question="${i}"]`);
        const inputEl = questionEl.querySelector('input, textarea');
        formData[inputEl.name] = inputEl.value.trim();
    }
    
    // Show loading state
    document.getElementById('questionnaire').style.display = 'none';
    document.getElementById('loading').style.display = 'block';
    
    try {
        const response = await fetch('/api/complete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Reload the page to show the new idea in "All Ideas" tab
            // The user can then click on it to access the generated site
            window.location.href = '/?success=true&idea_id=' + data.idea_id;
        } else {
            alert(data.error || 'Failed to complete questionnaire');
            document.getElementById('loading').style.display = 'none';
            document.getElementById('questionnaire').style.display = 'block';
        }
    } catch (error) {
        alert('Network error. Please try again.');
        document.getElementById('loading').style.display = 'none';
        document.getElementById('questionnaire').style.display = 'block';
    }
}

// Get AI follow-up question
async function getAIFollowup(questionType, userResponse) {
    try {
        // Collect current context
        const ideaContext = {};
        for (let i = 1; i < currentQuestion; i++) {
            const questionEl = document.querySelector(`.question[data-question="${i}"]`);
            const inputEl = questionEl.querySelector('input, textarea');
            if (inputEl.value.trim()) {
                ideaContext[inputEl.name] = inputEl.value.trim();
            }
        }
        
        const response = await fetch('/api/question', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question_type: questionType,
                user_response: userResponse,
                idea_context: ideaContext
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.followup) {
            // Display AI follow-up
            const followupDiv = document.getElementById(`followup-${currentQuestion - 1}`);
            if (followupDiv) {
                followupDiv.textContent = `AI Coach: ${data.followup}`;
                followupDiv.classList.add('show');
            }
        }
    } catch (error) {
        console.error('Failed to get AI follow-up:', error);
    }
}

// Reset questionnaire to initial state
function resetQuestionnaire() {
    // Reset to first question
    currentQuestion = 1;
    
    // Hide all questions
    document.querySelectorAll('.question').forEach(q => {
        q.classList.remove('active');
    });
    
    // Show first question
    document.querySelector('.question[data-question="1"]').classList.add('active');
    
    // Clear all form inputs
    document.querySelectorAll('#questionnaire-form input, #questionnaire-form textarea').forEach(input => {
        input.value = '';
    });
    
    // Clear all follow-up questions
    document.querySelectorAll('.followup-question').forEach(followup => {
        followup.textContent = '';
        followup.classList.remove('show');
    });
    
    // Clear API key fields
    document.getElementById('api-key').value = '';
    document.getElementById('save-api-key').checked = false;
    
    // Show API setup, hide questionnaire and loading
    document.getElementById('api-setup').style.display = 'block';
    document.getElementById('questionnaire').style.display = 'none';
    document.getElementById('loading').style.display = 'none';
    
    // Update progress and buttons
    updateProgress();
    updateButtons();
}

// Delete an idea
async function deleteIdea(ideaId) {
    if (!confirm('Are you sure you want to delete this idea? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/ideas/${ideaId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Remove the card from the UI
            const card = document.getElementById(`idea-${ideaId}`);
            if (card) {
                card.style.transition = 'opacity 0.3s ease';
                card.style.opacity = '0';
                setTimeout(() => {
                    card.remove();
                    
                    // Check if there are no more ideas
                    const ideasGrid = document.querySelector('.ideas-grid');
                    if (ideasGrid && ideasGrid.children.length === 0) {
                        ideasGrid.innerHTML = `
                            <div class="empty-state">
                                <p>No ideas yet. Create your first nonprofit idea!</p>
                                <button class="btn btn-primary" onclick="switchTab('new-idea')">Get Started</button>
                            </div>
                        `;
                    }
                }, 300);
            }
        } else {
            alert(data.error || 'Failed to delete idea');
        }
    } catch (error) {
        alert('Network error. Please try again.');
    }
}


// Voice input functionality
let recognition = null;
let currentVoiceTarget = null;

// Check if browser supports speech recognition
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onresult = (event) => {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript + ' ';
            } else {
                interimTranscript += transcript;
            }
        }

        if (currentVoiceTarget) {
            const input = document.getElementById(currentVoiceTarget);
            if (input) {
                // Append to existing text
                const currentText = input.value;
                if (finalTranscript) {
                    input.value = currentText + finalTranscript;
                }
            }
        }
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        stopVoiceInput();
    };

    recognition.onend = () => {
        stopVoiceInput();
    };
}

// Add click handlers to all voice buttons
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.voice-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const targetId = this.dataset.target;
            toggleVoiceInput(targetId, this);
        });
    });
});

function toggleVoiceInput(targetId, button) {
    if (!recognition) {
        alert('Voice input is not supported in your browser. Please use Chrome, Edge, or Safari.');
        return;
    }

    if (currentVoiceTarget === targetId) {
        // Stop listening
        stopVoiceInput();
    } else {
        // Start listening
        stopVoiceInput(); // Stop any existing recognition
        currentVoiceTarget = targetId;
        
        try {
            recognition.start();
            button.classList.add('listening');
            button.textContent = '⏹️';
        } catch (error) {
            console.error('Error starting recognition:', error);
        }
    }
}

function stopVoiceInput() {
    if (recognition && currentVoiceTarget) {
        try {
            recognition.stop();
        } catch (error) {
            // Already stopped
        }
        
        // Reset button state
        const button = document.querySelector(`[data-target="${currentVoiceTarget}"]`);
        if (button) {
            button.classList.remove('listening');
            button.textContent = '🎤';
        }
        
        currentVoiceTarget = null;
    }
}
