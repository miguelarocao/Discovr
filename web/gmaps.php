<html>
<link rel="stylesheet" type = "text/css" href="style.css">
<script type="text/javascript" src="scripts.js"></script>
<body>
<div class='locations'>
<?php 
$act = $_GET['act'];
$address = $_GET['address']; //User input address
$radius = $_GET['radius']; //Search radius

    /*echo 'Inside gmaps.php. some more text to check wrapping of text. <br \>';*/
    
    $string = 'cd ..\gmaps_api & python google_maps.py "'.$act.'" "'.$address.'" "'.$radius.'"';
    /*echo $string;*/
    $output = shell_exec($string);
    $output = str_replace("\n", "<br \><br \>", $output);
    if(is_null($output)){
        echo 'Error: google maps script did not run';
    }
    echo $output
?>
</div>
</body>
</html>