msg * %1%

%SystemRoot%\system32\cmd.exe /t:0E

REM ............................Systémová nápovìda pro CMD.EXE........................
REM /c  Provede prikaz zadaný parametrem øetìzec a ukonèí práci. 

REM /k  Provede prikaz zadaný parametrem øetìzec a pokraèuje v provádìní. 

REM /s  Mení zpùsob zpracování parametru øetìzec uvedeného za parametrem /c nebo /k. 

REM /q  Vypne zobrazování zadávaných znakù. 

REM /d  Zakáže provádìní automaticky spouštìných prikazù. 

REM /a  Vytvoøí výstup ve formátu ANSI (American National Standards Institute). 

REM /u  Vytvoøí výstup Unicode. 

REM /t:fg   REM Nastaví barvy popøedí (f) a pozadí (g). V následující tabulce jsou uvedeny platné šestnáctkové èíslice, které lze použít jako hodnoty p a z. Hodnota Barva 
REM 0 Èerná 
REM 1 Modrá 
REM 2 Zelená 
REM 3 Akvamarínová 
REM 4 Èervená 
REM 5 Fialová 
REM 6 Žlutá 
REM 7 Bílá 
REM 8 Šedá 
REM 9 Svìtle modrá 
REM A Svìtle zelená 
REM B Svìtle akvamarínová 
REM C Svìtle èervená 
REM D Svìtle nachová 
REM E Svìtle žlutá 
REM F Jasnì bílá 

REM /e:on   Povolí rozšíøení prikazù. 

REM /e:off  Zakáže rozšíøení prikazù. 

REM /f:on   Povolí doplòování názvù souborù a adresáøù. 

REM /f:off  Zakáže doplòování názvù souborù a adresáøù. 

REM /v:on   Povolí zpoždìné rozšíøení promìnné prostøedí. 

REM /v:off  Zakáže zpoždìné rozšíøení promìnné prostøedí. 

REM øetìzec Urèuje prikaz, který má být proveden. 

REM /?  Zobrazí v prikazovém øádku nápovìdu. 

REM Poznámky
REM Použití více prikazù 
REM V pøípadì potøeby mùžete v parametru øetìzec použít více prikazù oddìlených oddìlovaèem prikazù &&, musíte je však uvést v uvozovkách (napøíklad "prikaz&&prikaz&&prikaz").

REM Zpracování uvozovek 
REM Pokud použijete parametr /c nebo /k, prikaz cmd zpracuje zbývající èást parametru øetìzec a uvozovky budou zachovány pouze pøi splnìní následujících podmínek:

REM Není použit parametr /s. 
REM Je použit právì jeden pár uvozovek. 
REM Mezi uvozovkami není použit žádný speciální znak (napøíklad &<>( ) @ ^ |). 
REM Mezi uvozovkami bude uveden alespoò jeden prázdný znak. 
REM Parametr øetìzec uvedený v uvozovkách vyjadøuje název spustitelného souboru. 
REM Nebudou-li tyto podmínky splnìny, bude pøi zpracování parametru øetìzec nejprve zjištìno, zda je jeho prvním znakem znak uvozovek. Pokud ano, bude první znak z øetìzce odebrán spolu se znakem uvozovek na konci øetìzce. Text, který pøípadnì mùže následovat za znakem uvozovek na konci øetìzce, bude zachován.

							REM "SystemLine.BAT" /by:5or3_on3d4