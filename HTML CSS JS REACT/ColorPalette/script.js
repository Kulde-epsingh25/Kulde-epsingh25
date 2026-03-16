const generateBtn = document.querySelector("#generate-btn");  
const colorBoxes = document.querySelectorAll(".color-box");
const colorCodes = document.querySelectorAll(".color-code");
const copyButtons = document.querySelectorAll(".copy-btn");
const paletteContainer = document.querySelector(".palette");

generateBtn.addEventListener("click", changeColors);
paletteContainer.addEventListener("click", (e) => {
  if(e.target.classList.contains("copy-btn") || e.target.classList.contains("color-box")) {
    const hexCode = e.target.previousElementSibling.textContent;
    navigator.clipboard.writeText(hexCode).then(() => {
        setTimeout(() => {
          e.target.classList.remove("fa-copy");
          e.target.classList.add("fa-check");
        }, 100);
        setTimeout(() => {
          e.target.classList.remove("fa-check");
          e.target.classList.add("fa-copy");
        }, 3000);

    }).catch(err => {
      console.error("Failed to copy: ", err);
    });
  }
});
function changeColors() {
  colorBoxes.forEach((box, index) => {
    const randomColor = getRandomColor();
    box.style.backgroundColor = randomColor;
    colorCodes[index].textContent = randomColor;
  });
}
changeColors(); 
function getRandomColor() {
  const letters = "0123456789ABCDEF";
  let color = "#";
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}  

