const backendUrl = window.location.origin + '/evaluate_answer';

document.getElementById("Submit").addEventListener("click", async function() {
    let textareaContent = document.getElementById("UserCode").value;

    let AIResponseDiv = document.getElementById('AIResponse');
    AIResponseDiv.classList.remove('hidden');

    try {
        // Send user code to the backend for evaluation
        let response = await fetch(backendUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code: textareaContent,
                question: "Create a Python class called Employee that stores the following information for each employee: name, age, and job position. Use the employee data provided below to create instances of the Employee class and store them in a list. Next, write a function called print_employee_names that takes the list of employees as an argument and prints each employee's name to the console. See below for given employee data: Sarah, 36, Engineer John, 42, Accountant Bob, 53, Cashier"
            })
        });

        let result = await response.json();
        let feedback = result.feedback;

        // Display AI's feedback
        AIResponseDiv.innerHTML = feedback;

        // Check if the AI response indicates success
        if (feedback.toLowerCase().startsWith("correct")) {
            userQuizGrade = true;
            document.getElementById('Continue').classList.remove('hidden');
        } else {
            alert("Incorrect. Please try again.");
        }
    } catch (error) {
        AIResponseDiv.innerHTML = "Error communicating with the backend. Please try again.";
        console.error('Error:', error);
    }
});

document.getElementById("Continue").addEventListener("click", function() {
    if (userQuizGrade) {
        alert("You have completed the free trial!");
    } 
});
