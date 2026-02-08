const newcard = document.getElementById('new-btn');
const lists = document.querySelectorAll('.items');
const cards = document.querySelectorAll('.card');

newcard.addEventListener('click', addCard); 
cards.forEach(card => {
    console.log(card);
    card.addEventListener('dragstart', dragStart);
    card.addEventListener('dragend', dragEnd);
    });
for(const list of lists) {
    list.addEventListener('dragover', dragOver);
    list.addEventListener('dragenter', dragEnter);
    list.addEventListener('dragleave', dragLeave);
    list.addEventListener('drop', dragDrop);
}
function dragStart(e) {
    e.dataTransfer.setData('text/plain', e.target.id);

}
function dragEnd(e) {
    e.dataTransfer.clearData();
}
function dragOver(e) {
    e.preventDefault();
}
function dragEnter(e) {
    e.preventDefault();
    e.target.classList.add('drag-over');
}
function dragLeave(e) {
    e.target.classList.remove('drag-over');
}
function dragDrop(e) {
    e.preventDefault();
    const id = e.dataTransfer.getData('text/plain');
    const draggable = document.getElementById(id);
    e.target.appendChild(draggable);
    e.target.classList.remove('drag-over');
}
function addCard() { 
    const card = document.createElement('div');
    card.className = 'card';
    card.id = `card-${Date.now()}`;
    card.draggable = true;
    card.textContent = 'New Task';
    lists[0].appendChild(card);
    editcard(card);
        card.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            editcard(card);
        });
}
 
function editcard(card) {   
    const title = prompt('Enter task title:');
    if (title) {
        card.textContent = title;
    }
    else {
        card.remove();
    } 
}





