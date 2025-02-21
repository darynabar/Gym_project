document.addEventListener("DOMContentLoaded", function () {
    const questions = document.querySelectorAll(".faq-question");

    questions.forEach(question => {
        question.addEventListener("click", function () {
            const answer = this.nextElementSibling; // Шукаємо наступний елемент (відповідь)
            
            // Закриваємо всі інші відповіді перед відкриттям нової
            document.querySelectorAll(".faq-answer").forEach(el => {
                if (el !== answer) {
                    el.style.maxHeight = null;
                    el.classList.remove("faq-active");
                }
            });

            // Якщо відповідь вже відкрита — закриваємо її
            if (answer.style.maxHeight) {
                answer.style.maxHeight = null;
                answer.classList.remove("faq-active");
            } else {
                answer.style.maxHeight = answer.scrollHeight + "px"; // Встановлюємо висоту для плавного відкриття
                answer.classList.add("faq-active");
            }
        });
    });
});
