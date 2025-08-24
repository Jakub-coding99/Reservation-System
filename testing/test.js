let datetime = "Sat Aug 23 2025 12:00:00 GMT+0200 (středoevropský letní čas)"

let t = datetime.replace(" GMT+0200 (středoevropský letní čas)","Z")
dateToFormat = new Date(t).toISOString()


console.log(t)
//"2025-08-23T10:00:00.000Z"



dateToFormat = new Date(t).toISOString()
console.log(dateToFormat)


            // let divided = dateToFormat.split("T")
            // let date = divided[0]
            // let timeToFormate = divided[1]
            // time = timeToFormate.slice("0",5)
            // console.log(time)
            // console.log(date)