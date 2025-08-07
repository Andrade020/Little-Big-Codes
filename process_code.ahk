^#!w::
    ; Envia Ctrl+C para copiar o texto selecionado
    Clipboard := ""                  ; limpa o clipboard
    Send, ^c                       ; envia Ctrl+C
    ClipWait, 2                    ; aguarda até 2 segundos para o clipboard ser atualizado
    if ErrorLevel {
        MsgBox, O clipboard não possui texto.
        return
    }
    
    oldClip := ClipboardAll        ; salva o conteúdo atual do clipboard
    inputText := Clipboard

    ; Define os caminhos fixos
    pythonPath := "C:\Users\Leo\AppData\Local\Programs\Python\Python312\python.exe"
    pythonScriptPath := "C:\Users\Leo\Desktop\Porto_Real\Little-Big-Codes\process_code_ahk.py"
    inputFilePath := "C:\Users\Leo\Desktop\Porto_Real\Little-Big-Codes\input.txt"
    outputFilePath := "C:\Users\Leo\Desktop\Porto_Real\Little-Big-Codes\output.txt"

    ; Apaga arquivos anteriores, se existirem
    FileDelete, %inputFilePath%
    FileDelete, %outputFilePath%

    ; Grava o conteúdo do clipboard no arquivo de entrada
    FileAppend, %inputText%, %inputFilePath%

    ; Constrói o comando para chamar o Python exatamente como desejado
    cmd = %pythonPath% "%pythonScriptPath%" "%inputFilePath%" "%outputFilePath%"
    
    ; Executa o comando e aguarda seu término
    RunWait, %cmd%,, Hide

    ; Aguarda até 5 segundos para que o arquivo de saída seja criado
    maxWait := 5000
    waited := 0
    sleepInterval := 200
    while ((!FileExist(outputFilePath)) && (waited < maxWait)) {
         Sleep, %sleepInterval%
         waited += sleepInterval
    }
    if !FileExist(outputFilePath) {
         MsgBox, O arquivo de saída não foi criado.
         return
    }
    
    ; Lê o conteúdo do arquivo de saída
    FileRead, processedText, %outputFilePath%
    
    ; Coloca o resultado no clipboard e cola (Ctrl+V)
    Clipboard := processedText
    Send, ^v

    ; Remove os arquivos temporários
    FileDelete, %inputFilePath%
    FileDelete, %outputFilePath%

    ; (Opcional) Restaura o clipboard original
    ; Clipboard := oldClip
return



