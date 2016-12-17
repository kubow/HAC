# XML DOM Tk Text Browser Editor
    # May 18, 2004
    # Alex Caldwell M.D.
    # alcald2000@yahoo.com
    
    # derived from xmlbrowser.tcl
    #   by Richard Suchenwirth http://wiki.tcl.tk/3884

    # Comparison:
    # Modified to allow real time editing of the XML DOM in memory via events in the Tk text
    # widget.
    # It seems like the text widget is faster than the BWidget Tree. I personally find
    # the table-like layout in the Tk text widget with the color coding is easier to read
    # and find your data than the Tree widget.
    
    # Purpose:
    # to get some XML data, parse it into an XML DOM tree in memory, and then
    # map the DOM structure into an editable display in a Tk text widget. A sort of "Map" is
    # generated in the text widget using marks and tags that corresponds to elements and
    # attributes in the DOM structure. Event bindings are used so that any changes to the data
    # in the text widget are updated in the DOM memory structure in parallel in real time. 
    # The modified DOM can then be dumped as XML to a file, sent to another part of the
    # application, transmitted over the network, etc. It currently dumps the modified DOM
    # as XML to the console when any change is made to the data. So start it from a console.
    
    # This is similar to domtext widget in Swish and Waxml by Steve Ball http://waxml.sourceforge.net
    # I was using a similar technique with SAX and mapping the XML elements and attributes with
    # Tk text widget marks and tags. The problem with the SAX method is that it's sort of one-way
    # SAX works good for mapping the XML data to the text widget display, but when you want to
    # reverse that, and go back to XML from the Tk text widget display, you have to write a unique
    # Tcl script to collect your data and convert it back to XML. So the SAX method is not very 
    # generalizable to different XML schema. Each change in the XML schema means you have to
    # re-write your script.
    # With the DOM model, it is more automatic in both directions and more generalizable to different
    # XML schema.
    
    # Limitations and Bugs: 
    # You can only edit the text node data and the value of the attributes, you can't change the
    # XML schema itself.
    # Don't allow the value of an attribute to become NULL. You can change the value but leave at least
    # one character between the quote marks.

    # To do:
    # wrap it up in a namespace, turn it into a Tcl package and make it behave as a proper Tk widget with
    # options etc like the domtext widget.
    # Add a "Save" button and a better menubar across the top.
    # maybe add some whitespace so variable length text elements will always line up vertically in the
    # display which will make it faster to find stuff.
    # maybe remove or hide the XML element tags in the display and only show the text node data
    # and the attribute values with the element names only across a header at the top.
    
    #BWidget not required since we are going to use a Tk text widget
    #package require BWidget
    
    # we do need the tDOM package
    package require tdom
    
    proc recurseInsert {w node parent} {
        global colorlist color name tag_list
        foreach one $tag_list {
            global $one
        }
        set name [$node nodeName]
        set done 0
        if {$name=="#text" || $name=="#cdata"} {
            set text [string map {\n " "} [$node nodeValue]]
        } else {
            set text <$name
            set lineno [lindex [split [$w index current] "."] 0]
            $w mark set begin$name$lineno [$w index current]
            $w mark gravity begin$name$lineno left
            $w insert end $text
            set text ""
            foreach att [getAttributes $node] {
                $w mark set begin$att$lineno [$w index current]
                $w mark gravity begin$att$lineno left
                catch {set text " $att=\"[$node getAttribute $att]\""
                    $w insert end $text
                }
                $w mark set end$att$lineno [$w index current]
                $w mark gravity end$att$lineno left
                $w tag add $att$lineno "begin$att$lineno + 1 char" end$att$lineno
            }
            # this tests if the option to insert a newline to format the display in the text
            # widget is turned on for this element
            if {[set $name] == "1"} {
                set text ">\n"
            } else {
                set text >
            }
            set children [$node childNodes]
            # I think this is a test to see if the child is a text node
            if {[llength $children]==1 && [$children nodeName]=="#text"} {
                # this tests if the option is turned on for that element to break the data display with
                # a newline on that element.
                # You can format the display in various ways depending on which elements you choose
                # to use newlines on in the Tk text widget.
              
                if {[set $name] == "1"} {
                    append text "[$children nodeValue]\n</$name>\n"
                } else {
                    append text "[$children nodeValue]</$name>"
                }

                
                
                set done 1
            }
        }
        
        $w insert end "$text"
        $w mark set end$name$lineno [$w index current]
        $w mark gravity end$name$lineno left
        $w tag add $name$lineno begin$name$lineno end$name$lineno
        # update the DOM Tree and dump it as XML to the standard output. In application, you would save it
        # or use it somewhere else. Here it's just to monitor the changes to the DOM tree.
        $w tag bind $name$lineno <KeyRelease> "
        set new_text \[$w get begin$name$lineno end$name$lineno\]
        regsub  \"<${name}(.*?)>\" \$new_text \{\} new_text
        regsub  \"</$name>\" \$new_text \{\} new_text
        \[$node firstChild\] nodeValue \$new_text
        puts \"\[\$root asXML\]\"
        "
        $w tag configure $name$lineno -background $color($name) -relief raised -borderwidth 1
        
        foreach att [getAttributes $node] {
            $w tag configure $att$lineno -relief  sunken -background $color($att) -borderwidth 1
            $w tag raise $att$lineno
            # Update DOM tree in memory and dump as XML to the standard output. In application, you would save it
            # or use it somewhere else. Here it's just to monitor the changes to the DOM tree.
            $w tag bind $att$lineno <KeyRelease> "
            set new_attribute \[$w get \"begin$att$lineno + 1 char\" end$att$lineno\]
            regsub -all \{\"\} \$new_attribute \{\} new_attribute
            set new_attribute  \[split \$new_attribute \"=\"\]
            $node setAttribute \[lindex \$new_attribute 0\] \"\[lindex \$new_attribute 1\]\"
            puts \"\[\$root asXML\]\"
            "
            
        }
        
        if !$done {
            foreach child [$node childNodes] {
                recurseInsert $w $child $node
                
            }
            $w mark set startend[lindex [$node nodeName] 0]$lineno current
            $w mark gravity startend[lindex [$node nodeName] 0]$lineno left
            
            if {[set [lindex [$node nodeName] 0]] == "1"} {
                $w insert end "\n</[lindex [$node nodeName] 0]>\n"
            } else {
                $w insert end "</[lindex [$node nodeName] 0]>"
            }
            
            
            $w mark set end[lindex [$node nodeName] 0]$lineno [$w index current]
            $w mark gravity end[lindex [$node nodeName] 0]$lineno left
            $w tag add [lindex [$node nodeName] 0]$lineno startend[lindex [$node nodeName] 0]$lineno \
            end[lindex [$node nodeName] 0]$lineno
            $w tag configure [lindex [$node nodeName] 0]$lineno -background $color([lindex [$node nodeName] 0]) \
            -relief raised -borderwidth 1
        }
    }

    
    proc getAttributes node {
        if {![catch {$node attributes} res]} {set res}
    }
    
    # this is for generating a list of the unique element names and attribute names
    # in your XML data. This will be used for mapping a unique color to the text
    # corresponding to that data in the Tk text widget. It makes an array called color
    # indexed by the element and attribute names, with a value of a color name for the display
    proc recurse_names {node} {
        global tag_list color colorlist
        
        
        foreach child [$node childNodes]  {
            if {![regexp [$child nodeName] $tag_list] && [$child nodeName] != "#text" } {
                lappend tag_list [$child nodeName]
                set color([$child nodeName]) [lindex $colorlist [llength $tag_list]]
                if {[getAttributes $child] != ""} {
                    set match ""
                    if {![regexp [getAttributes $child] $tag_list match]} {
                        lappend tag_list [getAttributes $child]
                        set color([getAttributes $child]) [lindex $colorlist [llength $tag_list]]
                    }
                    
                    if {$match != "" && ![string compare [getAttributes $child] $match]} {
                        lappend tag_list [getAttributes $child]
                        set color([getAttributes $child]) [lindex $colorlist [llength $tag_list]]
                    }
                }
                recurse_names $child
            }
            
        }
    }
    
    
    # Check for an XML file from the command line. If none, present user with a
    # tk_getOpenFile dialog.
    if {[lindex $argv 0] == ""} {
        set            fp [open [tk_getOpenFile]]
    } else {
        set            fp [open [file join [lindex $argv 0]]]
    }
    fconfigure    $fp -encoding utf-8
    set xml [read $fp]
    close         $fp
    
    dom parse  $xml doc
    $doc documentElement root
    
    # BWidget Tree not needed as we are using the Tk text widget
    #Tree .t -yscrollcommand ".y set" -xscrollcommand ".x set" -padx 0
    menubutton .m -text "Options... Add newline to choice of XML tags to format display" -menu .m.menu -indicatoron true
    grid .m -sticky news
    menu .m.menu
    text .t -yscrollcommand ".y set" -xscrollcommand ".x set"  -wrap none
    scrollbar .x -ori hori -command ".t xview"
    scrollbar .y -ori vert -command ".t yview"
    grid .t .y  -sticky news
    grid .x    -sticky news
    grid rowconfig    . 0 -weight 1
    grid columnconfig . 0 -weight 1
    
    # this is a map of the colors to use for the various attributes and elements
    # you want to display - needs to be at least as long as the no. of unique elements and attributes
    # in your XML data
    set colorlist [list  white bisque red green lightblue yellow pink #E4D0EC orange #FF3F3F wheat\
    peachpuff lightgrey olivedrab2  white ivory bisque pink yellow skyblue3]
    
    
    # set up a map of colors for each unique element or attribute
    set tag_list ""
    set color([$root nodeName]) [lindex $colorlist 0]
    lappend tag_list "[$root nodeName]"
    recurse_names $root
    # add menuitems representing the element names to the options menu
    
    foreach one $tag_list {
        .m.menu add checkbutton -label $one -variable $one -onvalue 1 -offvalue 0
    }
    .m.menu add separator
    .m.menu add command -label "Save Options" -command {
        set f [open xmlbrowser.options w]
        foreach one $tag_list {
            puts $f "set $one [set $one]"
        }
        close $f
    }
    
    if {[catch {source ./xmlbrowser.options} res]} {
        toplevel .res
        label .res.label -text "No options file Available...\nSet and save options\nto format display."
        grid .res.label
        button .res.ok -text "OK" -command {
            destroy .res
        }
        grid .res.ok
    }
    
    after 5 recurseInsert .t $root root
