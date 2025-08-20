let calendar
document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('calendar');
    calendar = new FullCalendar.Calendar(calendarEl, {
          initialView: 'dayGridMonth',
          locale : "cs",
           headerToolbar:{
                 start:"dayGridMonth,dayGridWeek,dayGridDay,list",
                 center:"title",
                 end:"today,prev,next",
                 
           },
          eventClick : function(info){
            document.querySelector(".modal-body").textContent = info.event.title
            document.querySelector(".modal-body").textContent =info.event.start
            document.querySelector(".modal-body").textContent =info.event.extendedProps.time
            document.querySelector(".modal-body").textContent =info.event.extendedProps.phone
            
            new bootstrap.Modal(document.querySelector("#eventModal")).show()
            
            
            let button = document.querySelector("#delete-button").addEventListener("click", (event) => {
            let id = info.event.extendedProps.id
            deleteFromDB(id)
            
          })
            

         
         
          },
      
          events :  async function (fetchInfo, successCallback, failureCallback) {
            try{

              const data = await catchEvent()
              const events = []
                      
              data.forEach(function(ev){
              let event = {
                          title : ev["name"],
                          start : ev["date"],
                          extendedProps:{
                            phone : ev["phone"],
                            time: ev["time"],
                            id : ev["id"]
                          }     
                }
              events.push(event)
              })
              successCallback(events)
                  } catch(err){
                        failureCallback(err)
                      }}
           
        });
      calendar.render();
      });

async function catchEvent(params) {
  const url = "/send_event"
  const response = await fetch(url)
  const result = await response.json()
  return result} 
  
let form = document.querySelector("#my-form").addEventListener("submit", async (event) => {
    event.preventDefault()
    userData = {
    name : event.target.name.value,
    date : event.target.date.value,
    time : event.target.time.value,
    phone : event.target.phone.value,
    }

  await fetch("/api_python/submit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(userData)
  })
  calendar.refetchEvents()
    event.target.reset()

})


async function deleteFromDB(id) {
  user = {userID : id}
  await fetch("/delete_id", {
    method : "POST",
    headers : {
       "Content-Type": "application/json"},
    body : JSON.stringify(user)
  })
  calendar.refetchEvents()
  
}


