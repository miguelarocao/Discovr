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

//loading gif
/*<script>
    function dispLoad () {
       document.getElementById('load').style.visibility="visible";
}
</script>*/

