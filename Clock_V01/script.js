const hourHand = document.querySelector('#hour-hand');
const minuteHand = document.querySelector('#minute-hand');
const secondHand = document.querySelector('#second-hand');

function updateClock(){
    try {
    let hour = new Date().getHours();
    const minute = new Date().getMinutes();
    const second = new Date().getSeconds();
    if(hour >= 12){
        hour -= 12;
    }
    secondHand.style.transform = `rotate(${second * 6}deg)`;
    minuteHand.style.transform = `rotate(${minute * 6}deg)`;
    hourHand.style.transform = `rotate(${(hour * 30) + (minute / 2)}deg)`;
    }   
    catch (error) {
    console.error("An error occurred while updating the clock:", error);
}
}
updateClock();
setInterval(updateClock, 1000);
