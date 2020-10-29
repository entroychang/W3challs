<?php

/********************************************************************************************\
|            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                    |
| A comment that seems useless but that is useful nonetheless. Understand if you can :D      |
| Do not remove!                                                                             |
|            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~                    |
\*******************************************************************************************/

session_start();

require_once('lang.php');
require_once('../db/vip.php');

if(!isset($_SESSION['admin']) || $_SESSION['admin']!==True)
	echo fail_auth1;
else
	echo password_is.password('azerfazefazdamlfkazoezaefralmzefalz').'.';

?>
