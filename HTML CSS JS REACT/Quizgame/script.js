const startscreen = document.getElementById('start-screen');
const quizscreen = document.getElementById('quiz-screen');
const resultscreen = document.getElementById('result-screen');
const startBtn = document.getElementById('startBtn');
const restartBtn = document.getElementById('restartBtn');
const questionEl = document.getElementById('question');
const answercontainer = document.getElementById('answers-container');
const answerButtons = document.querySelectorAll('.answer-btn');
const currentquestionEl = document.getElementById('current-question');
const qustionnumberEl = document.getElementById('question-number');
const totalquestionsEl = document.getElementById('total-questions');
const scoreEl = document.getElementById('score');
const finalscoreEl = document.getElementById('final-score');
const totalquestionsresultEl = document.getElementById('total-questions-result');
const resultmessageEl = document.getElementById('result-message');
const progressBar = document.getElementById('progress');

const quizQuestions = [
    {
        question: "What is the capital of France?",
        answers: [
            { text: "Berlin", correct: false },
            { text: "Madrid", correct: false },
            { text: "Paris", correct: true },
            { text: "Rome", correct: false }
        ]       
    },
    {
        question: "Which planet is known as the Red Planet?",
        answers: [
            { text: "Earth", correct: false },
            { text: "Mars", correct: true },
            { text: "Jupiter", correct: false },
            { text: "Saturn", correct: false }
        ]       
    },
    {
        question: "Who wrote 'To Kill a Mockingbird'?",
        answers: [
            { text: "Harper Lee", correct: true },
            { text: "Mark Twain", correct: false },
            { text: "Ernest Hemingway", correct: false },
            { text: "F. Scott Fitzgerald", correct: false }
        ]       
    },
    {
        question: "What is the largest ocean on Earth?",
        answers: [
            { text: "Atlantic Ocean", correct: false },
            { text: "Indian Ocean", correct: false },
            { text: "Arctic Ocean", correct: false },
            { text: "Pacific Ocean", correct: true }
        ]       
    },
    {
        question: "Which element has the chemical symbol 'O'?",
        answers: [
            { text: "Gold", correct: false },
            { text: "Oxygen", correct: true },
            { text: "Silver", correct: false },
            { text: "Hydrogen", correct: false }
        ]       
    },
    {
        question: "Who painted the Mona Lisa?",
        answers: [
            { text: "Vincent van Gogh", correct: false },
            { text: "Pablo Picasso", correct: false },
            { text: "Leonardo da Vinci", correct: true },
            { text: "Claude Monet", correct: false }
        ]       
    },
    {
        question: "What is the smallest prime number?",
        answers: [
            { text: "0", correct: false },
            { text: "1", correct: false },
            { text: "2", correct: true },
            { text: "3", correct: false }
        ]       
    },
    {
        question: "Which country is known as the Land of the Rising Sun?",
        answers: [
            { text: "China", correct: false },
            { text: "Japan", correct: true },
            { text: "South Korea", correct: false },
            { text: "Thailand", correct: false }
        ]       
    },
    {
        question: "What is the chemical formula for water?",
        answers: [
            { text: "H2O", correct: true },
            { text: "CO2", correct: false },
            { text: "O2", correct: false },
            { text: "NaCl", correct: false }
        ]       
    },
    {
        question: "Who is the author of the Harry Potter series?",
        answers: [
            { text: "J.R.R. Tolkien", correct: false },
            { text: "George R.R. Martin", correct: false },
            { text: "J.K. Rowling", correct: true },
            { text: "Stephen King", correct: false }
        ]       
    }
];

let currentQuestionIndex = 0;
let score = 0;
let answerDisabled = false;
totalquestionsEl.textContent = quizQuestions.length;
totalquestionsresultEl.textContent = quizQuestions.length;


startBtn.addEventListener('click', startQuiz);
restartBtn.addEventListener('click', restartQuiz);

function startQuiz() {
    startscreen.classList.remove('active');
    quizscreen.classList.add('active');
    showquestion();
}
function showquestion(){
    const currentQuestion = quizQuestions[currentQuestionIndex];
    questionEl.textContent = currentQuestion.question;
    progressBar.style.width = `${((currentQuestionIndex) / quizQuestions.length) * 100}%`;
    answerDisabled = false;
    qustionnumberEl.textContent = `${currentQuestionIndex + 1}`;
    answercontainer.innerHTML = '';
    currentQuestion.answers.forEach(answers => {
        const button = document.createElement('button');
        button.textContent = answers.text;
        button.classList.add('answer-btn');
      if(answers.correct){
            button.dataset.correct = answers.correct;
        }

        button.addEventListener('click', selectAnswer = (e) => {
            if (answerDisabled) return;
            const selectedButton = e.target;
            const correct = selectedButton.dataset.correct;
            if (correct) {
                score++;
                scoreEl.textContent = score;
                button.classList.add('correct');
            }
            else {
                button.classList.add('incorrect');
                 Array.from(answercontainer.children).forEach(button => {
                if (button.dataset.correct) {
                    button.classList.add('correct');
                }
            });
            }
    answerDisabled = true;
    setTimeout(() => {
        currentQuestionIndex++;
        if(currentQuestionIndex < quizQuestions.length){
            showquestion();
        }else{
            showresult();
        }
    }, 1000); } ) 
        answercontainer.appendChild(button);
    });

}
function showresult(){
    quizscreen.classList.remove('active');
    resultscreen.classList.add('active');
    finalscoreEl.textContent = score;
    if(score / quizQuestions.length >= 0.8){
        resultmessageEl.textContent = "Excellent work! You're a quiz master!";
    }else if(score / quizQuestions.length >= 0.5){
        resultmessageEl.textContent = "Good job! You have a solid understanding.";
    }else{
        resultmessageEl.textContent = "Don't worry, keep practicing and you'll improve!";
    }
}
function restartQuiz(){
    resultscreen.classList.remove('active');
    startscreen.classList.add('active');
    currentQuestionIndex = 0;
    score = 0;
    scoreEl.textContent = score;
}
