


let calendar
document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('calendar');
    calendar = new FullCalendar.Calendar(calendarEl, {
           initialView: 'timeGridDay',
                locale: 'cs',
                themeSystem: 'bootstrap5',
                headerToolbar: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'
                },
          eventClick : function(info){
            changeElements(true,"enabled", "d-none")
            
            document.querySelector("#form-name").value = info.event.title
            
            let date = new Date(info.event.start);
            let year = date.getFullYear()
            let month = String(date.getMonth() +1).padStart(2,"0")
            let day = String(date.getDate()).padStart(2,"0")
            
            let formatted = `${year}-${month}-${day}`
      
            document.querySelector("#form-date").value = formatted
            document.querySelector("#form-time").value =info.event.extendedProps.time
            document.querySelector("#form-phone").value =info.event.extendedProps.phone
            
            new bootstrap.Modal(document.querySelector("#eventModal")).show()
            
            //patch function
            let patchButton = document.querySelector("#patch-button").addEventListener("click", (event) => {
            changeElements(false,"d-none","enabled")
            
            let form = document.querySelector("#editForm").addEventListener("submit", (event) =>{
              event.preventDefault()
              let editedUser = {
                name : event.target.elements.name.value,
                date : event.target.elements.date.value,
                time : event.target.elements.time.value,
                phone : event.target.elements.phone.value,
                id : info.event.extendedProps.id
                
              }
              
              updateDatabase(editedUser)
            })
            
            })

            //delete function
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

async function updateDatabase(users) {
  await fetch("/update_db",{
    method : "PATCH",
    headers : {
      "Content-Type": "application/json"
    },
    body : JSON.stringify(users)
  


  })
  calendar.refetchEvents()

}
   
const changeElements = (isReadOnly,removeCls,addCls) => {
  let saveButton = document.querySelector("#submitButton")
  if(removeCls) saveButton.classList.remove(removeCls)
  if(addCls) saveButton.classList.add(addCls)
  const sel = ["#form-name","#form-date", "#form-time","#form-phone"]
    sel.forEach((id) => {
    const element = document.querySelector(id)
    element.toggleAttribute("readonly", isReadOnly)
  })
  saveButton.toggleAttribute("disabled", isReadOnly)
  
}

