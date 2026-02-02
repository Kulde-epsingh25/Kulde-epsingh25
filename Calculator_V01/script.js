const Buttons = document
    .querySelectorAll('.button');
const inputScreen = document
    .getElementById('input');
const resultScreen = document
    .getElementById('result');
function updateScreen(event) {
    if (event === 'C') inputScreen.textContent = inputScreen.textContent.slice(0, -1);
    else if (event === 'clear') inputScreen.textContent = '';
    else if( (event === '+' || event === '-' || event === '*' || event === '/')  && chechlast() ){
        return;
    }
    else
        inputScreen.textContent += event;
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


function calculate(){
    console.log('Calculating');
}
function chechlast() {
    const lastchar = inputScreen.textContent.at(-1);
    if (lastchar === '+' || lastchar === '-' || lastchar === '*' || lastchar === '/') {
        return true;
    }
    return false;
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