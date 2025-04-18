const scriptURL = 'https://script.google.com/macros/s/AKfycbxWPt6adLPW1b7puLnj4HBzMBJkPkRukvDizOKjdParmEAvfItHDdQhWrNlFcnrKfCeBA/exec'
const form = document.forms['contact-form']

form.addEventListener('submit', e => {
  
  e.preventDefault()
  
  fetch(scriptURL, { method: 'POST', body: new FormData(form)})
  .then(response => alert("Thank you! Form is submitted" ))
  .then(() => { window.location.reload(); })
  .catch(error => console.error('Error!', error.message))
})


    const phrases = [
      "Web Developer.",
      "Tech Enthusiast.",
      "Problem Solver.",
      "Open Source Contributor."
    ];

    const words = ["a Passionate Python Programmer.", "GATE 2025 Qualified." ,"a Novice Data Analyst.", "an Avid Java Enthusiast.",  "a Jupyter Notebook Explorer.", "a React Frontend Explorer."];
    let i = 0;
    let j = 0;
    let currentWord = "";
    let isDeleting = false;
    const speed = 100;
    const pause = 1000;
  
    function type() {
      if (i < words.length) {
        if (!isDeleting && j <= words[i].length) {
          currentWord = words[i].substring(0, j++);
        } else if (isDeleting && j >= 0) {
          currentWord = words[i].substring(0, j--);
        }
  
        document.getElementById("typed-text").textContent = currentWord;
  
        if (j === words[i].length) {
          isDeleting = true;
          setTimeout(type, pause);
        } else if (j === 0 && isDeleting) {
          isDeleting = false;
          i = (i + 1) % words.length;
          setTimeout(type, speed);
        } else {
          setTimeout(type, speed);
        }
      }
    }
  
    document.addEventListener("DOMContentLoaded", type);
