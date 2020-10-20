<!-- ######################     Start  of Nav   ############################ -->
<nav>
    <ol>
        <?php
        print '<li class="';
        if($path_parts['filename'] == 'map'){
            print 'activePage';
        }
        print '">';
        print '<a href="map.php">Map</a>';
        print '</li>';

        print '<li class="';
        if($path_parts['filename'] == 'aboutUs'){
            print 'activePage';
        }
        print '">';
        print '<a href="aboutUs.php">About Us</a>';
        print '</li>';

        print '<li class="';
        if($path_parts['filename'] == 'purpose'){
            print 'activePage';
        }
        print '">';
        print '<a href="purpose.php">Purpose</a>';
        print '</li>';



        ?>
    </ol>

</nav>
<!-- ######################     End  of Nav   ############################ -->
