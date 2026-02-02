const Buttons = document
    .querySelectorAll('.button');
const inputScreen = document
    .getElementById('input');
const resultScreen = document
    .getElementById('result');
function checklast() {
    const lastchar = inputScreen.textContent.at(-1);
    if (lastchar === ' ') {
        return true;
    }
    else return false;
}
function updateScreen(event) {
    if (event === 'C'){ 
        if(inputScreen.textContent.at(-1) === ' '){
            inputScreen.textContent = inputScreen.textContent.slice(0, -3);
        }
        else{
            inputScreen.textContent = inputScreen.textContent.slice(0, -1);
        }
    }
    else if (event === 'clear') {
        inputScreen.textContent = '';
        resultScreen.textContent = '';
    }
    else if( (event === '+' || event === '-' || event === '*' || event === '/')  && checklast() ){
        inputScreen.textContent = inputScreen.textContent.slice(0, -3);
        inputScreen.textContent += ` ${event} `;
    }
    else if( (event === '+' || event === '-' || event === '*' || event === '/')  && !checklast() ){
        inputScreen.textContent += ` ${event} `;
    }
    else if(checklast() && event === '.' ){
        inputScreen.textContent += `0${event}`;
    }
    else if(inputScreen.textContent === '' && (event === '+' || event === '-' || event === '*' || event === '/')){
        inputScreen.textContent += `0`;
    }
    else{
        inputScreen.textContent += event;
    }
}
Buttons
    .forEach(button => button
        .addEventListener('click', (event) => {
            updateScreen(event.target.id);
            calculate();
        })
    );
const clear = document.getElementById('C');
let holdInterval;
clear.addEventListener('mousedown', () => {
    holdInterval = setInterval(() => {
        inputScreen.textContent = '';
    }, 1000)
})
clear.addEventListener('mouseup', () => {
    clearTimeout(holdInterval);

})
clear.addEventListener('mouseleave', () => {
    clearTimeout(holdInterval);

})

document.onselectstart = (e) => {
  e.preventDefault();
  return false;
};
let newexpression = [];

function calculate(){

    const expression = inputScreen.textContent;
     newexpression = expression.split(' ');
    try{
    while(newexpression.includes('/')){
        const index = newexpression.indexOf('/');
        let result = 0;
        if(newexpression[index + 1] === '0') {
            throw new Error('Infinity');
        }
        else {
        result = parseFloat(newexpression[index - 1]) / parseFloat(newexpression[index + 1]);
        newexpression.splice(index - 1, 3, result);
        }
    }
    while(newexpression.includes('*')){
        const index = newexpression.indexOf('*');
        const result = parseFloat(newexpression[index - 1]) * parseFloat(newexpression[index + 1]);
        newexpression.splice(index - 1, 3, result);
    }

    while(newexpression.includes('+') || newexpression.includes('-')){
        const indexPlus = newexpression.indexOf('+');
        const indexMinus = newexpression.indexOf('-');
        let result = 0;
        if(indexPlus !== -1 && (indexPlus < indexMinus || indexMinus === -1)){ 
            result = parseFloat(newexpression[indexPlus - 1]) + parseFloat(newexpression[indexPlus + 1]);
            console.log(newexpression);
            newexpression.splice(indexPlus - 1, 3, result);
        } else if(indexMinus !== -1){
            result = parseFloat(newexpression[indexMinus - 1]) - parseFloat(newexpression[indexMinus + 1]);
            console.log(newexpression);
            newexpression.splice(indexMinus - 1, 3, result);
        }
    }
    if(Number.isNaN(newexpression[0])) throw new Error('Error: NaN');
    else resultScreen.textContent = newexpression[0];
    
    } catch (error) {
        resultScreen.textContent = 'Error';
    }
}

addEventListener('keydown', (event) => {
    if (isFinite(+event.key)) {
        updateScreen(event.key);
        calculate();
        return;
    }
     switch (event.key) {
        case '+':
            updateScreen('+');
            break;
        case '-':
            updateScreen('-');
            break;
        case '*':
            updateScreen('*');
            break;
        case '/':
            updateScreen('/');
            break;
        case '=':
            calculate();
            break;
        case '.':
            updateScreen('.');
            break;
        case 'Enter':
            calculate();
            break;
        case 'Backspace':
            updateScreen('C');
            calculate();
            break;
        case 'Delete':
            updateScreen('clear');
            break;
        default:
            break;
    }
})