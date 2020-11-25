const animationLi = document.querySelector('ul.animation');

for ( let i = 0; i < 16; i++ ) {

  const li = document.createElement('li');

  const random = (min, max) => Math.random() * (max - min) + min
  
  const size = Math.floor(random(50, 100));
  const position = random(10,90);
  const delay = random(5, 0.5);
  const duration = random(24, 12)

  li.style.width = `${size}px`;
  li.style.height = `${size}px`;
  li.style.bottom = `-${size}px`;
  li.style.left = `${position}%`;
  li.style.animationDelay = `${delay}s`
  li.style.animationDuration = `${duration}s`
  li.style.animationTimingFunction = `cubic-bezier: ${Math.random()}, ${Math.random()}, ${Math.random()}, ${Math.random()}`

  animationLi.appendChild(li);
}
