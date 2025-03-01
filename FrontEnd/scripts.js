document.addEventListener('DOMContentLoaded', function() {
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
});