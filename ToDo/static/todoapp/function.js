 
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


function form_check() {
    var task = 'task',day,month,year,hr,min,text,date,valid,flag1,flag2,flag3;
    console.log("helllllllllllllll")
    try{
      task=document.getElementById("task").value;
    }
    catch(err){
      
    }
    finally{
    day=document.getElementById("create_day").value;
    month=document.getElementById("create_month").value;
    year=document.getElementById("create_year").value;
    hr=document.getElementById("create_hour").value;
    min=document.getElementById("create_min").value;
    valid=document.getElementById("preventsubmit");
    if (task === '') {

      text = "*Input Required";
      document.getElementById("valid_task").innerHTML = text;
    flag1=false;
    }
    else {
      console.log(task);
      document.getElementById("valid_task").innerHTML = '';
      flag1 = true;
    }

    if (isNaN(day) || isNaN(year) || year==='' || year === '0000' || day === '' || month === ''){
      text = "*Invalid Date";
      document.getElementById("valid_date").innerHTML = text;
      flag2 = false;
    }
    else {
        date = year + "-" + month + "-" + day;
        date =new Date(date);
        if("Invalid Date" === date.toString()) {
          flag2 = false;
          text = "*Invalid Date";
          document.getElementById("valid_date").innerHTML = text;
        }
        else {
           flag2 = true;
           document.getElementById("valid_date").innerHTML = '';
        }
    }       

    if (isNaN(hr) || hr < 0 || hr > 23 || hr === '' || isNaN(min) || min < 0 || min > 59 || min === '') {
      flag3 = false;
      text = "*Invalid Time";
      document.getElementById("valid_time").innerHTML = text;
      
    } 
    else{
       flag3 = true;
      document.getElementById("valid_time").innerHTML = '';
      }

    }

    if (flag1 && flag2 && flag3) {
      console.log("inside submit");
      valid.submit();
    }
    else {
      console.log(flag1,flag2,flag3);
       valid.addEventListener("submit", function(event){
      event.preventDefault()
    });
    }


}




