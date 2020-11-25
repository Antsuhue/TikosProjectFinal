const iconsPencil = document.querySelectorAll('i.fa-pencil');
const iconsCheck = document.querySelectorAll('i.fa-check');
const iconsTimes = document.querySelectorAll('i.fa-times');
const inputs = document.querySelectorAll('input.qntd');
const inputsMin = document.querySelectorAll('input.min');
const inputsProduct = document.querySelectorAll('input.product');
const inputsUnity = document.querySelectorAll('input.unity');


iconsPencil.forEach(function(icon, indice){

    icon.addEventListener('click', async function(){
        inputs[indice].disabled = 0
        inputsMin[indice].disabled = 0
        inputsProduct[indice].disabled = 0
        inputs[indice].focus()
        inputsMin[indice]
        inputsProduct[indice]
        iconsCheck[indice].style.color = 'black'
        iconsTimes[indice].style.color = 'black'
     
        iconsTimes.forEach(function(icon, indice){
            icon.addEventListener('click', async function(){
            iconsCheck[indice].style.color = 'transparent'
            iconsTimes[indice].style.color = 'transparent'
            inputs[indice].disabled = 1
            inputsMin[indice].disabled = 1
            inputsProduct[indice].disabled = 1
            });
        });
        
    });
});

function Letras(e, t) {
    try {
        if (window.event) {
            var charCode = window.event.keyCode;
        } else if (e) {
            var charCode = e.which;
        } else {
            return true;
        }
        if ((charCode == 00 || charCode == 32) || (charCode >= 48 && charCode <= 57) || (charCode >= 65 && charCode <= 90) || (charCode >= 97 && charCode <= 122))
            return true;
        else
            return false;
    } catch (err) {
        alert(err.Description);
    }
}