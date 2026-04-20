document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predictionForm');
    const modal = document.getElementById('resultModal');
    const resultHeading = document.getElementById('predictionResult');
    const confidenceText = document.getElementById('predictionConfidence');
    const progressBar = document.getElementById('confidenceBar');
    const resetBtn = document.getElementById('resetBtn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Add a loading state
        const btn = form.querySelector('button[type="submit"]');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<span>Analyzing...</span>';
        btn.style.opacity = '0.7';
        btn.disabled = true;

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        
        // Convert number types
        data.SeniorCitizen = parseInt(data.SeniorCitizen);
        data.tenure = parseInt(data.tenure);
        data.MonthlyCharges = parseFloat(data.MonthlyCharges);
        data.TotalCharges = parseFloat(data.TotalCharges);

        try {
            // Replace with your Render/Railway backend URL once deployed
            const API_URL = 'http://127.0.0.1:8000'; 
            
            const response = await fetch(`${API_URL}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error(`Server Error: ${response.status}`);
            }

            const result = await response.json();
            
            // Re-enable Form button
            btn.innerHTML = originalText;
            btn.style.opacity = '1';
            btn.disabled = false;

            showModal(result.prediction, result.confidence);

        } catch (error) {
            console.error(error);
            alert("Error predicting churn. Make sure the server is running.");
            btn.innerHTML = originalText;
            btn.style.opacity = '1';
            btn.disabled = false;
        }
    });

    resetBtn.addEventListener('click', () => {
        modal.classList.add('hidden');
        setTimeout(() => {
            progressBar.style.width = '0%';
        }, 400); // Wait for transition
    });

    function showModal(prediction, confidence) {
        modal.classList.remove('hidden');
        
        if (prediction.toLowerCase() === 'churn' || prediction.toLowerCase() === 'yes') {
            resultHeading.innerHTML = "High Risk of <span class='churn-yes'>Churn</span>";
            progressBar.style.background = "linear-gradient(90deg, #ff2a2a, #ff7a7a)";
        } else {
            resultHeading.innerHTML = "Customer will <span class='churn-no'>Stay</span>";
            progressBar.style.background = "linear-gradient(90deg, var(--neon-purple), var(--neon-blue))";
        }

        confidenceText.textContent = `Confidence: ${confidence.toFixed(2)}%`;
        
        // Slight delay to allow CSS transition to catch form rendering
        setTimeout(() => {
            progressBar.style.width = `${confidence}%`;
        }, 100);
    }
});
