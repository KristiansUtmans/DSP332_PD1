# DSP332_PD1
Mākslīgā intelekta pamati(1),24/25-P 1.praktiskais darbs

# Spēles apraksts
- Spēles sākumā cilvēks-spēlētājs norāda spēlē izmantojamas skaitļu virknes garumu, kas var būt diapazonā no 15 līdz 25 skaitļiem.
- Spēles programmatūra gadījuma ceļā saģenerē skaitļu virkni atbilstoši uzdotajam garumam, tajā iekļaujot skaitļus no 1 līdz 6.

# Spēles gaita
1. Spēlētājs iepazīstas ar spēles noteikumiem;
2. Tiek pieprasīti ievades dati: 
   - spēles skaitļu virknes garums(no 15 līdz 25);
   - pirmais spēlētājs;
   - opcionāli ievades lauki(ja netiek ievadīts, tad tiek iestatīta noklusējuma vērtība):
     - algoritma pārmeklēšanas dziļums;
     - algoritma tips (Minimaksa vai Alfa-beta algoritms).
3. Spēles sākumā ir dota ģenerētā skaitļu virkne un abu spēlētāju punktu skaits ir 0.
4. Spēlētājs izpilda gājienus pēc kārtas. 
   - Gājiena laikā spēlētājs var saskaitīt skaitļu pāri (jebkurus divus skaitļus blakus viens otram), summa tad tiek ierakstīta to vietā:
     - Ja summa ir lielāka par 6, tad pieskaita vienu punktu spēlētāja punktu skaitam un notiek aizvietošana: 7 = 1, 8 = 2, 9 = 3, 10 = 4, 11=5, 12=6
     - Ja summa ir mazāka par 6, tad atņem vienu punktu no spēlētāja punktu skaita.
     

5. Spēle beidzas, kad skaitļu virknē paliek viens skaitlis. Uzvar spēlētājs, kam ir vairāk punktu. Spēlētājam tiek dota iespēja spēlēt atkal - atgriežas uz 2.soli.


## Programmatūrā obligāti ir jānodrošina šādas iespējas lietotājam: 

1. Izvēlēties, kurš uzsāk spēli: cilvēks vai dators;
2. Izvēlēties, kuru algoritmu izmantos dators: Minimaksa algoritmu vai Alfa-beta algoritmu;
3. Izpildīt gājienus un redzēt izmaiņas spēles laukumā pēc gājienu (gan cilvēka, gan datora) izpildes;
4. Uzsākt spēli atkārtoti pēc kārtējās spēles pabeigšanas.

## Obligāti ir jārealizē:
1. Spēles koka vai tā daļas glabāšana datu struktūras veidā (klases, saistītie saraksti). Netiks pieņemti un vērtēti darbi, kuros datu struktūra netiks izveidota, bet tā vietā tiks izmantots mainīgo kopums;
2. Spēles koka vai tā daļas ģenerēšana atkarībā no spēles sarežģītības un studentu komandai pieejamiem skaitļošanas resursiem;
3. Heiristiskā novērtējuma funkcijas izstrāde;
4. Minimaksa algoritms un Alfa-beta algoritms (kas abi var būt realizēti kā Pārlūkošana uz priekšu pār n-gājieniem);
5. (Selenium - automatizēts tests) 10 eksperimenti ar katru no algoritmiem, fiksējot datora un cilvēka uzvaru skaitu, datora apmeklēto virsotņu skaitu, datora vidējo laiku gājiena izpildei.

## izstrādājot darbu, studentu komandai ir jāizpilda šādi soļi:

1. Jāsaņem spēle no mācībspēka;
2. Jāizvēlas programmēšanas vide/valoda;
3. Jāizveido datu struktūra spēles stāvokļu glabāšanai;
4. Jāprojektē, jārealizē un jātestē spēles algoritmi;
5. Jāveic eksperimenti ar abiem algoritmiem;
6. Jāsagatavo atskaite par izstrādāto spēli un tā ir jāiesniedz e-studiju kursā;
7. Jāatbild uz jautājumiem par mākslīgā intelekta rīku izmantošanu spēles izstrādē;
8. Jāveic komandas dalībnieku savstarpējā vērtēšana;
9. Jāpiesakās aizstāvēšanas laikam;
10. Jāaizstāv izstrādātais darbs.