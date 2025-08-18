document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
          initialView: 'dayGridMonth',
           headerToolbar:{
                 start:"dayGridMonth,dayGridWeek,dayGridDay,list",
                 center:"title",
                 end:"today,prev,next"
           }
           
          
           
        });
        calendar.render();
      });



let form = document.querySelector("#my-form").addEventListener("submit", (event) => {
    event.preventDefault()
    userData = {
    name : event.target.name.value,
    date : event.target.date.value,
    time : event.target.time.value,
    phone : event.target.phone.value,
    }

  fetch("/api_python/submit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(userData)
  })
  .then(response => response.json())
  .then(data => {
    console.log('server response:', data);
  })
  .catch(error => {
    console.error('eror:', error);
  });
    event.target.name.value = ""
    event.target.date.value = ""
    event.target.time.value = ""
    event.target.phone.value = ""

})
    