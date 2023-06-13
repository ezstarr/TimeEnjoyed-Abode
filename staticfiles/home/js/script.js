const nonauthRead = document.getElementById('nonauth-read');
const formSubmitted = document.getElementById('form-submitted');


nonauthRead.addEventListener('submit', function (e) {
    e.preventDefault(); // prevents page reloading

    const nonauthReadFormData = new FormData(nonauthRead);
    const name = nonauthReadFormData.get('name');

    formSubmitted.innerHTML = `Hi <strong>${name}</strong> :) your form has been submitted...<br>`;

    const j_data = JSON.stringify(Object.fromEntries(nonauthReadFormData));


    fetch(nonauthRead.action, {
        method: 'POST',
        body: j_data,
        headers: {'X-CSRFToken': nonauthReadFormData.get('csrfmiddlewaretoken')}
    })
        .then(response => response.json())
        .then(jObject => jObject.random_cards.forEach(item => formSubmitted.innerHTML += `${item['name']} `))
           // .then(thing => thing.forEach(item => console.log(item)))
           //  .then(thing => console.log(thing))
})
