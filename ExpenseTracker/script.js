const incomeInput = document.getElementById('income');
const expenseInput = document.getElementById('expense');
const addIncomeBtn = document.getElementById('add-income');
const addExpenseBtn = document.getElementById('add-expense');
const incomeList = document.getElementById('income-list');
const expenseList = document.getElementById('expense-list');
const totalDisplay = document.getElementById('total');

addIncomeBtn.addEventListener('click', () => {
    const amount = parseFloat(incomeInput.value);
    if (!isNaN(amount) && amount > 0) {
        addEntry(incomeList, amount, 'income');
        incomeInput.value = '';
        updateTotal();
    }   
}); 