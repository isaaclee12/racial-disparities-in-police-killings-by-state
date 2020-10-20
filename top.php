<?php
$phpSelf = htmlentities($_SERVER['PHP_SELF'], ENT_QUOTES, "UTF-8");

$path_parts = pathinfo($phpSelf);
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <!-- you can add php code here (similar to nav.php) to print a different title on each page -->

        <title>Team Five's Final Project</title>

        <link rel="icon" href="images/Logo.png" sizes="32x32" >
        <meta charset="utf-8">
        <meta name="author" content="Yousef Khan, Grace Bart, Isaac Lee, Phillip Nguyen">
        <meta name="description" content="Social Justice">
        <meta name="viewport" content="width=device-width, initial-scale=1">

     <!--   <link rel="stylesheet" href="finalcss.css" type="text/css" media="screen"> -->
    <?php
            $debug = false;



            if (isset($_GET["debug"])) {
                $debug = true;
            }





    $domain = '//';

    $server = htmlentities($_SERVER['SERVER_NAME'], ENT_QUOTES, 'UTF-8');

    $domain .= $server;

    if ($debug) {
        print '<p>php Self: ' . $phpSelf;
        <!-- print '<pdomain: ' . $domain; -->
        print '<p>Path Parts<pre>';
        print_r($path_parts);
        print '</pre></p>';
    }


    print PHP_EOL . '<!-- include libraries-->' . PHP_EOL;
    require_once 'lib/security.php';
    include_once 'lib/validation-functions.php';
    include_once 'lib/mail-message.php';
    print PHP_EOL . '<!-- finished including libraries -->' . PHP_EOL;
    ?>
    </head>

    <?php
            print '<body id="' . $path_parts['filename'] . '">' . PHP_EOL;

include ('header.php');
print PHP_EOL;

include ('nav.php');
print PHP_EOL;

if ($debug) {
    print '<p>DEBUG MODE IS ON</p>';
}

print "<!-- End of top.php-->";
?>

    <!-- ######################     Start of Body   ############################ -->