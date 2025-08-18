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

async function getData() {
    const url =  "http://127.0.0.1:5000/calendarapi"
    const response = await fetch(url)
    const result = await response.json()
    let p = document.createElement("p")
    p.textContent = JSON.stringify(result)
    document.querySelector("body").appendChild(p)

}

getData()


let form = document.querySelector("#my-form").addEventListener("submit", (event) => {
    event.preventDefault()
    let name = event.target.name.value
    let date = event.target.date.value
    let time = event.target.time.value
    let phone = event.target.phone.value
    let userdata = {
        name : name,
        date : date,
        time:time,
        phone:phone
    }
    console.log(userdata)

})
