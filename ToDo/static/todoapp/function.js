

/* This function is use to select all the check box */

function selectAll(mainCheckBox,allCheckboxes){   
    
    if(mainCheckBox.checked){
         //This condition is used to check wheter the check box of form used to delet object is selcted or not
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

/* This function is used for form (personal task form) validation  */
function form_check() {
    var task = 'task',day,month,year,hr,min,text,date,valid,flag1,flag2,flag3;
    
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
      
      valid.submit();
    }
    else {
      
       valid.addEventListener("submit", function(event){
      event.preventDefault()
    });
    }


}






