#!/bin/bash

location="$(curl -s ipinfo.io/city),$(curl -s ipinfo.io/country)"

weather="$(curl -s wttr.in/$location?format=%C,%t)"

case "${weather%%,*}" in
  "Sunny") ascii="    \   /
     .-.     (____)
  ― (-*-) ―  __(__)
     \`-\`  (____)
    /   \\    "
  ;;
  "Cloudy") ascii="             .
      ___   //
     (\` *\`)//
  ___\\\`\\\\__//\`___
((\*   )6   (   \*))
 |    (_Y_)\\\`   |
 '     \`'-'\\\`    '"
  ;;
  "Raining") ascii="    .-.     .-.
     /  \\~~~/  \\
    (  O _ o     )
     \\ --C_--  /
      \`-. .-'\\\`
        \`\"\`      "
  ;;
  "Snowing") ascii="        .-~~--.
   (      ..   )
  (   )\\\\____\\\\(_
   \\_/ /   \\\/
  ___\\\\/____\\\\___
   /     --,   \\\\
  /'~\"\"~\`'-'\"\"~\"\"~\`\\"
  ;;
  "Overcast") ascii="      .--.
   .-(    ).-.
  (___.__)__)  "
  ;;
  "Clear") ascii="
   -^-     _':_
 ^^  * ^-^   _____   ^*^
  ^^        (____))"
 ;;
 "Partly cloudy") ascii="
     ____    __
    (____)__(__)_/
       (_____) \/
     -----( ( ) )-----
          /\___/\
         /   |   \
 "
 ;;
esac


echo "			Weather for $location:"
echo "			$weather"
echo "$ascii"
