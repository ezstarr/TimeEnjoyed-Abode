const nonauthRead = document.getElementById('nonauth-read');
const formSubmitted = document.getElementById('form-submitted');

if (nonauthRead === null) {
  console.log("read is authenticated")}

else {
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
  })}


let currentDate = new Date();
const curMonthYear = document.getElementById("cal-title")
let month = ""
let year = ""


function renderCalendar() {
  let firstDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
  let lastDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);
  let daysInMonth = lastDayOfMonth.getDate();
  let dayOfWeek = firstDayOfMonth.getDay();


  let calendar = document.getElementById("calendar");
  calendar.innerHTML = ""



function getMonthYear(date) {
  const lang = navigator.languages[0]
  const monthFmt = new Intl.DateTimeFormat(lang, {month: "long"})
  const yearFmt = date.getUTCFullYear()
  month = monthFmt.format(date)
  year = yearFmt
}

getMonthYear(currentDate)


  curMonthYear.textContent = `${month} ${year}`

function getWeekDay(date) {
  const lang = navigator.languages[0] // gets nativ language
  const weekdayFmt = new Intl.DateTimeFormat(lang, {weekday: "narrow"}) // gets narrow wkdy from it
  if (lang.slice(0, 2) == "en") {
    return weekdayFmt.format(date)[0] // returns en str
  } else {
    return weekdayFmt.format(date) // returns local str
  }
}

let days = [
  new Date(2023, 4, 7), // Sun
  new Date(2023, 4, 1), // Mon May 01 2023 00:00:00 GMT-0700 (Pacific Daylight Time),
  new Date(2023, 4, 2), // Tue May 02 2023 00:00:00 GMT-0700 (Pacific Daylight Time)
  new Date(2023, 4, 3), // W
  new Date(2023, 4, 4), // T
  new Date(2023, 4, 5), // F
  new Date(2023, 4, 6), // S
   // S
]

const narrow_days = [] // eventually ["S", "M", "T", "W", "T", "F", "S"];

for (let i = 0; i < days.length; i++) {
  narrow_days.push(getWeekDay(days[i]))
}

  for (let day of narrow_days) {
    let dayElement = document.createElement("div");
    dayElement.classList.add('narrow-day');
    dayElement.innerText = day;
    calendar.appendChild(dayElement); // .date aka MTWTFSS
  }

  for (let i = 0; i < dayOfWeek; i++) {
    let dayElement = document.createElement("div");
    dayElement.classList.add("cal-day");
    calendar.appendChild(dayElement);  // number (1-30)
  }

  for (let i = 1; i <= daysInMonth; i++) {
    let dayElement = document.createElement("div");
    dayElement.classList.add("cal-day");
    dayElement.innerText = i;
    if (currentDate.getDate() == i && currentDate.getMonth() == new Date().getMonth()) {
      dayElement.classList.add("cal-current-day");

    }
    calendar.appendChild(dayElement);
  }

}


renderCalendar();


let backButton = document.getElementById("month-previous-btn");
backButton.innerText = "<";

let forwardButton = document.getElementById("month-next-btn");
forwardButton.innerText = ">";


backButton.addEventListener("click", function() {
  currentDate.setMonth(currentDate.getMonth() - 1);
  renderCalendar();
});
forwardButton.addEventListener("click", function() {
  currentDate.setMonth(currentDate.getMonth() + 1);
  renderCalendar();
});
