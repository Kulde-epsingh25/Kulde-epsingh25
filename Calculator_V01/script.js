const Buttons = document.
querySelectorAll('.button');
const inputScreen = document.
getElementById('input');
const resultScreen = document.
getElementById('result');
function updateScreen(event){
    if(event === 'C')  inputScreen.textContent = inputScreen.textContent.slice(0, -1);
    else  if(event === 'clear') inputScreen.textContent = '';
    else
        inputScreen.textContent += event;
}
Buttons.
forEach(button => button
                        .addEventListener('click', (event) => 
                            { 
                                updateScreen(event.target.id);
                            })
        );
const clear = document.getElementById('C');
let holdInterval;
clear.addEventListener('mousedown', () => {
    holdInterval =setInterval(() => {
        inputScreen.textContent = '';
    }, 1000)
});
clear.addEventListener('mouseup', () => {
    clearTimeout(holdInterval);
   
});
clear.addEventListener('mouseleave', () => {
    clearTimeout(holdInterval);
   
});

function calculate(){
    try{
        let input = inputScreen.textContent;
        let result = input.split(' ');
        
        console.log(result);

    } catch(error){
       
    }
}
addEventListener('keydown', (event) =>{
    switch(event.key){
        case '1':
            updateScreen(1);
            calculate();
            break;
        case '2':
            updateScreen(2);
            calculate();
            break;
        case '3':
            updateScreen(3);
            calculate();
            break;
        case '4':
            updateScreen(4);
            calculate();
            break;
        case '5':
            updateScreen(5);
            calculate();
            break;
        case '6':
          
            updateScreen(6);
            calculate();
            break;
        case '7':
            updateScreen(7);
            calculate();
            break;
        case '8':
            updateScreen(8);
            calculate();
            break;
        case '9':
            updateScreen(9);
            calculate();
            break;
        case '0':
            updateScreen(0);
            calculate();
            break;
        case '+':
            updateScreen(' + ');
            break;
        case '-':
            updateScreen(' - ');
            break;
        case '*':
            updateScreen(' * ');
            break;
        case '/':
            updateScreen(' / ');
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
        case 'delete':
            updateScreen('clear');
            break;
        
    }   
}) 