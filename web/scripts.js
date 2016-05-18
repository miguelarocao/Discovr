/*For back button*/
function goBack()
{
    window.history.back();
}

/*To hide and display locations. 5 activities (max).*/
var act_loc=['loc0','loc1','loc2','loc3','loc4'];

function toggle_visibility(id) {
    var e = document.getElementById(id);
    //toggle desired one
    if(e.style.display == 'block')
        e.style.display = 'none';
    else
        e.style.display = 'block';
        
    for(i=0;i<act_loc.length;i++)
    {
        if(act_loc[i]==id)
            continue;
        e = document.getElementById(act_loc[i]);
        e.style.display = 'none';
    }
}

/*Auto location script*/
var x = document.getElementById("demo");
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(autoDetected);
    } 
}

function autoDetected(position) {
    loc_data=String(position.coords.latitude)+','+String(position.coords.longitude);
    //set to form
    document.getElementById('auto_out').value=loc_data;
    document.getElementById('detect').innerHTML='&#10004';
    document.getElementById('detect').style.fontSize='20';
    document.getElementById('detect').style.backgroundColor='#39a939';
    document.getElementById('detect').style.borderBottom='5px solid #0A730A';
    document.getElementById('address').placeholder='Auto detected!';
    document.getElementById('address').style.border='solid 5px #39a939';
    document.getElementById('address').className+=("green-placeholder");
}

/*Radius Slider*/
