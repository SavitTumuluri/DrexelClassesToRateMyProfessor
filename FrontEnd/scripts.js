async function handleSubmit() {
    // Get values from all inputs
    const selectedMajor = document.getElementById('major-select').value;
    const selectedTerm = document.getElementById('term-select').value;
    const creditHours = document.getElementById('credit-limit').value;
    const classHistory = document.getElementById('history-input').value.toString();

    // Create an object with the form data
    const formData = {
        major: selectedMajor,
        term: selectedTerm,
        credits: creditHours,
        history: classHistory
    };

    // Log to console to verify data (you can remove this later)
    console.log('Form Data:', formData);
    localStorage.setItem('scheduleData', JSON.stringify(formData));

    // Basic validation
    if (!selectedMajor || !selectedTerm || !creditHours || !classHistory) {
        alert('Please fill in all fields');
        return;
    }

    try {
        const response = await fetch('/api/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();
        console.log('Success:', result);
    } catch (error) {
        console.error('Error:', error);
        alert('There was a problem submitting your data');
    }
    // Here you can:
    // 1. Send to backend
    // 2. Store in localStorage
    // 3. Process the data
    return formData;
}

document.addEventListener('DOMContentLoaded', function() {
     // Add modal HTML to the document
     document.body.insertAdjacentHTML('beforeend', `
        <div class="modal" id="instructionsModal">
            <div class="modal-content">
                <span class="close-button" id="closeModal">&times;</span>
                <h2>How to Get Your Class History</h2>
                <div class="instructions">
                    <p>Follow these steps to get your class history:</p>
                    <ol>
                        <li>Go to your DegreeWorks page and click on the three dots on the right-hand side of the page.</li>
                        <img src="path/to/your/image1.png" alt="Step 1">
                        <li>Step 2 with description</li>
                        <img src="path/to/your/image2.png" alt="Step 2">
                        <li>Step 3 with description</li>
                    </ol>
                </div>
            </div>
        </div>
    `);

    // Modal functionality
    const helpLink = document.getElementById('history-help');
    const modal = document.getElementById('instructionsModal');
    const closeButton = document.getElementById('closeModal');

    helpLink.addEventListener('click', function(e) {
        e.preventDefault();
        modal.style.display = 'block';
    });

    closeButton.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
    
    const creditInput = document.getElementById('credit-limit');
    
    function validateCredits() {
        const credits = parseInt(creditInput.value);
        if (isNaN(credits)) {
            creditInput.classList.remove('invalid');
            return;
        }
        
        if (credits < 12 || credits > 20) {
            creditInput.classList.add('invalid');
        } else {
            creditInput.classList.remove('invalid');
        }
    }
    
    // Check on input change
    creditInput.addEventListener('input', validateCredits);
    const submitButton = document.getElementById('submit-btn');
    submitButton.addEventListener('click', handleSubmit);
});