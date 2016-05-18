<html>
<link rel="stylesheet" type = "text/css" href="style.css">
<script type="text/javascript" src="scripts.js"></script>
<body>

<?php 

$activities = $_POST['activities'];
$address = $_POST['address']; //User input address
$autodetect = $_POST['auto']; //Auto detected address, may be 'None' otherwise
                              //'latitude,longitude'
$radius = $_POST['radius']; //Search radius

$string = 'cd .. & python recommend.py ';
foreach($activities as $act)
{
    $string .= '"'.$act.'" ';
}
$string .= '"'.$address.'" ';
$string .= '"'.$autodetect.'" ';
$string .= '"'.$radius.'" ';

//echo 'Eexecuting command : '.$string;
$output = shell_exec($string);
if(is_null($output)){
    echo 'Error: recommendation script did not run';
}

$output = str_replace("'", "", $output);
$output = str_replace("]", "", $output);
$output = str_replace("[", "", $output);

$acts = explode(", ", $output);

/*Query Google Maps*/

$locations = array();

foreach($acts as $act)
{
    $string = 'cd ..\gmaps_api & python google_maps.py "'.$act.'"';
    $output = shell_exec($string);
    $output = str_replace("\n", "<br \><br \>", $output);
    if(is_null($output)){
        echo 'Error: google maps script did not run';
    }
    $locations[]=$output;
}
/*
$locations[]="California Billiard Club:  881 E El Camino Real, Mountain View, CA 94040, United States";
$locations[]="Domino's:  1711 W El Camino Real, Mountain View, CA 94040, United States";
$locations[]="Jo-Ann Fabrics and Crafts:  435 San Antonio Rd, Mountain View, CA 94040, United States";
$locations[]="Buffalo Wild Wings:  43821 Pacific Commons Blvd, Fremont, CA 94538, United States";
$locations[]="
Finish Line (located inside Macy's): 200 W Washington Ave, Sunnyvale, CA 94086, United States<br \><br \>

Finish Line: 300 Standord Mall, Palo Alto, CA 94304, United States<br \><br \>

lululemon athletica | University Ave: 432 University Ave, Palo Alto, CA 94301, United States";
*/

//echo "running command: <br \>".$string."<br \>";

?>
<div class="discovr">
    discovr
</div>
<div class="center">
    <div id="prompt">
        <div id="big_prompt">
            Your Favorite Activies Are
        </div>
        <div class="row_wrap">

            <?php
                foreach($activities as $act)
                    {
                        echo "<div class='choices'>{$act}</div>";
                    }
            ?>
        </div>
        <div id="small_prompt">
            (Good choices.)
        </div>
        <div id="big_prompt">
            We Recommend
        </div>
        <div class="row_wrap">
        <div class="scale"> #1 </div>
        <?php
            for($i=0;$i<count($acts);$i++)
            {
                echo "<div id='r{$i}' class='rec' onclick='toggle_visibility(\"loc{$i}\");'>{$acts[$i]}</div>";
            }
        ?>
        <div class="scale"> #5 </div>
        </div>
        </div>
    </div>
</div>
<div id="loc_wrap">
    <?php
        for($i=0;$i<count($acts);$i++)
        {
            echo "<div class='locations' id='loc{$i}' style='display:none;' >{$locations[$i]}</div>";
        }
    ?>
</div>
<div>
    <button class="back" onClick="goBack()"> Go Back </button>
</div>
</body>
</html>
