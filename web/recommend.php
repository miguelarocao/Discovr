<html>
<body>

You said you like the following activities: <br \><br \>
<?php 
$activities = $_POST['activities'];
$string = 'cd .. & python recommend.py ';
foreach($activities as $act)
{
    $string .= '"'.$act.'" ';
    echo "{$act}<br />";
}

//echo 'We recommend the following activities: <br \>';

//echo 'Eexecuting command : '.$string;
$output = shell_exec($string);
if(is_null($output)){
    echo 'Error: recommendation script did not run';
}

$output = str_replace("'", "", $output);
$output = str_replace("]", "", $output);
$output = str_replace("[", "", $output);

$acts = explode(", ", $output);

echo "<br \>Discovr recommends:<br \><br \>";
foreach($acts as $act)
{
    $string .= '"'.$act.'" ';
    echo "{$act}<br />";
}
echo "<br \><a href=\"javascript:history.go(-1)\">Go Back</a>";
?>

</body>
</html>
