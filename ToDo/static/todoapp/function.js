
 
 
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


function logical(data1,task,element){
  var num = (new Date()).getTime();
  let anyDate = new Date(num);
  var current_date = anyDate.toShortFormat();
  var current_time = formatAMPM(new Date());
  var current_dt = current_date+current_time;
	var timearr =[];
    var i;
    //clearInterval(element);
	for(i=0;i<(data1.length)-1;){
        timearr[timearr.length]=data1[i]+data1[i+1];
        i +=2;
      }
      console.log(timearr);
      console.log(current_dt);
      for(i=0;i<(timearr.length);i++){
        if(current_dt == timearr[i]){
          console.log("inside logic");
          alert(task[i]);
        }
      }
}

function selectAll(mainCheckBox,allCheckboxes){   
    
      if(mainCheckBox.checked){
         
    console.log(mainCheckBox.checked);

    for(var i=0,n=allCheckboxes.length;i<n;i++){
      allCheckboxes[i].checked = true;
    }
        
      }
      else{

    for(var i=0,n=allCheckboxes.length;i<n;i++){
      allCheckboxes[i].checked = false;
      }
    }
   
  }


function sort_() {
  alert("hello");
}
