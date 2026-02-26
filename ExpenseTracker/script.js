const incomeInput = document.getElementById('income');
const expenseInput = document.getElementById('expense');
const balanceDisplay = document.getElementById('balance');
const transactionList = document.querySelector('.transaction-list');
const transactionform = document.getElementById('transaction-form');
const descriptionInput = document.getElementById('description');
const amountInput = document.getElementById('amount');

let transactions = JSON.parse(localStorage.getItem('transactions')) || [];

transactionform.addEventListener('submit', addTransaction);
transactionList.addEventListener('click', handleDelete);
initialize();

function addTransaction(e) {
    e.preventDefault();
    const description = descriptionInput.value.trim();
    const amount = parseFloat(amountInput.value);
    if (!description || Number.isNaN(amount)) {
        return;
    }
    
    transactions.push({ id: Date.now(), description, amount });
    updateTransactions();
    updateSummary();

    transactionform.reset();
}

function updateTransactions() {
    transactionList.innerHTML = '';
    const sortedTransactions = [...transactions].reverse();
    sortedTransactions.forEach(transaction => {
        const li = document.createElement('li');
        li.classList.add('transaction-item');
        li.classList.add(transaction.amount >= 0 ? 'income' : 'expense');
        li.innerHTML = `${transaction.description}: $${transaction.amount.toFixed(2)} <button class="delete-btn" data-id="${transaction.id}">x</button>`;
        transactionList.appendChild(li);
    });
}

    function updateSummary() {
        const amounts = transactions.map(transaction => transaction.amount);
        const income = amounts.filter(value => value > 0).reduce((sum, value) => sum + value, 0);
        const expense = amounts.filter(value => value < 0).reduce((sum, value) => sum + value, 0);
        const balance = income + expense;

        incomeInput.textContent = `$${income.toFixed(2)}`;
        expenseInput.textContent = `$${Math.abs(expense).toFixed(2)}`;
        balanceDisplay.textContent = `$${balance.toFixed(2)}`;
        localStorage.setItem('transactions', JSON.stringify(transactions)); // Save transactions to localStorage and JSON.stringify() converts the transactions array into a JSON string before storing it in localStorage. This allows us to persist the transaction data across page reloads.
    }

    function handleDelete(e) {
        const button = e.target.closest('.delete-btn');
        if (!button) {
            return;
        }
        const id = Number(button.dataset.id);
        transactions = transactions.filter(transaction => transaction.id !== id); // This line filters out the transaction with the matching id from the transactions array, effectively deleting it.
        updateTransactions();
        updateSummary();
    }

    function initialize() {
        updateTransactions();
        updateSummary();
    }