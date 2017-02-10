<form action="calculator.php" method="post">
<input type="text" name="i" />
<select name="co">
<option>plus</option>
<option>minus</option>
<option>deleno</option>
<option>krat</option>
</select>
<input type"text" name="ii" />
<input type="submit" value="Vypocitej!" />
</form>

<?php
$i=$_POST["i"];   // ziskame hodnotu prveho �isla
$ii=$_POST["ii"]; // ziskame hodnotu druheho �isla
$co=$_POST["co"]; // ziskame hodnotu akcie (plus, minus, deleno a krat)
if($i=="" or $ii==""){  // ak hodnota 1. alebo 2. �isla je �iadna vypise:
echo "Zadajte priklad"; // Zadajte priklad
}
elseif($co=="plus"){  // ak hodnota akcie je plus, php bude s�itava�
$vysledok=$i+$ii;     // s�itame
echo "$i + $ii = $vysledok";  //vypiseme vysledok
}
elseif($co=="minus"){  // ak hodnota akcie je minus, php bude od�itava�
$vysledok=$i-$ii;     // od�itame
echo "$i - $ii = $vysledok";  //vypiseme vysledok
}
elseif($co=="deleno"){ // ak hodnota akcie je deleno, php bude deli�
$vysledok=$i/$ii;     // vydelime
echo "$i : $ii = $vysledok";  //vypiaseme vysledok
}
elseif($co=="krat"){  // ak hodnota akcie je krat, php bude kriti�
$vysledok=$i*$ii;     // vykratime
echo "$i x $ii = $vysledok";  //vypiseme vysledok
}
else {
echo "Asi sa stala nejak� chyba :(. Skus to este raz!";
}
?> 