Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = oWS.SpecialFolders("Desktop") & "\Robo Visao Noturna.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "C:\Users\Italo\Documents\IAForex\INICIAR_VISAO_NOTURNA.bat"
oLink.WorkingDirectory = "C:\Users\Italo\Documents\IAForex"
oLink.Description = "Robo Visao Noturna - Forex IA"
oLink.IconLocation = "C:\Program Files\MetaTrader 5\terminal64.exe, 0"
oLink.Save
MsgBox "Atalho criado na area de trabalho!", 64, "Robo Visao Noturna"
