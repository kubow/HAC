#!/bin/sh
FILES=${PWD}/*.JPG # input files in JPG format (!case sensitive)
OUTPUT=book.txt # set to the final output file
RESOLUTION=600 # set to the resolution the scanner used (the higher, the better)

touch $OUTPUT
for file in $FILES 
do
    convert -monochrome -density $RESOLUTION $file $file.tif
    # convert -normalize -density $RESOLUTION -depth 8 $SOURCE\[$(($i - 1 ))\] page$i.tif
    echo "processing file $file"
    tesseract -l ces $file.tif tempoutput
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
