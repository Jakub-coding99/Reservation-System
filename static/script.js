let selectedID = null

const modal = new bootstrap.Modal(document.querySelector("#eventModal"))

const confirmModal = new bootstrap.Modal(document.querySelector("#confirmModal"))


let cancelButton = document.querySelector("#cancel-button")

cancelButton.addEventListener("click", () => {
  changeElements(true,"enabled", "d-none")
  modal.hide()
  
})

let patchButton = document.querySelector("#patch-button")
patchButton.addEventListener("click", (event) => {
           
              changeElements(false,"d-none","enabled")
              patchButton.style.display = "none"
              cancelButton.style.display = "flex"

})


            
let editForm = document.querySelector("#editForm").addEventListener("submit", (event) =>{
             
event.preventDefault()
let editedUser = {
  name : event.target.elements.name.value,
  date : event.target.elements.date.value,
  time : event.target.elements.time.value,
  phone : event.target.elements.phone.value,
  id : selectedID           
       }
  
updateDatabase(editedUser)
modal.hide()
toastFunctionSuccess("Klient úspěšně upraven","success","USPĚŠNÉ")
})
            
//delete function
let button = document.querySelector("#delete-button").addEventListener("click", (event) => {

modal.hide()
confirmModal.show()

yes = document.querySelector("#confirmYes")
no = document.querySelector("#confirmNo")

closeBtn = document.querySelector("#closeModal")
id = selectedID

  yes.addEventListener("click", () => {
  confirmModal.hide()
  deleteFromDB(id)
  toastFunctionSuccess("Klient úspěšně odstraněn z kalendáře","success","ÚSPĚŠNÉ")

  })


  no.addEventListener("click", () => {
    confirmModal.hide()
  })
  closeBtn.addEventListener("click", (event) => {
            confirmModal.hide() })

})
          
let calendar
document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('calendar');
    calendar = new FullCalendar.Calendar(calendarEl, {
      firstDay:1,
      fixedWeekCount:false,
           initialView: 'dayGridMonth',
                locale: 'cs',
                themeSystem: 'bootstrap5',
                headerToolbar: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth,timeGridWeek,listMonth',
                    
            
                }, 
          buttonText: {
              today:    'Dnes',
              month:    'Měsíc',
              week:     'Týden',
              
              list:     'Výpis'

          },
               
          
          eventClick : function(info){
           
            cancelButton.style.display = "none"
            
            patchButton.style.display = "flex"
            changeElements(true,"enabled", "d-none")
            selectedID = info.event.extendedProps.id
            
            document.querySelector("#form-name").value = info.event.title

            let datetime = info.event.start
           
            let formatted = datetime.toLocaleString("en-US",{month: "2-digit",
                day: "2-digit", year:"numeric", hour12:false, hour: "numeric", minute:"numeric"})
           
            
            let y = formatted.slice("6","10")
            let d = formatted.slice("3","5")
            let m = formatted.slice("0","2")
            let formattedDate = (`${y}-${m}-${d}`)
            
            let timeFormatted = formatted.slice("12","17")
           
            document.querySelector("#form-date").value = formattedDate
            document.querySelector("#form-time").value = timeFormatted
            document.querySelector("#form-phone").value =info.event.extendedProps.phone
            
            
            modal.show()
            
            document.querySelector(".btn-close").addEventListener("click", (event) => {
            modal.hide() })
            },
          
          
          
           

            //patch function
            
          events :  async function (fetchInfo, successCallback, failureCallback) {
            try{

              const data = await catchEvent()
              const events = []
                      
              data.forEach(function(ev){
              let event = {
                          title : ev["name"],
                          start : ev["start"],
                          extendedProps:{
                          phone : ev["phone"],
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
    toastFunctionSuccess("Klient úspěšně přidán do kalendáře","info","INFO")

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
let toastFunctionSuccess = (msg,type,head) => {
       
            
            typeToast = document.querySelector(".toasts")
            
            typeToast.className = "toasts " + type
            typeToast.classList.add("visible")
            
            typeToast.querySelector(".toastText p").textContent = msg
            typeToast.querySelector(".toastHead h3").textContent = head
            
            
            setTimeout(()=> {
                typeToast.classList.remove("visible");},3000)
            


        
        

        let toastWindow = document.querySelector(".close")
        toastWindow.addEventListener("click",() => {
            typeToast.classList.remove("visible")

        })


        

       }
       