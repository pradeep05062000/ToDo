Date.prototype.toShortFormat = function() {

    let monthNames =["Jan.","Feb.","March","April",
                      "May","June","July","Aug.",
                      "Sep.", "Oct.","Nov.","Dec."];
    
    let day = this.getDate() + ",";
    
    let monthIndex = this.getMonth();
    let monthName = monthNames[monthIndex];
    
    let year = this.getFullYear();
    
    return `${monthName} ${day} ${year}`;  

}



function formatAMPM(date) {
      var hours = date.getHours();
      var minutes = date.getMinutes();
      var ampm = hours >= 12 ? 'p.m.' : 'a.m.';
      hours = hours % 12;
      hours = hours ? hours : 12; // the hour '0' should be '12'
      minutes = minutes < 10 ? '0'+minutes : minutes;
      var strTime = hours + ':' + minutes + ' ' + ampm;
      return strTime;
    }


function taskNotification(timearr,alarmInfo,task){
  var num = (new Date()).getTime();
  let anyDate = new Date(num);
  var current_date = anyDate.toShortFormat();
  var current_time = formatAMPM(new Date());
  var current_dt = current_date+current_time;
  console.log("inside");
      for(i=0;i<(timearr.length);i++){
        if(current_dt == timearr[i]){
          if (alarmInfo[timearr[i]+task[i]] === "no") {
          alert(task[i]);
          alarmInfo[timearr[i]+task[i]] = "yes";
        }
      }
    }
      
}