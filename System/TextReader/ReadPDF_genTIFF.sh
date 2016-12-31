#!/bin/sh
STARTPAGE=3 # set to pagenumber of the first page of PDF you wish to convert
ENDPAGE=176 # set to pagenumber of the last page of PDF you wish to convert
SOURCE=book.pdf # set to the file name of the PDF
OUTPUT=book.txt # set to the final output file
RESOLUTION=600 # set to the resolution the scanner used (the higher, the better)

touch $OUTPUT
for i in `seq $STARTPAGE $ENDPAGE`; do
    #~ convert -monochrome -density $RESOLUTION $SOURCE\[$(($i - 1 ))\] page.tif
    convert -normalize -density $RESOLUTION -depth 8 $SOURCE\[$(($i - 1 ))\] page$i.tif
    echo processing page $i
    tesseract -l ces page$i.tif tempoutput
    cat tempoutput.txt >> $OUTPUT
done
#~ odkomentovat pro spusteni tesreact

#~ #!/bin/bash
#~ if [ "$1" ] && [ -e "$1" ]; then
  #~ TMPF=$(mktemp XXXXXXXX.tif)
  #~ DEST="$2"
  #~ if [ ! "$DEST" ]; then
    #~ DEST="${1%.*}.txt"
    #~ if [ -e "$DEST" ]; then
      #~ echo "$DEST already exists; please provide a new textfile name" >&2
      #~ exit 1
    #~ fi
  #~ fi
  #~ /usr/bin/convert "$1" -colorspace Gray -depth 8 -resample 200x200 $TMPF \
  #~ && /usr/bin/cuneiform -o "$DEST" $TMPF
  #~ EX=$?
  #~ /bin/rm -f $TMPF
  #~ [ $EX -eq 0 ] && [ "$TERM" ] && echo "created $DEST"
  #~ exit $EX
#~ else
  #~ echo "Usage: $0 imagefile [textfile]" >&2
  #~ echo " creates a plain text file with the text found in imagefile" >&2
  #~ exit 1
#~ fi
