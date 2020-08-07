/* This function is used to show password   */
function showPassword() {
  var x = document.getElementById("myInput");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

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
      document.getElementById("valid_task").innerHTML = '';
      flag1 = true;
    }

    if (isNaN(day) || isNaN(year) || parseInt(year) === 0 || year === '' || day === '' || month === ''){
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


//This function is used to search 


function search() {
  var filter = document.getElementById("search").value.toLowerCase();
  var tr = document.getElementsByClassName("rowUsedForSearch")
  
  
  if(tr){
    for (var i = 0; i < tr.length; i++) {
      
      data = tr[i].getElementsByTagName("td")
      
       td = [data[1].textContent.trim().toLowerCase() ];
       td = td.concat([data[2].textContent.trim().toLowerCase()]);
       if(data[3])
        td = td.concat([data[3].textContent.trim().toLowerCase()]);
        
        if(filter.length === 0) {
          tr[i].style.display = "none";
        }

        else{

          for(let j=0; j<td.length; j++) {
            if ((td[j].includes(filter)) || (filter === td[j])) {
             tr[i].style.display = "";
             break;
             
           } 
          tr[i].style.display = "none";
        }
       
      }
     }
   }
  }
  

  






