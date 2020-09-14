const divItemsItem = document.querySelectorAll('div.item');

dicColors = {1:'#ed74ed',2:'#6c94c9',3:'#FFA500'}

const random = (min, max) => Math.random() * (max - min) + min

for (color in divItemsItem){
    divItemsItem[color].style.background = `${dicColors[Math.floor(random(0,4))]}`
}
