const newcard = document.getElementById('new-btn');
const lists = document.querySelectorAll('.items');
const listContainers = document.querySelectorAll('.list');
const cards = document.querySelectorAll('.card');

newcard.addEventListener('click', addCard);
cards.forEach(card => {
    ensureCardId(card);
    card.addEventListener('dragstart', dragStart);
    card.addEventListener('dragend', dragEnd);
});
for (const list of listContainers) {
    list.addEventListener('dragover', dragOver);
    list.addEventListener('dragenter', dragEnter);
    list.addEventListener('dragleave', dragLeave);
    list.addEventListener('drop', dragDrop);
}
function dragStart(e) {
    ensureCardId(e.currentTarget);
    e.dataTransfer.setData('text/plain', e.currentTarget.id);

}
function dragEnd(e) {
    e.dataTransfer.clearData();
}
function dragOver(e) {
    e.preventDefault();
}
function dragEnter(e) {
    e.preventDefault();
    e.currentTarget.classList.add('drag-over');
}
function dragLeave(e) {
    e.currentTarget.classList.remove('drag-over');
}
function dragDrop(e) {
    e.preventDefault();
    const id = e.dataTransfer.getData('text/plain');
    const draggable = document.getElementById(id);
    const items = e.currentTarget.querySelector('.items');
    if (draggable && items) {
        items.appendChild(draggable);
    }
    e.currentTarget.classList.remove('drag-over');
}
function addCard() { 
    const card = document.createElement('div');
    card.className = 'card';
    ensureCardId(card);
    card.draggable = true;
    card.textContent = 'New Task';
    lists[0].appendChild(card);
    editcard(card);
    card.addEventListener('dragstart', dragStart);
    card.addEventListener('dragend', dragEnd);
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

function ensureCardId(card) {
    if (!card.id) {
        card.id = `card-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
    }
}





