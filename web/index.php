<link rel="stylesheet" type = "text/css" href="style.css">
<script type="text/javascript" src="scripts.js"></script>
<form method="post" id="fav_form" action="recommend.php">
<div class="discovr">
discovr
</div>
<div class="center">
<input type="submit" class="submit" value="Try Something New!"> <!--Has to go here-->
    <div id="prompt">
        <div id="big_prompt">
        What Are Your 5 Favorite Activities?
        </div>
        <div id="small_prompt">
        Help us get to know you a little better.
        </div>
     </div>
    <div class="row_wrap">
        <?php
        $activities = array(
        '', 
        'Bowling', /*Indoor Sports*/
        'Dance',
        'Golf',
        'Swimming (sport)',
        'Salsa (dance)',
        'Samba',
        'Basketball',
        'Hockey',
        'Racquetball',
        'Table Tennis',
        'Badminton',
        'Curling',
        'Boxing',
        'Physical fitness',
        'Gymnastics',
        'Martial Arts',
        'Yoga',
        'Squash (sport)',
        'Volleyball',
        'Fencing',
        'Trampolining',
        'Handball',
        'Surfing', /*Outdoor Sports*/
        'Baseball',
        'Disc Golf',
        'Cricket',
        'Association football',
        'American football',
        'Tennis',
        'Track and field',
        'Running',
        'Sport Climbing',
        'Rock Climbing',
        'Cycling',
        'Paddleboarding',
        'Field Hockey',
        'Paintball',
        'Rugby football',
        'Skateboarding',
        'Inline skating',
        'Roller skating',
        'Hiking',
        'Rafting',
        'Skiing',
        'Horseback Riding',
        'Parkour',
        'Skydiving',
        'Snowboarding',
        'Softball',
        'Archery ',
        'Shooting sport',
        'Racing',
        'Paragliding',
        'Pottery', /*Arts*/
        'Photography',
        'Painting',
        'Drawing',
        'Singing',
        'Improvisational theatre',
        'Comedy',
        'Theatre',
        'Origami',
        'Sculpture',
        'Karaoke',
        'Charity shop', /*Other*/
        'Billiards',
        'Motorcycling',
        'Reading (process)',
        'Pool (cue sports)',
        'Go Kart',
        'Laser Tag',
        'Mini Golf',
        'Escape room',
        'Gambling ',
        'Arcade game',
        'Bungee jumping',
        'Ziplining',
        );
        $labels = array (
            1 => "Indoor Sports",
            23 => "Outdoor Sports",
            54 => "Arts",
            65 => "Other",
        );
        for($i=0;$i<5;$i++)
        {
            echo '<div><select name="activities[]" id="activities">';
            for($j=0;$j<count($activities);$j++)
            {
                if(array_key_exists ($j, $labels))
                {
                    if($j!=0)
                        echo "</optgroup>";
                    echo "<optgroup label={$labels[$j]}>";
                }
                echo "<option>{$activities[$j]}</option>";
            }
            echo '</optgroup></select></div>';    
        }
        ?>
    </div>
    <div class="row_wrap">
        <input type="text" id="address" name="address" placeholder="Please Enter Address">
        <div id='detect_wrap'>
            <button onclick="getLocation()" type="button" id="detect">Auto Detect</button>
            <input type='hidden' id= 'auto_out' name='auto' value="None" />
        </div>
        <div class="user_rad">
            Search Radius
        
        <input type="range" id="radius" name="radius" value="100" min="10" max="200"
        oninput="radius_out.value=radius.value">
        <output id="radius_out"> 100 </output> miles.
        </div>
    </div>
</div>

</form>

