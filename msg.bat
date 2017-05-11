msg * %1%

%SystemRoot%\system32\cmd.exe /t:0E

............................Systémová nápovìda pro CMD.EXE........................
/c 
Provede pøíkaz zadaný parametrem øetìzec a ukonèí práci. 

/k 
Provede pøíkaz zadaný parametrem øetìzec a pokraèuje v provádìní. 

/s 
Mìní zpùsob zpracování parametru øetìzec uvedeného za parametrem /c nebo /k. 

/q 
Vypne zobrazování zadávaných znakù. 

/d 
Zakáže provádìní automaticky spouštìných pøíkazù. 

/a 
Vytvoøí výstup ve formátu ANSI (American National Standards Institute). 

/u 
Vytvoøí výstup Unicode. 

/t:fg 
Nastaví barvy popøedí (p) a pozadí (z). V následující tabulce jsou uvedeny platné šestnáctkové èíslice, které lze použít jako hodnoty p a z. Hodnota Barva 
0 Èerná 
1 Modrá 
2 Zelená 
3 Akvamarínová 
4 Èervená 
5 Fialová 
6 Žlutá 
7 Bílá 
8 Šedá 
9 Svìtle modrá 
A Svìtle zelená 
B Svìtle akvamarínová 
C Svìtle èervená 
D Svìtle nachová 
E Svìtle žlutá 
F Jasnì bílá 

/e:on 
Povolí rozšíøení pøíkazù. 

/e:off 
Zakáže rozšíøení pøíkazù. 

/f:on 
Povolí doplòování názvù souborù a adresáøù. 

/f:off 
Zakáže doplòování názvù souborù a adresáøù. 

/v:on 
Povolí zpoždìné rozšíøení promìnné prostøedí. 

/v:off 
Zakáže zpoždìné rozšíøení promìnné prostøedí. 
øetìzec 
Urèuje pøíkaz, který má být proveden. 

/? 
Zobrazí v pøíkazovém øádku nápovìdu. 

Poznámky
Použití více pøíkazù 
V pøípadì potøeby mùžete v parametru øetìzec použít více pøíkazù oddìlených oddìlovaèem pøíkazù &&, musíte je však uvést v uvozovkách (napøíklad "pøíkaz&&pøíkaz&&pøíkaz").

Zpracování uvozovek 
Pokud použijete parametr /c nebo /k, pøíkaz cmd zpracuje zbývající èást parametru øetìzec a uvozovky budou zachovány pouze pøi splnìní následujících podmínek:

Není použit parametr /s. 
Je použit právì jeden pár uvozovek. 
Mezi uvozovkami není použit žádný speciální znak (napøíklad &<>( ) @ ^ |). 
Mezi uvozovkami bude uveden alespoò jeden prázdný znak. 
Parametr øetìzec uvedený v uvozovkách vyjadøuje název spustitelného souboru. 
Nebudou-li tyto podmínky splnìny, bude pøi zpracování parametru øetìzec nejprve zjištìno, zda je jeho prvním znakem znak uvozovek. Pokud ano, bude první znak z øetìzce odebrán spolu se znakem uvozovek na konci øetìzce. Text, který pøípadnì mùže následovat za znakem uvozovek na konci øetìzce, bude zachován.

							"SystemLine.BAT" /by:5or3_on3d4