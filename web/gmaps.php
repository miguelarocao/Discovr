<html>
<body>
<?php 
$activity = $_GET['act'];
?>
Google Maps Suggestions for <?php echo $activity?>: <br \><br \>
<?php
$string = 'cd ..\gmaps_api & python google_maps.py "'.$activity.'"';
$output = shell_exec($string);
$output = str_replace("\n", "<br \><br \>", $output);
//echo "running command: <br \>".$string."<br \>";
if(is_null($output)){
    echo 'Error: google maps script did not run';
}

echo $output;
echo "<br \><a href=\"javascript:history.go(-1)\">Go Back</a>";
?>

</body>
</html>