; Hotkey: Ctrl + Win + Alt + I to open a small input box for a simple idea
^#!i::
    ; Display an input box for idea entry
    InputBox, idea, Register Idea, Type your idea and press Enter:
    if ErrorLevel  ; If the user cancels or closes the box, do nothing
        return

    ; Get the current date and time in American format (MM/DD/YYYY HH:MM)
    FormatTime, now, , MM/dd/yyyy HH:mm

    ; Create the line to append (with a newline)
    line := now " - " idea "`r`n"

    ; Append the line to the file (the file will be created if it doesn't exist)
    FileAppend, %line%, C:\Users\Leo\Desktop\Portfolio\Ideas.txt
return


; Hotkey: Ctrl + Win + Alt + D to open a larger text box for details
^#!d::
    ; Create a new GUI window with the title "Detalhes"
    Gui, New, , Details
    ; Add a multi-line Edit control (variable: DetalhesEdit) with specified width and height
    Gui, Add, Edit, vDetalhesEdit w400 h200,  ; Empty initial text
    ; Add a Submit button; the "Default" option sets it as the default button
    Gui, Add, Button, Default gSubmitDetails, Submit
    ; Show the GUI window
    Gui, Show
return

; Label for handling the Submit button click in the details GUI
SubmitDetails:
    ; Retrieve the text from the edit control and store it in the variable
    Gui, Submit, NoHide
    ; Append the details below the previous entry in the file, starting on a new line
    FileAppend, % "`r`nDetalhes: " DetalhesEdit "`r`n", C:\Users\Leo\Desktop\Portfolio\Ideas.txt
    ; Close the GUI window
    Gui, Destroy
return

; Handle the GUI window close event (if the user closes the window without clicking Submit)
GuiClose:
    Gui, Destroy
return
