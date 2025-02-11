global passwordHash := ""

; Check if the password file exists, otherwise prompt for an initial password
if (!FileExist("C:\Users\Leo\Desktop\Portfolio\password.txt")) {
    InputBox, newPassword, Set Master Password, Enter a strong password for encryption:
    if ErrorLevel
        ExitApp  ; Exit if the user cancels
    passwordHash := HashPassword(newPassword)
    FileAppend, %passwordHash%, C:\Users\Leo\Desktop\Portfolio\password.txt
    MsgBox, Master password set successfully.
} else {
    FileRead, passwordHash, C:\Users\Leo\Desktop\Portfolio\password.txt
}

; Hotkey: Ctrl + Win + Alt + C to add an encrypted idea
^#!c::
    InputBox, enteredPassword, Authenticate, Enter your master password:
    if ErrorLevel
        return

    if (HashPassword(enteredPassword) != passwordHash) {
        MsgBox, Incorrect password!
        return
    }

    InputBox, idea, Secure Idea, Enter your idea:
    if ErrorLevel
        return

    FormatTime, now, , MM/dd/yyyy HH:mm
    fullText := now " - " idea

    encryptedText := EncryptAES(fullText, enteredPassword)
    
    FileAppend, %encryptedText% "`r`n", C:\Users\Leo\Desktop\Portfolio\Crypt.txt
    MsgBox, Idea saved securely.
return


; Hotkey: Ctrl + Win + Alt + O to decrypt and view ideas
^#!o::
    InputBox, enteredPassword, Authenticate, Enter your master password:
    if ErrorLevel
        return

    if (HashPassword(enteredPassword) != passwordHash) {
        MsgBox, Incorrect password!
        return
    }

    if (!FileExist("C:\Users\Leo\Desktop\Portfolio\Crypt.txt")) {
        MsgBox, No encrypted data found!
        return
    }

    FileRead, encryptedData, C:\Users\Leo\Desktop\Portfolio\Crypt.txt
    decryptedText := DecryptAES(encryptedData, enteredPassword)

    if (decryptedText = "ERROR") {
        MsgBox, Decryption failed!
        return
    }

    MsgBox, %decryptedText%
return


; Hash function to securely store the password
HashPassword(password) {
    tempFile := A_Temp "\hash.txt"
    FileDelete, %tempFile%
    FileAppend, %password%, %tempFile%

    RunWait, "C:\Program Files\OpenSSL-Win64\bin\openssl.exe" dgst -sha256 -r "%tempFile%" > "%tempFile%.out", , Hide
    FileRead, hashOutput, %tempFile%.out

    return Trim(StrSplit(hashOutput, " ")[1])  ; Extract only the hash
}


; Encrypt text using OpenSSL AES-256
EncryptAES(plainText, key) {
    tempInput := A_Temp "\input.txt"
    tempOutput := A_Temp "\output.enc"

    FileDelete, %tempInput%
    FileDelete, %tempOutput%

    FileAppend, %plainText%, %tempInput%

    RunWait, openssl enc -aes-256-cbc -salt -in "%tempInput%" -out "%tempOutput%" -pass pass:%key%, , Hide

    FileRead, encryptedText, %tempOutput%
    return encryptedText
}


; Decrypt text using OpenSSL AES-256
DecryptAES(encryptedText, key) {
    tempInput := A_Temp "\input.enc"
    tempOutput := A_Temp "\output.txt"

    FileDelete, %tempInput%
    FileDelete, %tempOutput%

    FileAppend, %encryptedText%, %tempInput%

    RunWait, openssl enc -aes-256-cbc -d -in "%tempInput%" -out "%tempOutput%" -pass pass:%key%, , Hide

    if !FileExist(tempOutput) {
        return "ERROR"  ; Decryption failed (wrong key)
    }

    FileRead, decryptedText, %tempOutput%
    return decryptedText
}
